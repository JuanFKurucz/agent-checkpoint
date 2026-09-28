"""Task-scoped loopback viewer. No mutations, provider loading, or remote assets."""

import hmac
import json
import re
import secrets
import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlsplit

from agent_checkpoint.reporting import read_report
from agent_checkpoint.storage import StoreError

ASSETS = {
    "/": ("index.html", "text/html"),
    "/app.js": ("app.js", "text/javascript"),
    "/style.css": ("style.css", "text/css"),
}


class DashboardServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(
        self,
        state: Path,
        worktree_id: str,
        port: int,
        source_role: str,
        producer_version: str | None,
    ) -> None:
        self.state = state
        self.worktree_id = worktree_id
        self.source_identity = {
            "role": source_role,
            "version": producer_version,
            "basis": "operator_declared_not_attested",
        }
        self.token = secrets.token_urlsafe(32)
        self.slots = threading.BoundedSemaphore(8)
        super().__init__(("127.0.0.1", port), Handler)

    def process_request(
        self, request: socket.socket | tuple[bytes, socket.socket], client_address: Any
    ) -> None:
        if not self.slots.acquire(blocking=False):
            self.shutdown_request(request)
            return
        try:
            super().process_request(request, client_address)
        except BaseException:
            self.slots.release()
            raise

    def process_request_thread(
        self, request: socket.socket | tuple[bytes, socket.socket], client_address: Any
    ) -> None:
        try:
            super().process_request_thread(request, client_address)
        finally:
            self.slots.release()


class Handler(BaseHTTPRequestHandler):
    server: DashboardServer
    server_version = "CheckpointDashboard"
    sys_version = ""

    def setup(self) -> None:
        super().setup()
        self.connection.settimeout(5)

    def log_message(self, format: str, *args: object) -> None:
        # Never log URLs, authorization headers, or report contents.
        return

    def reply(self, code: int, body: bytes, content_type: str = "application/json") -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type + "; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; connect-src 'self'; "
            "object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'",
        )
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def error(self, code: int, reason: str) -> None:
        self.reply(code, json.dumps({"status": "error", "code": reason}).encode())

    def do_GET(self) -> None:
        authority = f"127.0.0.1:{self.server.server_port}"
        if (
            self.headers.get_all("Host") != [authority]
            or self.headers.get_all("Origin") not in (None, [f"http://{authority}"])
            or self.headers.get("Sec-Fetch-Site") not in (None, "none", "same-origin")
        ):
            self.error(403, "ORIGIN_DENIED")
            return
        if len(self.path) > 2048:
            self.error(400, "INVALID_REQUEST")
            return
        try:
            target = urlsplit(self.path)
        except ValueError:
            self.error(400, "INVALID_REQUEST")
            return
        if target.scheme or target.netloc or target.fragment:
            self.error(400, "INVALID_REQUEST")
            return
        if target.path in ASSETS and not target.query:
            filename, mime = ASSETS[target.path]
            self.reply(200, files("agent_checkpoint").joinpath("web", filename).read_bytes(), mime)
            return
        if target.path != "/api/report":
            self.error(404, "NOT_FOUND")
            return
        supplied = self.headers.get("Authorization", "")
        expected = "Bearer " + self.server.token
        if self.headers.get_all("Authorization") != [supplied] or not hmac.compare_digest(
            supplied.encode(), expected.encode()
        ):
            self.error(401, "SESSION_TOKEN_REQUIRED")
            return
        try:
            query = parse_qs(
                target.query, keep_blank_values=True, max_num_fields=3, strict_parsing=True
            )
            if set(query) - {"task", "limit"} or any(len(v) != 1 for v in query.values()):
                raise ValueError
            limit = int(query.get("limit", ["100"])[0])
            task = query.get("task", [None])[0]
            report = read_report(self.server.state, self.server.worktree_id, task, limit=limit)
            report["source_identity"] = self.server.source_identity
            body = json.dumps(report, allow_nan=False).encode()
            if len(body) > 1048576:
                raise StoreError("REPORT_TOO_LARGE")
            self.reply(200, body)
        except (ValueError, OverflowError):
            self.error(400, "INVALID_REQUEST")
        except StoreError as exc:
            code = (
                str(exc)
                if str(exc) in {"TASK_NOT_FOUND", "REPORT_UNAVAILABLE", "REPORT_TOO_LARGE"}
                else "REPORT_UNAVAILABLE"
            )
            self.error(404 if code == "TASK_NOT_FOUND" else 503, code)

    def deny_method(self) -> None:
        self.error(405, "READ_ONLY")

    do_POST = deny_method
    do_PUT = deny_method
    do_DELETE = deny_method
    do_PATCH = deny_method
    do_OPTIONS = deny_method
    do_HEAD = deny_method


def make_server(
    state: Path,
    worktree_id: str,
    *,
    port: int = 0,
    source_role: str = "unknown",
    producer_version: str | None = None,
) -> DashboardServer:
    if type(port) is not int or not 0 <= port <= 65535:
        raise ValueError("INVALID_PORT")
    if source_role not in {"unknown", "pinned_supervisor", "candidate_fixture"}:
        raise ValueError("INVALID_SOURCE_ROLE")
    if producer_version is not None and not re.fullmatch(
        r"\d{1,3}\.\d{1,3}\.\d{1,3}", producer_version
    ):
        raise ValueError("INVALID_PRODUCER_VERSION")
    return DashboardServer(state, worktree_id, port, source_role, producer_version)


def serve_dashboard(
    state: Path,
    worktree_id: str,
    *,
    port: int = 0,
    source_role: str = "unknown",
    producer_version: str | None = None,
) -> None:
    with make_server(
        state, worktree_id, port=port, source_role=source_role, producer_version=producer_version
    ) as server:
        print(f"http://127.0.0.1:{server.server_port}/#token={server.token}", flush=True)
        print(
            "Local read-only dashboard. Polling does not validate readiness. Ctrl+C to stop.",
            flush=True,
        )
        server.serve_forever()
