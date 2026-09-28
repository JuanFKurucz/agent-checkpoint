"""Bounded, read-only projections of recorded history, never fresh evidence."""

import json
import math
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Literal, cast, get_args

from pydantic import Field, TypeAdapter, ValidationError

from agent_checkpoint import __version__
from agent_checkpoint.contracts import Name, NextAction, Record, StaleDiagnostic
from agent_checkpoint.outputs import ErrorResponse
from agent_checkpoint.storage import StoreError, digest

MAX_PAYLOAD = 65536
TraceKind = Literal["check", "route", "review", "decision", "completion", "operation", "unknown"]
Pairing = Literal[
    "finish_observed",
    "start_observed",
    "finish_not_observed",
    "start_not_observed",
    "ambiguous",
    "association_unavailable",
]
REASONS = set(get_args(NextAction.model_fields["reason_code"].annotation)) | {
    "",
    "STALE_OR_UNAVAILABLE",
    "PROVIDER_DISABLED",
    "INPUT_TOO_LARGE",
    "CREDENTIAL_UNAVAILABLE",
    "PROVIDER_DEPENDENCY_UNAVAILABLE",
    "MODEL_IDENTITY_MISMATCH",
    "MALFORMED_RESPONSE",
    "PROVIDER_TIMEOUT",
    "PROVIDER_UNAVAILABLE",
    "BUDGET_EXHAUSTED",
    "DATA_SCOPE_NOT_APPROVED",
    "NO_MATCH",
    "LOCAL_KEYWORD_MATCH",
    "AMBIGUOUS_LOCAL_MATCH",
    "NO_CRITERIA",
    "RESPONSE_TOO_LARGE",
    "OPERATION_FAILED",
}
STATUSES = {
    "pass",
    "fail",
    "unknown",
    "not_applicable",
    "ready",
    "unresolved",
    "needs_changes",
    "selected",
    "none",
    "unavailable",
    "reviewed",
    "started",
    "completed",
    "error",
    "pending",
}


class ReportRequest(Record):
    task_id: Name | None = None
    limit: int = Field(default=100, ge=1, le=200, strict=True)


class TaskSummary(Record):
    task_id: str
    contract_revision: int
    last_sequence: int | None


class TraceEvent(Record):
    sequence: int
    kind: TraceKind
    contract_revision: int | None = None
    recorded_at: str | None = None
    started_at: str | None = None
    operation_id: str | None = None
    operation: str | None = None
    transport: Literal["python", "cli", "mcp"] | None = None
    producer_version: str | None = None
    status: str | None = None
    reason_code: str = ""
    check_id: str | None = None
    run_id: str | None = None
    decision_id: str | None = None
    phase: Literal["started", "finished"] | None = None
    duration_seconds: float | None = None
    selected: tuple[str, ...] = ()
    source: Literal["local", "jev_gateway"] | None = None
    pairing: Pairing | None = None
    related_sequence: int | None = None


class RecordedCheck(Record):
    id: str
    status: str
    reason_code: str


class RecordedAction(Record):
    kind: str
    reason_code: str
    check_ids: tuple[str, ...]
    authorized_execution: Literal[False] = False


class RecordedCompletion(Record):
    sequence: int
    contract_revision: int | None
    status: str
    snapshot_id: str | None
    required_checks: tuple[RecordedCheck, ...]
    next_actions: tuple[RecordedAction, ...]
    stale_diagnostics: tuple[StaleDiagnostic, ...] = ()
    freshness: Literal["not_revalidated"] = "not_revalidated"


class Usage(Record):
    scope: Literal["returned_event_window"] = "returned_event_window"
    unique_decisions: int = 0
    physical_requests_known: int = 0
    physical_requests_unknown: int = 0
    input_tokens_known: int = 0
    input_tokens_unknown: int = 0
    output_tokens_known: int = 0
    output_tokens_unknown: int = 0
    conflicting_decisions: int = 0
    budget_reserved_calls: int | None = None
    billed_usd: None = None


class Report(Record):
    schema_version: Literal["1"] = "1"
    status: Literal["recorded_history"] = "recorded_history"
    readiness: Literal["not_revalidated"] = "not_revalidated"
    reporter_version: str = __version__
    producer_version: None = None
    task_id: str | None
    tasks: tuple[TaskSummary, ...]
    tasks_truncated: bool
    events: tuple[TraceEvent, ...]
    truncated: bool
    unavailable_events: int
    last_recorded_completion: RecordedCompletion | None
    usage: Usage
    limitations: tuple[str, ...] = (
        "Historical metadata only; no checks, provider calls or freshness validation performed.",
        "Missing timestamps and producer versions remain unknown; traces may be incomplete.",
        "Usage is deduplicated within the returned window, not a lifetime or billing total.",
    )


def report_output_schema() -> dict[str, object]:
    return {"type": "object", **TypeAdapter(Report | ErrorResponse).json_schema()}


def identifier(value: object) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    if re.fullmatch(r"[A-Za-z0-9_.:-]{1,256}", value):
        return value
    # Free-text identifiers are correlated through an opaque alias, not echoed.
    return "redacted-" + digest(value)[:16]


def integer(value: object) -> int | None:
    return value if type(value) is int and 0 <= value <= 10**12 else None


def duration(value: object) -> float | None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return None
    result = float(value)
    return result if math.isfinite(result) and 0 <= result <= 86400 else None


def reason(value: object) -> str:
    return value if isinstance(value, str) and value in REASONS else "UNRECOGNIZED_REASON"


def status(value: object) -> str | None:
    return value if isinstance(value, str) and value in STATUSES else None


def timestamp(value: object) -> str | None:
    if (
        not isinstance(value, str)
        or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T[\d:.]+(?:\+00:00|Z)", value)
        or len(value) > 40
    ):
        return None
    try:
        datetime.fromisoformat(value)
        return value
    except ValueError:
        return None


def objects(value: object) -> list[dict[str, object]]:
    if not isinstance(value, list):
        return []
    return [item for item in value[:100] if isinstance(item, dict)]


def completion(sequence: int, data: dict[str, object]) -> RecordedCompletion:
    kinds = set(get_args(NextAction.model_fields["kind"].annotation))
    checks = tuple(
        RecordedCheck(
            id=identifier(c.get("id")) or "unknown",
            status=status(c.get("status")) or "unknown",
            reason_code=reason(c.get("reason", "")),
        )
        for c in objects(data.get("required_checks"))
    )
    actions = []
    for item in objects(data.get("next_actions")):
        kind = item.get("kind")
        if not isinstance(kind, str) or kind not in kinds:
            continue
        ids = item.get("check_ids")
        actions.append(
            RecordedAction(
                kind=kind,
                reason_code=reason(item.get("reason_code")),
                check_ids=tuple(identifier(i) or "unknown" for i in ids[:100])
                if isinstance(ids, list)
                else (),
            )
        )
    diagnostics = []
    for item in objects(data.get("stale_diagnostics")):
        try:
            diagnostics.append(
                StaleDiagnostic.model_validate(
                    {
                        "check_id": identifier(item.get("check_id")) or "unknown",
                        "evidence_id": identifier(item.get("evidence_id")) or "unknown",
                        "context_comparison": item.get("context_comparison"),
                        "changed_components": item.get("changed_components", []),
                        "workspace_generation_changed": item.get("workspace_generation_changed"),
                    }
                )
            )
        except ValidationError:
            continue
    return RecordedCompletion(
        sequence=sequence,
        contract_revision=integer(data.get("contract_revision")),
        status=status(data.get("status")) or "unknown",
        snapshot_id=identifier(data.get("snapshot_id")),
        required_checks=checks,
        next_actions=tuple(actions),
        stale_diagnostics=tuple(diagnostics),
    )


def project(sequence: int, kind: str, data: dict[str, object]) -> TraceEvent:
    selected = data.get("selected")
    phase = data.get("phase")
    source = data.get("source")
    operation = data.get("operation")
    transport = data.get("transport")
    version = data.get("producer_version")
    return TraceEvent(
        sequence=sequence,
        kind=cast(TraceKind, kind) if kind in get_args(TraceKind) else "unknown",
        contract_revision=integer(data.get("contract_revision")),
        recorded_at=timestamp(data.get("recorded_at")),
        started_at=timestamp(data.get("started_at")),
        operation_id=identifier(data.get("operation_id")),
        operation=operation
        if operation
        in (
            "checkpoint_start_task",
            "checkpoint_route",
            "checkpoint_run_checks",
            "checkpoint_review",
            "checkpoint_completion",
        )
        else None,
        transport=transport if transport in ("python", "cli", "mcp") else None,
        producer_version=version
        if isinstance(version, str) and re.fullmatch(r"\d{1,3}\.\d{1,3}\.\d{1,3}", version)
        else None,
        status=status(data.get("status")),
        reason_code=reason(data.get("reason", "")),
        check_id=identifier(data.get("check_id")),
        run_id=identifier(data.get("run_id")),
        decision_id=identifier(data.get("decision_id")),
        phase=phase if phase in ("started", "finished") else None,
        duration_seconds=None if phase == "started" else duration(data.get("duration_seconds")),
        selected=tuple(identifier(i) or "unknown" for i in selected[:40])
        if isinstance(selected, list)
        else (),
        source=source if source in ("local", "jev_gateway") else None,
    )


def pair_events(events: tuple[TraceEvent, ...]) -> tuple[TraceEvent, ...]:
    """Annotate only observed window associations; never infer process liveness."""
    groups: dict[tuple[str, str], list[TraceEvent]] = {}
    updates: dict[int, tuple[Pairing, int | None]] = {}
    for event in events:
        if event.kind not in ("check", "operation"):
            continue
        identity = event.run_id if event.kind == "check" else event.operation_id
        if not identity:
            updates[event.sequence] = ("association_unavailable", None)
            continue
        groups.setdefault((event.kind, identity), []).append(event)
    for group in groups.values():
        if any(
            not (e.check_id if e.kind == "check" else e.operation)
            or not e.contract_revision
            or not e.phase
            for e in group
        ):
            for event in group:
                updates[event.sequence] = ("association_unavailable", None)
            continue
        starts = [e for e in group if e.phase == "started"]
        finishes = [e for e in group if e.phase == "finished"]
        associations = {
            (
                e.contract_revision,
                e.check_id if e.kind == "check" else e.operation,
                e.transport,
                e.producer_version,
            )
            for e in group
        }
        if (
            len(associations) != 1
            or len(starts) > 1
            or len(finishes) > 1
            or (starts and finishes and starts[0].sequence >= finishes[0].sequence)
        ):
            for event in group:
                updates[event.sequence] = ("ambiguous", None)
        elif starts and finishes:
            updates[starts[0].sequence] = ("finish_observed", finishes[0].sequence)
            updates[finishes[0].sequence] = ("start_observed", starts[0].sequence)
        elif starts:
            updates[starts[0].sequence] = ("finish_not_observed", None)
        else:
            updates[finishes[0].sequence] = ("start_not_observed", None)
    return tuple(
        e.model_copy(
            update={"pairing": updates[e.sequence][0], "related_sequence": updates[e.sequence][1]}
        )
        if e.sequence in updates
        else e
        for e in events
    )


def summarize_usage(
    records: list[tuple[int, str, dict[str, object]]], reserved: int | None
) -> Usage:
    decisions: dict[str, dict[str, int | None]] = {}
    conflicts: set[str] = set()
    for _, kind, data in records:
        candidates = [data] if kind == "decision" else []
        route_usage = data.get("usage")
        if kind == "route" and isinstance(route_usage, dict):
            candidates.append(route_usage)
        if kind == "review":
            candidates.extend(objects(data.get("findings")))
        for candidate in candidates:
            key = identifier(candidate.get("decision_id"))
            if key is None:
                continue
            metrics = {
                name: integer(candidate.get(name))
                for name in ("physical_requests", "input_tokens", "output_tokens")
            }
            if key in decisions and decisions[key] != metrics:
                conflicts.add(key)
            decisions[key] = metrics
    sums = {
        name + suffix: 0
        for name in ("physical_requests", "input_tokens", "output_tokens")
        for suffix in ("_known", "_unknown")
    }
    for key, metrics in decisions.items():
        for name, value in metrics.items():
            if value is None or key in conflicts:
                sums[name + "_unknown"] += 1
            else:
                sums[name + "_known"] += value
    return Usage.model_validate(
        {
            "unique_decisions": len(decisions),
            "conflicting_decisions": len(conflicts),
            "budget_reserved_calls": reserved,
            **sums,
        }
    )


def read_report(
    state: Path, worktree_id: str, task_id: str | None = None, *, limit: int = 100
) -> dict[str, object]:
    request = ReportRequest(task_id=task_id, limit=limit)
    database = state.resolve() / "checkpoint.sqlite3"
    db = None
    try:
        db = sqlite3.connect(database.as_uri() + "?mode=ro", uri=True, timeout=1)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA query_only=ON")
        # Bound query work as well as result size, even on an unindexed legacy store.
        ticks = 0

        def bounded() -> int:
            nonlocal ticks
            ticks += 1
            return int(ticks > 2000)

        db.set_progress_handler(bounded, 1000)
        db.execute("BEGIN")
        if db.execute("PRAGMA user_version").fetchone()[0] != 1:
            raise StoreError("REPORT_UNAVAILABLE")
        rows = db.execute(
            "SELECT c.task_id, MAX(c.revision) AS revision, "
            "(SELECT MAX(e.sequence) FROM events e WHERE e.task_id=c.task_id "
            "AND e.worktree_id=c.worktree_id) AS last_sequence "
            "FROM contracts c WHERE c.worktree_id=? GROUP BY c.task_id "
            "ORDER BY last_sequence DESC, c.task_id LIMIT ?",
            (worktree_id, limit + 1),
        ).fetchall()
        tasks = tuple(
            TaskSummary(
                task_id=identifier(row["task_id"]) or "unknown",
                contract_revision=row["revision"],
                last_sequence=row["last_sequence"],
            )
            for row in rows[:limit]
        )
        events: list[tuple[int, str, dict[str, object]]] = []
        unavailable = 0
        truncated = False
        reserved = None
        if request.task_id is not None:
            if (
                db.execute(
                    "SELECT 1 FROM contracts WHERE task_id=? AND worktree_id=? LIMIT 1",
                    (request.task_id, worktree_id),
                ).fetchone()
                is None
            ):
                raise StoreError("TASK_NOT_FOUND")
            raw = db.execute(
                "SELECT sequence, kind, substr(payload,1,?) AS payload FROM events "
                "WHERE task_id=? AND worktree_id=? ORDER BY sequence DESC LIMIT ?",
                (MAX_PAYLOAD + 1, request.task_id, worktree_id, limit + 1),
            ).fetchall()
            truncated = len(raw) > limit
            for row in reversed(raw[:limit]):
                try:
                    payload = row["payload"]
                    if not isinstance(payload, str) or len(payload) > MAX_PAYLOAD:
                        raise ValueError
                    value = json.loads(payload)
                    if not isinstance(value, dict):
                        raise ValueError
                    if value.get("task_id", request.task_id) != request.task_id:
                        raise ValueError
                    if value.get("worktree_id", worktree_id) != worktree_id:
                        raise ValueError
                    events.append((row["sequence"], row["kind"], value))
                except (ValueError, RecursionError):
                    unavailable += 1
            budget = db.execute(
                "SELECT calls FROM budgets WHERE task_id=?", (request.task_id,)
            ).fetchone()
            reserved = integer(budget[0]) if budget else None
        recorded = [completion(seq, data) for seq, kind, data in events if kind == "completion"]
        result = Report(
            task_id=identifier(request.task_id),
            tasks=tasks,
            tasks_truncated=len(rows) > limit,
            events=pair_events(tuple(project(*event) for event in events)),
            truncated=truncated,
            unavailable_events=unavailable,
            last_recorded_completion=recorded[-1] if recorded else None,
            usage=summarize_usage(events, reserved),
        ).model_dump(mode="json")
        if len(json.dumps(result).encode()) > 1048576:
            raise StoreError("REPORT_TOO_LARGE")
        return result
    except sqlite3.Error as exc:
        raise StoreError("REPORT_UNAVAILABLE") from exc
    finally:
        if db is not None:
            db.close()
