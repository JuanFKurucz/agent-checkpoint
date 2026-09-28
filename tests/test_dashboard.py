"""Local HTTP acceptance tests: only synthetic state and loopback sockets."""

import http.client
import json
import threading

import pytest

from agent_checkpoint.contracts import Contract, Criterion
from agent_checkpoint.dashboard import make_server
from agent_checkpoint.storage import Store

pytestmark = pytest.mark.allow_hosts(["127.0.0.1", "::1"])


@pytest.fixture
def dashboard(tmp_path):
    store = Store(tmp_path / "state")
    store.save_contract(
        Contract(
            task_id="task",
            worktree_id="repo",
            request="PRIVATE_REQUEST",
            criteria=(Criterion(id="check", text="PRIVATE_TEXT"),),
        ),
        "start",
    )
    server = make_server(store.state, "repo", port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server, store
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def fetch(server, path="/api/report?task=task", *, headers=None, method="GET"):
    client = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=3)
    try:
        client.request(method, path, headers=headers or {})
        response = client.getresponse()
        return response.status, dict(response.getheaders()), response.read()
    finally:
        client.close()


def test_api_requires_token_and_never_mutates(dashboard):
    server, store = dashboard
    assert fetch(server)[0] == 401
    with store.connection() as db:
        before = list(db.iterdump())
    code, headers, body = fetch(server, headers={"Authorization": "Bearer " + server.token})
    assert code == 200
    assert json.loads(body)["readiness"] == "not_revalidated"
    assert b"PRIVATE" not in body
    assert headers["Cache-Control"] == "no-store"
    assert "Access-Control-Allow-Origin" not in headers
    with store.connection() as db:
        assert list(db.iterdump()) == before


@pytest.mark.parametrize(
    "headers",
    [
        {"Host": "evil.example"},
        {"Origin": "https://evil.example"},
        {"Sec-Fetch-Site": "cross-site"},
        {"Host": "localhost:9999"},
    ],
)
def test_rebinding_and_cross_origin_are_rejected(dashboard, headers):
    server, _ = dashboard
    assert fetch(server, headers={"Authorization": "Bearer " + server.token, **headers})[0] == 403


@pytest.mark.parametrize("method", ["POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
def test_no_write_methods(dashboard, method):
    server, _ = dashboard
    assert fetch(server, method=method)[0] == 405


@pytest.mark.parametrize(
    "path",
    [
        "/api/report?limit=201",
        "/api/report?limit=0",
        "/api/report?limit=a",
        "/api/report?task=task&task=other",
        "/api/report?path=PRIVATE",
    ],
)
def test_api_rejects_unbounded_or_unknown_parameters(dashboard, path):
    server, _ = dashboard
    assert fetch(server, path, headers={"Authorization": "Bearer " + server.token})[0] == 400


def test_static_assets_are_offline_and_path_allowlisted(dashboard):
    server, _ = dashboard
    code, headers, body = fetch(server, "/")
    assert code == 200
    assert "default-src 'self'" in headers["Content-Security-Policy"]
    assert server.token.encode() not in body
    assert b"https://" not in body
    assert fetch(server, "/../checkpoint.sqlite3")[0] == 404
    assert fetch(server, "/app.js")[0] == 200
    assert fetch(server, "/style.css")[0] == 200


def test_missing_store_returns_sanitized_unavailable(dashboard):
    server, store = dashboard
    server.state = store.state / "missing"
    code, _, body = fetch(server, headers={"Authorization": "Bearer " + server.token})
    assert code == 503
    assert json.loads(body) == {"status": "error", "code": "REPORT_UNAVAILABLE"}
    assert not server.state.exists()


def test_source_identity_is_explicitly_declared_not_attested(dashboard):
    server, _ = dashboard
    code, _, body = fetch(server, headers={"Authorization": "Bearer " + server.token})
    assert code == 200
    assert json.loads(body)["source_identity"] == {
        "role": "unknown",
        "version": None,
        "basis": "operator_declared_not_attested",
    }


def test_source_metadata_is_bounded(tmp_path):
    with pytest.raises(ValueError):
        make_server(tmp_path, "repo", source_role="PRIVATE")
    with pytest.raises(ValueError):
        make_server(tmp_path, "repo", producer_version="PRIVATE")
