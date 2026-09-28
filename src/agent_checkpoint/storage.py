"""Transactional local records and bounded content-addressed evidence blobs."""

import hashlib
import json
import os
import re
import sqlite3
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from agent_checkpoint.contracts import Contract


class StoreError(RuntimeError):
    """Stable error code; never include raw payloads or credentials."""


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


class Store:
    def __init__(self, state: Path, max_blob_bytes: int = 1_048_576) -> None:
        self.state = state.resolve()
        self.blobs = self.state / "blobs"
        self.max_blob_bytes = max_blob_bytes
        try:
            self.blobs.mkdir(parents=True, exist_ok=True)
            with self.connection() as db:
                version = db.execute("PRAGMA user_version").fetchone()[0]
                if version not in (0, 1):
                    raise StoreError("UNSUPPORTED_STORAGE_VERSION")
                db.execute("PRAGMA journal_mode=WAL")
                db.executescript("""
                    CREATE TABLE IF NOT EXISTS contracts (
                        task_id TEXT NOT NULL, revision INTEGER NOT NULL,
                        worktree_id TEXT NOT NULL, payload TEXT NOT NULL,
                        PRIMARY KEY(task_id, revision));
                    CREATE TABLE IF NOT EXISTS requests (
                        scope TEXT NOT NULL, request_id TEXT NOT NULL,
                        fingerprint TEXT NOT NULL, result TEXT NOT NULL,
                        PRIMARY KEY(scope, request_id));
                    CREATE TABLE IF NOT EXISTS events (
                        sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                        task_id TEXT NOT NULL, worktree_id TEXT NOT NULL,
                        kind TEXT NOT NULL, payload TEXT NOT NULL);
                    CREATE TABLE IF NOT EXISTS budgets (
                        task_id TEXT PRIMARY KEY, calls INTEGER NOT NULL);
                    PRAGMA user_version=1;
                """)
        except OSError as exc:
            raise StoreError("STORAGE_UNAVAILABLE") from exc

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        db: sqlite3.Connection | None = None
        try:
            db = sqlite3.connect(self.state / "checkpoint.sqlite3", timeout=5)
            db.row_factory = sqlite3.Row
            yield db
            db.commit()
        except sqlite3.Error as exc:
            if db is not None:
                db.rollback()
            raise StoreError("STORAGE_UNAVAILABLE") from exc
        except BaseException:
            if db is not None:
                db.rollback()
            raise
        finally:
            if db is not None:
                db.close()

    def save_contract(
        self, contract: Contract, request_id: str, expected_revision: int | None = None
    ) -> Contract:
        payload = contract.model_dump_json()
        fingerprint = digest({"contract": contract.model_dump(), "expected": expected_revision})
        if not request_id.strip():
            raise StoreError("INVALID_REQUEST_ID")
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            scope = "contract:" + contract.worktree_id
            replay = db.execute(
                "SELECT fingerprint, result FROM requests WHERE scope=? AND request_id=?",
                (scope, request_id),
            ).fetchone()
            if replay:
                if replay["fingerprint"] != fingerprint:
                    raise StoreError("IDEMPOTENCY_CONFLICT")
                return Contract.model_validate_json(replay["result"])
            prior = db.execute(
                "SELECT payload FROM contracts WHERE task_id=? ORDER BY revision DESC LIMIT 1",
                (contract.task_id,),
            ).fetchone()
            if prior:
                previous = Contract.model_validate_json(prior["payload"])
                if previous.worktree_id != contract.worktree_id:
                    raise StoreError("TASK_SCOPE_MISMATCH")
                if (
                    expected_revision != previous.contract_revision
                    or contract.contract_revision != expected_revision + 1
                ):
                    raise StoreError("REVISION_CONFLICT")
                old_required = {c.id: c for c in previous.criteria if c.required}
                new_criteria = {c.id: c for c in contract.criteria}
                # No user authentication boundary yet: allow only additive revisions.
                if (
                    previous.request != contract.request
                    or previous.scope_exclude != contract.scope_exclude
                    or any(new_criteria.get(k) != v for k, v in old_required.items())
                    or not set(previous.required_check_ids) <= set(contract.required_check_ids)
                    or previous.policy_digest != contract.policy_digest
                ):
                    raise StoreError("CONTRACT_WEAKENING")
            elif expected_revision is not None or contract.contract_revision != 1:
                raise StoreError("REVISION_CONFLICT")
            db.execute(
                "INSERT INTO contracts VALUES (?, ?, ?, ?)",
                (
                    contract.task_id,
                    contract.contract_revision,
                    contract.worktree_id,
                    payload,
                ),
            )
            db.execute(
                "INSERT INTO requests VALUES (?, ?, ?, ?)",
                (
                    scope,
                    request_id,
                    fingerprint,
                    payload,
                ),
            )
        return contract

    def get_contract(self, task_id: str, worktree_id: str, revision: int | None = None) -> Contract:
        with self.connection() as db:
            if revision is None:
                row = db.execute(
                    "SELECT payload FROM contracts WHERE task_id=? ORDER BY revision DESC LIMIT 1",
                    (task_id,),
                ).fetchone()
            else:
                row = db.execute(
                    "SELECT payload FROM contracts WHERE task_id=? AND revision=?",
                    (task_id, revision),
                ).fetchone()
        if row is None:
            raise StoreError("TASK_NOT_FOUND")
        contract = Contract.model_validate_json(row["payload"])
        if contract.worktree_id != worktree_id:
            raise StoreError("TASK_SCOPE_MISMATCH")
        return contract

    def append_event(self, task_id: str, worktree_id: str, kind: str, payload: object) -> None:
        self.get_contract(task_id, worktree_id)
        with self.connection() as db:
            db.execute(
                "INSERT INTO events(task_id, worktree_id, kind, payload) VALUES (?, ?, ?, ?)",
                (task_id, worktree_id, kind, canonical(payload)),
            )

    def events(self, task_id: str, worktree_id: str, kind: str) -> list[dict[str, object]]:
        self.get_contract(task_id, worktree_id)
        with self.connection() as db:
            rows = db.execute(
                "SELECT payload FROM events WHERE task_id=? AND worktree_id=? AND kind=? "
                "ORDER BY sequence",
                (task_id, worktree_id, kind),
            ).fetchall()
        result: list[dict[str, object]] = []
        for row in rows:
            value = json.loads(row["payload"])
            if not isinstance(value, dict):
                raise StoreError("STORAGE_CORRUPT")
            result.append(value)
        return result

    @staticmethod
    def _report_guard(db: sqlite3.Connection, task_id: str, worktree_id: str) -> tuple[int, int]:
        row = db.execute(
            "SELECT revision, worktree_id FROM contracts WHERE task_id=? "
            "ORDER BY revision DESC LIMIT 1",
            (task_id,),
        ).fetchone()
        if row is None:
            raise StoreError("TASK_NOT_FOUND")
        if row["worktree_id"] != worktree_id:
            raise StoreError("TASK_SCOPE_MISMATCH")
        sequence = db.execute(
            "SELECT COALESCE(MAX(sequence), 0) FROM events WHERE task_id=? "
            "AND kind != 'completion'",
            (task_id,),
        ).fetchone()[0]
        return int(row["revision"]), int(sequence)

    def report_guard(self, task_id: str, worktree_id: str) -> tuple[int, int]:
        with self.connection() as db:
            db.execute("BEGIN")
            return self._report_guard(db, task_id, worktree_id)

    def publish_report(
        self, task_id: str, worktree_id: str, guard: tuple[int, int], payload: object
    ) -> None:
        """CAS publication: revision and evidence high-water must still match."""
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            if self._report_guard(db, task_id, worktree_id) != guard:
                raise StoreError("REPORT_INPUTS_CHANGED")
            db.execute(
                "INSERT INTO events(task_id, worktree_id, kind, payload) VALUES (?, ?, ?, ?)",
                (task_id, worktree_id, "completion", canonical(payload)),
            )

    def reserve_call(self, task_id: str, worktree_id: str, limit: int) -> int:
        self.get_contract(task_id, worktree_id)
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT calls FROM budgets WHERE task_id=?", (task_id,)).fetchone()
            count = row["calls"] if row else 0
            if count >= limit:
                raise StoreError("BUDGET_EXHAUSTED")
            db.execute(
                "INSERT INTO budgets VALUES (?, ?) ON CONFLICT(task_id) "
                "DO UPDATE SET calls=excluded.calls",
                (task_id, count + 1),
            )
        return int(count + 1)

    def claim_request(
        self, scope: str, request_id: str, payload: object
    ) -> dict[str, object] | None:
        """Reserve before external effects. Pending replay never re-executes a check."""
        if not request_id.strip():
            raise StoreError("INVALID_REQUEST_ID")
        fingerprint = digest(payload)
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT fingerprint, result FROM requests WHERE scope=? AND request_id=?",
                (scope, request_id),
            ).fetchone()
            if row:
                if row["fingerprint"] != fingerprint:
                    raise StoreError("IDEMPOTENCY_CONFLICT")
                result: dict[str, object] = json.loads(row["result"])
                return result
            db.execute(
                "INSERT INTO requests VALUES (?, ?, ?, ?)",
                (scope, request_id, fingerprint, canonical({"status": "pending"})),
            )
        return None

    def finish_request(self, scope: str, request_id: str, result: object) -> None:
        with self.connection() as db:
            cursor = db.execute(
                "UPDATE requests SET result=? WHERE scope=? AND request_id=?",
                (canonical(result), scope, request_id),
            )
            if cursor.rowcount != 1:
                raise StoreError("REQUEST_NOT_RESERVED")

    def put_blob(self, data: bytes) -> str:
        if len(data) > self.max_blob_bytes:
            raise StoreError("BLOB_TOO_LARGE")
        blob_id = hashlib.sha256(data).hexdigest()
        target = self.blobs / blob_id
        try:
            with tempfile.NamedTemporaryFile(dir=self.blobs, delete=False) as handle:
                temporary = Path(handle.name)
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            try:
                os.replace(temporary, target)
            finally:
                temporary.unlink(missing_ok=True)
        except OSError as exc:
            raise StoreError("STORAGE_UNAVAILABLE") from exc
        return blob_id

    def get_blob(self, blob_id: str) -> bytes:
        if not re.fullmatch(r"[a-f0-9]{64}", blob_id):
            raise StoreError("INVALID_BLOB_ID")
        try:
            with (self.blobs / blob_id).open("rb") as handle:
                data = handle.read(self.max_blob_bytes + 1)
        except OSError as exc:
            raise StoreError("BLOB_UNAVAILABLE") from exc
        if len(data) > self.max_blob_bytes or hashlib.sha256(data).hexdigest() != blob_id:
            raise StoreError("BLOB_CORRUPT")
        return data
