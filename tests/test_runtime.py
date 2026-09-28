import json
import subprocess
import sys
from pathlib import Path

import pytest

from agent_checkpoint.runtime import Runtime
from agent_checkpoint.storage import StoreError


@pytest.fixture
def runtime(tmp_path: Path) -> Runtime:
    root = tmp_path / "repo with spaces"
    root.mkdir()
    subprocess.run(["git", "init", "--quiet", str(root)], check=True)
    (root / "check.py").write_text("assert True\n")
    config = root / "checkpoint.json"
    config.write_text(
        json.dumps(
            {
                "schemaVersion": 1,
                "checks": {"test": {"argv": [sys.executable, "check.py"], "required": True}},
                "skills": {
                    "safety": {"description": "Repository safety", "mandatory": True},
                    "tests": {"description": "Testing", "keywords": ["tests"]},
                },
            }
        )
    )
    return Runtime(root, config, tmp_path / "state")


def payload(request_id="start") -> dict:
    return {
        "request_id": request_id,
        "request": {"text": "Implement input tests"},
        "criteria": [{"id": "a", "text": "Behavior verified", "check_ids": ["test"]}],
    }


def test_shared_runtime_five_operations_and_authority(runtime: Runtime) -> None:
    task = runtime.call("checkpoint_start_task", payload())["task_id"]
    route = runtime.call(
        "checkpoint_route", {"task_id": task, "request_id": "route", "allowed_candidate_ids": []}
    )
    assert route["mandatory"] == ["safety"]
    assert route["selected"] == ["safety"]
    report = runtime.call("checkpoint_completion", {"task_id": task})
    assert report["status"] == "unresolved"
    assert report["schema_version"] == "2"
    assert report["assessment_scope"] == "declared_evidence_only"
    assert report["next_actions"][0]["kind"] == "run_check"
    review = runtime.call("checkpoint_review", {"task_id": task, "request_id": "review"})
    assert review["status"] == "unavailable" and review["reason"] == "PROVIDER_DISABLED"
    run = runtime.call(
        "checkpoint_run_checks", {"task_id": task, "check_ids": ["test"], "request_id": "run"}
    )
    assert run["runs"][0]["status"] == "pass"
    assert runtime.call("checkpoint_completion", {"task_id": task})["status"] == "ready"
    (runtime.root / "check.py").write_text("assert False\n")
    assert runtime.call("checkpoint_completion", {"task_id": task})["status"] == "unresolved"


def test_report_never_executes_refreshes_writes_or_requires_working_config(runtime, monkeypatch):
    task = runtime.call("checkpoint_start_task", payload())["task_id"]
    before = runtime.call("checkpoint_report", {"task_id": task})["events"]

    def forbidden(*args, **kwargs):
        raise AssertionError("Read-only reporting called a mutating operation")

    monkeypatch.setattr(runtime.service, "run_checks", forbidden)
    monkeypatch.setattr(runtime.service, "complete", forbidden)
    monkeypatch.setattr(runtime.service.store, "append_event", forbidden)
    monkeypatch.setattr(runtime, "remote", forbidden)
    monkeypatch.setattr(runtime, "verify_config", forbidden)
    runtime.config_path.write_text("malformed configuration")
    result = runtime.call("checkpoint_report", {"task_id": task})
    assert result["status"] == "recorded_history"
    assert result["readiness"] == "not_revalidated"
    assert result["events"] == before


def test_operation_traces_have_timestamps_identity_and_no_request_text(runtime):
    task = runtime.call("checkpoint_start_task", payload())["task_id"]
    runtime.call(
        "checkpoint_route",
        {"task_id": task, "request_id": "route-private", "allowed_candidate_ids": []},
    )
    report = runtime.call("checkpoint_report", {"task_id": task})
    operations = [e for e in report["events"] if e["kind"] == "operation"]
    assert operations
    assert all(e["recorded_at"] and e["producer_version"] for e in operations)
    assert operations[-1]["operation"] == "checkpoint_route"
    assert operations[-1]["phase"] == "finished"
    assert operations[-1]["duration_seconds"] >= 0
    assert "route-private" not in json.dumps(report)
    assert "Implement input tests" not in json.dumps(report)


def test_trace_failure_does_not_change_core_result_or_leak_error(runtime, monkeypatch, capsys):
    task = runtime.call("checkpoint_start_task", payload())["task_id"]
    original = runtime.service.store.append_event

    def fail_trace(task_id, worktree_id, kind, data):
        if kind == "operation":
            raise StoreError("PRIVATE_FAILURE")
        return original(task_id, worktree_id, kind, data)

    monkeypatch.setattr(runtime.service.store, "append_event", fail_trace)
    result = runtime.call("checkpoint_completion", {"task_id": task})
    assert result["status"] == "unresolved"
    error = capsys.readouterr().err
    assert "trace unavailable" in error and "PRIVATE_FAILURE" not in error


def test_failed_operation_finishes_trace_and_preserves_exception(runtime):
    task = runtime.call("checkpoint_start_task", payload())["task_id"]
    with pytest.raises(StoreError, match="CANDIDATE_NOT_ALLOWED"):
        runtime.call("checkpoint_route", {"task_id": task, "allowed_candidate_ids": ["missing"]})
    operations = [
        e
        for e in runtime.call("checkpoint_report", {"task_id": task})["events"]
        if e["kind"] == "operation"
    ]
    assert operations[-1]["phase"] == "finished"
    assert operations[-1]["status"] == "error"
    assert operations[-1]["reason_code"] == "OPERATION_FAILED"


def test_pending_replay_without_task_field_still_finishes_operation_trace(runtime, monkeypatch):
    task = runtime.call("checkpoint_start_task", payload())["task_id"]
    monkeypatch.setattr(runtime, "execute", lambda request: {"status": "pending"})
    assert runtime.call("checkpoint_route", {"task_id": task}) == {"status": "pending"}
    events = runtime.call("checkpoint_report", {"task_id": task})["events"]
    assert events[-1]["phase"] == "finished" and events[-1]["status"] == "pending"


def test_cli_report_bypasses_runtime_and_works_with_broken_config(runtime, monkeypatch, capsys):
    from agent_checkpoint import cli

    def forbidden(*args, **kwargs):
        raise AssertionError("Reporting initialized runtime")

    monkeypatch.setattr(cli, "Runtime", forbidden)
    runtime.config_path.write_text("malformed configuration")
    assert (
        cli.main(
            ["--root", str(runtime.root), "--state", str(runtime.service.store.state), "report"]
        )
        == 0
    )
    assert json.loads(capsys.readouterr().out)["readiness"] == "not_revalidated"


def test_revision_replay_and_required_criteria_preserved(runtime: Runtime) -> None:
    original = runtime.call("checkpoint_start_task", payload())
    revised = {
        **payload("revision"),
        "task_id": original["task_id"],
        "expected_contract_revision": 1,
    }
    revised["criteria"].append({"id": "b", "text": "Manual review", "evidence_policy": "manual"})
    result = runtime.call("checkpoint_start_task", revised)
    assert result["contract_revision"] == 2
    assert runtime.call("checkpoint_start_task", revised) == result
    revised["request_id"] = "weaken"
    revised["expected_contract_revision"] = 2
    revised["criteria"] = revised["criteria"][:1]
    with pytest.raises(StoreError, match="CONTRACT_WEAKENING"):
        runtime.call("checkpoint_start_task", revised)


@pytest.mark.parametrize(
    "operation,extra",
    [
        ("checkpoint_start_task", {"mode": "enforce"}),
        ("checkpoint_run_checks", {"argv": ["evil"]}),
        ("checkpoint_completion", {"provenance": "checkpoint_runner"}),
        ("checkpoint_review", {"provider": {"enabled": True}}),
    ],
)
def test_wire_unknown_authority_fields_rejected(runtime, operation, extra):
    task = runtime.call("checkpoint_start_task", payload())["task_id"]
    data = (
        payload("bad")
        if operation == "checkpoint_start_task"
        else {"task_id": task, "request_id": "bad", "check_ids": ["test"]}
    )
    with pytest.raises(ValueError):
        runtime.call(operation, {**data, **extra})


def test_candidate_injection_and_configuration_change_rejected(runtime):
    task = runtime.call("checkpoint_start_task", payload())["task_id"]
    with pytest.raises(StoreError, match="CANDIDATE_NOT_ALLOWED"):
        runtime.call("checkpoint_route", {"task_id": task, "allowed_candidate_ids": ["evil"]})
    config = json.loads(runtime.config_path.read_text())
    config["checks"]["test"]["required"] = False
    runtime.config_path.write_text(json.dumps(config))
    with pytest.raises(StoreError, match="POLICY_CHANGED"):
        runtime.call("checkpoint_completion", {"task_id": task})


def test_expected_snapshot_precondition(runtime):
    task = runtime.call("checkpoint_start_task", payload())["task_id"]
    with pytest.raises(StoreError, match="SNAPSHOT_CHANGED"):
        runtime.call(
            "checkpoint_run_checks",
            {
                "task_id": task,
                "check_ids": ["test"],
                "request_id": "run",
                "expected_snapshot_id": "obsolete",
            },
        )
    assert runtime.service.store.events(task, runtime.service.worktree_id, "check") == []


def test_cli_lifecycle_and_safe_errors(runtime, tmp_path):
    contract = tmp_path / "task.json"
    data = payload()
    data.pop("request")
    contract.write_text(json.dumps(data))
    request_file = tmp_path / "request.md"
    request_file.write_text("Implement input tests")
    base = [
        sys.executable,
        "-m",
        "agent_checkpoint",
        "--root",
        str(runtime.root),
        "--config",
        str(runtime.config_path),
        "--state",
        str(runtime.service.store.state),
    ]
    result = subprocess.run(
        [
            *base,
            "task",
            "start",
            "--contract-file",
            str(contract),
            "--request-file",
            str(request_file),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    task = json.loads(result.stdout)["task_id"]
    completed = subprocess.run(
        [*base, "complete", "--task", task, "--json"], capture_output=True, text=True
    )
    assert completed.returncode == 4
    checked = subprocess.run(
        [*base, "check", "run", "--task", task, "test"], capture_output=True, text=True
    )
    assert checked.returncode == 0, checked.stdout
    completed = subprocess.run(
        [*base, "complete", "--task", task, "--json"], capture_output=True, text=True
    )
    assert completed.returncode == 0 and json.loads(completed.stdout)["status"] == "ready"
    contract.write_text('{"private-input":"do not echo", "mode":"enforce"}')
    failed = subprocess.run(
        [
            *base,
            "task",
            "start",
            "--contract-file",
            str(contract),
            "--request-file",
            str(request_file),
        ],
        capture_output=True,
        text=True,
    )
    assert failed.returncode == 2
    assert "do not echo" not in failed.stdout + failed.stderr


def test_duplicate_config_keys_rejected(runtime):
    runtime.config_path.write_text('{"schemaVersion":1,"schemaVersion":1,"checks":{}}')
    with pytest.raises(ValueError, match="DUPLICATE_JSON_KEY"):
        Runtime(runtime.root, runtime.config_path, runtime.service.store.state)


@pytest.mark.parametrize("approved", [[], ["single_route"], ["criterion_evidence"]])
@pytest.mark.parametrize("kind", ["single_route", "criterion_evidence"])
@pytest.mark.allow_hosts(["127.0.0.1", "::1"])
def test_launcher_approved_payload_kinds_are_narrow(runtime, monkeypatch, approved, kind):
    from agent_checkpoint.gateway import Decision, SelectionRequest

    config = json.loads(runtime.config_path.read_text())
    config["provider"] = {
        "enabled": True,
        "remoteAllowed": True,
        "spendAcknowledged": True,
        "approvedPayloadKinds": approved,
    }
    runtime.config_path.write_text(json.dumps(config))
    active = Runtime(runtime.root, runtime.config_path, runtime.service.store.state)
    task = active.call("checkpoint_start_task", payload())["task_id"]
    calls = []

    async def select(self, task_id, worktree_id, request_id, request):
        calls.append(request)
        return Decision(status="none", selected="none")

    monkeypatch.setattr("agent_checkpoint.runtime.GatewayJev.select", select)
    result = active.remote(
        task,
        "route-approved",
        SelectionRequest(
            kind=kind,
            state="Synthetic request",
            instructions="Pick a skill",
            candidates={"tests": "Testing", "none": "No match"}
            if kind == "single_route"
            else {"supported": "Yes", "contradicted": "No", "insufficient": "Unknown"},
        ),
    )
    assert bool(calls) == (kind in approved)
    assert result.status == ("none" if calls else "unavailable")
    assert active.config.provider.policy().model == "typesafe-ai/jev"


def test_payload_kind_approval_rejects_unknown_kind_and_missing_spend():
    from agent_checkpoint.config import ProviderConfig

    with pytest.raises(ValueError):
        ProviderConfig.model_validate({"approvedPayloadKinds": ["raw_source_upload"]})
    with pytest.raises(ValueError, match="SPEND_ACKNOWLEDGEMENT_REQUIRED"):
        ProviderConfig.model_validate(
            {"enabled": True, "remoteAllowed": True, "approvedPayloadKinds": ["single_route"]}
        )


@pytest.mark.parametrize("change", ["input", "revision", "generation"])
def test_stale_advice_is_not_current_but_history_is_preserved(runtime, monkeypatch, change):
    from agent_checkpoint.gateway import Decision

    task = runtime.call("checkpoint_start_task", payload())["task_id"]
    monkeypatch.setattr(
        runtime, "remote", lambda *args: Decision(status="selected", selected="supported")
    )
    runtime.call("checkpoint_review", {"task_id": task, "request_id": "review"})
    report = runtime.call("checkpoint_completion", {"task_id": task})
    assert report["advisory_findings"]
    assert report["status"] == "unresolved"  # Positive advice never passes missing checks.
    if change == "input":
        (runtime.root / "check.py").write_text("assert True\n# changed input\n")
    elif change == "generation":
        original = (runtime.root / "check.py").read_text()
        (runtime.root / "check.py").write_text("assert False\n")
        (runtime.root / "check.py").write_text(original)
    else:
        revised = {**payload("revise"), "task_id": task, "expected_contract_revision": 1}
        runtime.call("checkpoint_start_task", revised)
    current = runtime.call("checkpoint_completion", {"task_id": task})
    assert current["advisory_findings"] == []
    assert len(runtime.service.store.events(task, runtime.service.worktree_id, "review")) == 1


def test_completion_output_validation_rejects_malformed_advice(runtime, monkeypatch):
    task = runtime.call("checkpoint_start_task", payload())["task_id"]
    runtime.call("checkpoint_review", {"task_id": task, "request_id": "review"})
    original_events = runtime.service.store.events

    def bad_events(task_id, worktree_id, kind):
        events = original_events(task_id, worktree_id, kind)
        if kind == "review":
            events[0]["findings"][0]["authority"] = "mechanical"
        return events

    monkeypatch.setattr(runtime.service.store, "events", bad_events)
    with pytest.raises(StoreError, match="INVALID_COMPLETION_OUTPUT"):
        runtime.call("checkpoint_completion", {"task_id": task})
