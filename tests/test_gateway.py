import asyncio
import json
from pathlib import Path

import httpx2
import pytest
from pydantic import ValidationError

from agent_checkpoint.contracts import Contract, Criterion
from agent_checkpoint.gateway import GatewayJev, GatewayPolicy, SelectionRequest
from agent_checkpoint.storage import Store

pytestmark = pytest.mark.allow_hosts(["127.0.0.1", "::1"])
# Windows asyncio uses a loopback socketpair; external connections stay blocked.


def setup(tmp_path: Path) -> Store:
    store = Store(tmp_path / "state")
    store.save_contract(
        Contract(
            task_id="t",
            worktree_id="w",
            request="Synthetic task",
            criteria=(Criterion(id="a", text="Validate"),),
        ),
        "start",
    )
    return store


def request() -> SelectionRequest:
    return SelectionRequest(
        state="Add invalid-input tests.",
        instructions="Pick a skill.",
        candidates={"tests": "Testing", "none": "No relevant skill"},
    )


def response(model: str = "typesafe-ai/jev", choice: str = "tests") -> dict:
    return {
        "model": model,
        "usage": {"input_tokens": 50, "output_tokens": 0},
        "answers": {
            "selection": {
                "type": "choice",
                "choice": choice,
                "confidence": 0.9,
                "probabilities": {"tests": 0.9, "none": 0.1},
            }
        },
    }


@pytest.mark.parametrize(
    "override",
    [
        {"base_url": "https://api.typesafe.ai"},
        {"model": "openai/gpt-5.5"},
        {"api_key_env": "TYPESAFE_API_KEY"},
    ],
)
def test_gateway_policy_cannot_select_direct_provider_or_other_model(override: dict) -> None:
    with pytest.raises(ValidationError):
        GatewayPolicy(**override)


def test_disabled_provider_never_constructs_transport(tmp_path: Path) -> None:
    adapter = GatewayJev(setup(tmp_path), GatewayPolicy())
    result = asyncio.run(adapter.select("t", "w", "r", request()))
    assert result.status == "unavailable"
    assert result.reason == "PROVIDER_DISABLED"
    assert result.physical_requests == 0


def test_gateway_destination_model_retry_and_replay(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("AI_GATEWAY_API_KEY", "synthetic-test-value")
    monkeypatch.setenv("TYPESAFE_BASE_URL", "https://wrong.invalid")
    monkeypatch.setenv("TYPESAFE_DEFAULT_MODEL", "wrong-model")
    calls = []

    def handler(req: httpx2.Request) -> httpx2.Response:
        calls.append(req)
        assert str(req.url) == "https://ai-gateway.vercel.sh/typesafe/v1/systemone"
        assert json.loads(req.content)["model"] == "typesafe-ai/jev"
        return httpx2.Response(200, json=response())

    adapter = GatewayJev(
        setup(tmp_path),
        GatewayPolicy(enabled=True, remote_allowed=True),
        transport=httpx2.MockTransport(handler),
    )
    first = asyncio.run(adapter.select("t", "w", "r", request()))
    second = asyncio.run(adapter.select("t", "w", "r", request()))
    assert first == second
    assert first.status == "selected" and first.selected == "tests"
    assert len(calls) == first.physical_requests == 1
    assert first.identity_verified is False  # Alias, not an exact weight/version pin.


@pytest.mark.parametrize(
    "status,payload,reason",
    [
        (503, {}, "PROVIDER_UNAVAILABLE"),
        (200, {}, "MALFORMED_RESPONSE"),
        (200, response(model="other-model"), "MODEL_IDENTITY_MISMATCH"),
        (200, response(choice="arbitrary-command"), "MALFORMED_RESPONSE"),
    ],
)
def test_bad_responses_abstain_without_retries(tmp_path, monkeypatch, status, payload, reason):
    monkeypatch.setenv("AI_GATEWAY_API_KEY", "synthetic-test-value")
    calls = []

    def handler(req):
        calls.append(req)
        return httpx2.Response(status, json=payload)

    adapter = GatewayJev(
        setup(tmp_path),
        GatewayPolicy(enabled=True, remote_allowed=True),
        transport=httpx2.MockTransport(handler),
    )
    result = asyncio.run(adapter.select("t", "w", "r", request()))
    assert result.status == "unavailable" and result.reason == reason
    assert len(calls) == 1


def test_call_budget_and_input_limit(tmp_path, monkeypatch):
    monkeypatch.setenv("AI_GATEWAY_API_KEY", "synthetic-test-value")
    store = setup(tmp_path)
    adapter = GatewayJev(
        store,
        GatewayPolicy(enabled=True, remote_allowed=True, max_calls_per_task=1),
        transport=httpx2.MockTransport(lambda req: httpx2.Response(200, json=response())),
    )
    assert asyncio.run(adapter.select("t", "w", "r", request())).status == "selected"
    assert asyncio.run(adapter.select("t", "w", "r2", request())).reason == "BUDGET_EXHAUSTED"
    tiny = GatewayJev(store, GatewayPolicy(enabled=True, remote_allowed=True, max_input_bytes=10))
    assert asyncio.run(tiny.select("t", "w", "r3", request())).reason == "INPUT_TOO_LARGE"


def test_total_deadline_cancels_transport(tmp_path, monkeypatch):
    monkeypatch.setenv("AI_GATEWAY_API_KEY", "synthetic-test-value")

    async def handler(req):
        await asyncio.Event().wait()
        raise AssertionError("not reached")

    adapter = GatewayJev(
        setup(tmp_path),
        GatewayPolicy(enabled=True, remote_allowed=True, timeout_seconds=0.02),
        transport=httpx2.MockTransport(handler),
    )
    result = asyncio.run(adapter.select("t", "w", "r", request()))
    assert result.reason == "PROVIDER_TIMEOUT"
    assert result.physical_requests == 1


@pytest.mark.parametrize("compressed", [False, True])
def test_bounded_response_stops_reading_and_closes_stream(tmp_path, monkeypatch, compressed):
    monkeypatch.setenv("AI_GATEWAY_API_KEY", "synthetic-test-value")

    class Stream(httpx2.AsyncByteStream):
        closed = False
        chunks = 0

        async def __aiter__(self):
            for _ in range(4):
                self.chunks += 1
                yield b" " * 40000

        async def aclose(self):
            self.closed = True

    stream = Stream()
    calls = []

    def handler(req):
        calls.append(req)
        return httpx2.Response(
            200, stream=stream, headers={"Content-Encoding": "gzip"} if compressed else {}
        )

    adapter = GatewayJev(
        setup(tmp_path),
        GatewayPolicy(enabled=True, remote_allowed=True),
        transport=httpx2.MockTransport(handler),
    )
    result = asyncio.run(adapter.select("t", "w", "r", request()))
    assert result.reason == (
        "RESPONSE_ENCODING_UNSUPPORTED" if compressed else "PROVIDER_RESPONSE_TOO_LARGE"
    )
    assert stream.closed
    assert stream.chunks == (0 if compressed else 2)
    assert len(calls) == result.physical_requests == 1


def test_bounded_response_accepts_valid_stream(tmp_path, monkeypatch):
    monkeypatch.setenv("AI_GATEWAY_API_KEY", "synthetic-test-value")

    class Stream(httpx2.AsyncByteStream):
        closed = False

        async def __aiter__(self):
            body = json.dumps(response()).encode()
            yield body[:20]
            yield body[20:]

        async def aclose(self):
            self.closed = True

    stream = Stream()
    adapter = GatewayJev(
        setup(tmp_path),
        GatewayPolicy(enabled=True, remote_allowed=True),
        transport=httpx2.MockTransport(lambda req: httpx2.Response(200, stream=stream)),
    )
    result = asyncio.run(adapter.select("t", "w", "r", request()))
    assert result.status == "selected" and stream.closed
