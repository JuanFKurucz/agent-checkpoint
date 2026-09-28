"""Reporting is historical metadata, never another evidence-producing operation."""

import json
import sqlite3

import pytest

from agent_checkpoint.contracts import Contract, Criterion
from agent_checkpoint.reporting import read_report
from agent_checkpoint.storage import Store, StoreError


@pytest.fixture
def history(tmp_path):
    store = Store(tmp_path / "state")
    contract = Contract(
        task_id="task",
        worktree_id="repo",
        request="PRIVATE_REQUEST",
        criteria=(Criterion(id="behavior", text="PRIVATE_CRITERION"),),
    )
    store.save_contract(contract, "start")
    return store


def test_report_is_readonly_and_omits_sensitive_fields(history):
    history.append_event(
        "task",
        "repo",
        "check",
        {
            "run_id": "run",
            "check_id": "unit",
            "contract_revision": 1,
            "phase": "finished",
            "status": "pass",
            "duration_seconds": 0.2,
            "output": "PRIVATE_OUTPUT",
            "reason": "PRIVATE_REASON",
        },
    )
    history.append_event(
        "task",
        "repo",
        "completion",
        {
            "contract_revision": 1,
            "status": "ready",
            "snapshot_id": "snap",
            "criteria": [{"text": "PRIVATE_CRITERION"}],
        },
    )
    with history.connection() as db:
        before = list(db.iterdump())
    report = read_report(history.state, "repo", "task")
    assert report["readiness"] == "not_revalidated"
    assert report["last_recorded_completion"]["status"] == "ready"
    assert report["events"][0]["recorded_at"] is None
    assert report["events"][0]["reason_code"] == "UNRECOGNIZED_REASON"
    assert "PRIVATE" not in json.dumps(report)
    assert report["producer_version"] is None
    with history.connection() as db:
        assert list(db.iterdump()) == before


def test_report_projects_only_safe_stale_diagnostics(history):
    history.append_event(
        "task",
        "repo",
        "completion",
        {
            "contract_revision": 1,
            "status": "unresolved",
            "stale_diagnostics": [
                {
                    "check_id": "unit",
                    "evidence_id": "run",
                    "context_comparison": "changed",
                    "changed_components": ["environment"],
                    "workspace_generation_changed": False,
                    "raw": "PRIVATE_ENVIRONMENT",
                },
                {
                    "check_id": "unit",
                    "evidence_id": "run",
                    "context_comparison": "changed",
                    "changed_components": ["PRIVATE_COMPONENT"],
                },
            ],
        },
    )
    report = read_report(history.state, "repo", "task")
    details = report["last_recorded_completion"]["stale_diagnostics"]
    assert len(details) == 1
    assert details[0]["changed_components"] == ["environment"]
    assert "PRIVATE" not in json.dumps(report)


def test_report_pairs_observed_check_events_without_rewriting_raw_status(history):
    for phase, state in [("started", "unknown"), ("finished", "pass")]:
        history.append_event(
            "task",
            "repo",
            "check",
            {
                "run_id": "run",
                "check_id": "unit",
                "contract_revision": 1,
                "phase": phase,
                "status": state,
                "duration_seconds": 0,
            },
        )
    report = read_report(history.state, "repo", "task")
    first, last = report["events"]
    assert first["pairing"] == "finish_observed"
    assert first["related_sequence"] == last["sequence"]
    assert first["status"] == "unknown"
    assert first["duration_seconds"] is None
    assert last["pairing"] == "start_observed"
    assert report["readiness"] == "not_revalidated"


def test_pairing_does_not_reach_beyond_bounded_window(history):
    for phase in ["started", "finished"]:
        history.append_event(
            "task",
            "repo",
            "check",
            {
                "run_id": "run",
                "check_id": "unit",
                "contract_revision": 1,
                "phase": phase,
            },
        )
    report = read_report(history.state, "repo", "task", limit=1)
    assert report["truncated"] is True
    assert report["events"][0]["pairing"] == "start_not_observed"
    assert report["events"][0]["related_sequence"] is None


@pytest.mark.parametrize(
    "phases",
    [
        ["started"],
        ["finished"],
        ["started", "started", "finished"],
        ["finished", "started"],
    ],
)
def test_pairing_missing_and_ambiguous_records(history, phases):
    for phase in phases:
        history.append_event(
            "task",
            "repo",
            "operation",
            {
                "operation_id": "operation",
                "operation": "checkpoint_run_checks",
                "contract_revision": 1,
                "phase": phase,
            },
        )
    result = read_report(history.state, "repo", "task")
    expected = (
        "ambiguous"
        if len(phases) > 1
        else ("finish_not_observed" if phases[0] == "started" else "start_not_observed")
    )
    assert all(e["pairing"] == expected for e in result["events"])


@pytest.mark.parametrize(
    "field,value",
    [
        ("contract_revision", 2),
        ("operation", "checkpoint_completion"),
        ("transport", "cli"),
    ],
)
def test_pairing_never_joins_different_associations(history, field, value):
    original = {
        "operation_id": "operation",
        "operation": "checkpoint_run_checks",
        "contract_revision": 1,
        "transport": "mcp",
        "phase": "started",
    }
    history.append_event("task", "repo", "operation", original)
    history.append_event(
        "task", "repo", "operation", {**original, "phase": "finished", field: value}
    )
    assert all(
        e["pairing"] == "ambiguous" for e in read_report(history.state, "repo", "task")["events"]
    )


def test_pairing_requires_association_and_does_not_write(history):
    history.append_event("task", "repo", "check", {"phase": "started", "status": "unknown"})
    with history.connection() as db:
        before = list(db.iterdump())
    report = read_report(history.state, "repo", "task")
    assert report["events"][0]["pairing"] == "association_unavailable"
    with history.connection() as db:
        assert list(db.iterdump()) == before


def test_incomplete_association_in_same_run_prevents_confident_pair(history):
    for phase in ["started", "finished"]:
        history.append_event(
            "task",
            "repo",
            "check",
            {"run_id": "run", "check_id": "unit", "contract_revision": 1, "phase": phase},
        )
    history.append_event("task", "repo", "check", {"run_id": "run", "phase": "started"})
    assert all(
        e["pairing"] == "association_unavailable"
        for e in read_report(history.state, "repo", "task")["events"]
    )


def test_operation_pairs_do_not_join_checks_with_same_identifier(history):
    for phase in ["started", "finished"]:
        history.append_event(
            "task",
            "repo",
            "operation",
            {
                "operation_id": "same",
                "operation": "checkpoint_run_checks",
                "contract_revision": 1,
                "phase": phase,
            },
        )
    history.append_event(
        "task",
        "repo",
        "check",
        {"run_id": "same", "check_id": "unit", "contract_revision": 1, "phase": "started"},
    )
    rows = read_report(history.state, "repo", "task")["events"]
    assert [e["pairing"] for e in rows] == [
        "finish_observed",
        "start_observed",
        "finish_not_observed",
    ]


def test_usage_deduplicates_nested_route_decision_and_keeps_unknown_cost(history):
    decision = {
        "decision_id": "decision",
        "status": "selected",
        "physical_requests": 1,
        "input_tokens": 100,
        "output_tokens": None,
        "duration_seconds": 0.4,
    }
    history.append_event("task", "repo", "decision", decision)
    history.append_event(
        "task", "repo", "route", {"status": "selected", "source": "jev_gateway", "usage": decision}
    )
    report = read_report(history.state, "repo", "task")
    usage = report["usage"]
    assert usage["unique_decisions"] == 1
    assert usage["physical_requests_known"] == 1
    assert usage["input_tokens_known"] == 100
    assert usage["output_tokens_unknown"] == 1
    assert usage["billed_usd"] is None


def test_truncated_window_is_explicit_and_not_a_lifetime_total(history):
    for _ in range(4):
        history.append_event("task", "repo", "check", {"status": "unknown"})
    report = read_report(history.state, "repo", "task", limit=2)
    assert len(report["events"]) == 2
    assert report["truncated"] is True
    assert report["usage"]["scope"] == "returned_event_window"
    assert report["last_recorded_completion"] is None


def test_missing_store_is_not_created(tmp_path):
    state = tmp_path / "missing"
    with pytest.raises(StoreError, match="REPORT_UNAVAILABLE"):
        read_report(state, "repo")
    assert not state.exists()


def test_scopes_tasks_and_rejects_unknown_task(history):
    assert read_report(history.state, "other")["tasks"] == []
    with pytest.raises(StoreError, match="TASK_NOT_FOUND"):
        read_report(history.state, "other", "task")
    with pytest.raises(StoreError, match="TASK_NOT_FOUND"):
        read_report(history.state, "repo", "' OR 1=1 --")


@pytest.mark.parametrize("limit", [0, 201, True, -1])
def test_limits_are_strict(history, limit):
    with pytest.raises(ValueError):
        read_report(history.state, "repo", "task", limit=limit)


def test_corrupt_and_oversized_events_are_flagged_not_echoed(history):
    with history.connection() as db:
        for value in ["not-json PRIVATE", json.dumps({"secret": "PRIVATE" * 20000})]:
            db.execute(
                "INSERT INTO events(task_id,worktree_id,kind,payload) VALUES(?,?,?,?)",
                ("task", "repo", "check", value),
            )
    report = read_report(history.state, "repo", "task")
    assert report["unavailable_events"] == 2
    assert "PRIVATE" not in json.dumps(report)


def test_sqlite_failure_is_sanitized(history):
    with sqlite3.connect(history.state / "checkpoint.sqlite3") as db:
        db.execute("DROP TABLE events")
    with pytest.raises(StoreError, match="^REPORT_UNAVAILABLE$"):
        read_report(history.state, "repo", "task")


def test_conflicting_duplicate_usage_is_unknown_not_double_counted(history):
    history.append_event("task", "repo", "decision", {"decision_id": "d", "physical_requests": 1})
    history.append_event(
        "task", "repo", "route", {"usage": {"decision_id": "d", "physical_requests": 2}}
    )
    usage = read_report(history.state, "repo", "task")["usage"]
    assert usage["conflicting_decisions"] == 1
    assert usage["physical_requests_known"] == 0
    assert usage["physical_requests_unknown"] == 1


def test_foreign_payload_and_free_text_identifiers_do_not_leak(history):
    history.append_event("task", "repo", "check", {"task_id": "other", "status": "pass"})
    history.append_event(
        "task", "repo", "check", {"check_id": "PRIVATE TEXT", "duration_seconds": float("nan")}
    )
    report = read_report(history.state, "repo", "task")
    assert report["unavailable_events"] == 1
    assert report["events"][0]["check_id"].startswith("redacted-")
    assert report["events"][0]["duration_seconds"] is None
    assert "PRIVATE" not in json.dumps(report)


def test_history_actions_never_carry_commands_or_execution_grants(history):
    history.append_event(
        "task",
        "repo",
        "completion",
        {
            "status": "unresolved",
            "next_actions": [
                {
                    "kind": "run_check",
                    "reason_code": "EVIDENCE_MISSING",
                    "check_ids": ["test"],
                    "command": "PRIVATE COMMAND",
                    "authorized_execution": True,
                }
            ],
        },
    )
    report = read_report(history.state, "repo", "task")
    action = report["last_recorded_completion"]["next_actions"][0]
    assert action["authorized_execution"] is False
    assert "command" not in action
    assert "PRIVATE" not in json.dumps(report)


def test_operation_projection_retains_valid_time_but_not_injected_metadata(history):
    history.append_event(
        "task",
        "repo",
        "operation",
        {
            "operation": "checkpoint_completion",
            "operation_id": "op",
            "transport": "mcp",
            "producer_version": "0.1.6",
            "recorded_at": "2026-09-28T01:00:00+00:00",
            "started_at": "PRIVATE",
            "status": "error",
            "reason": "OPERATION_FAILED",
            "request": "PRIVATE",
            "duration_seconds": 0.1,
        },
    )
    event = read_report(history.state, "repo", "task")["events"][0]
    assert event["recorded_at"] == "2026-09-28T01:00:00+00:00"
    assert event["started_at"] is None and event["producer_version"] == "0.1.6"
    assert event["transport"] == "mcp" and "PRIVATE" not in json.dumps(event)
