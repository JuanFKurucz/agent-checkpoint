import subprocess
import sys
from pathlib import Path

import pytest

from agent_checkpoint.contracts import Criterion
from agent_checkpoint.runner import CheckDefinition
from agent_checkpoint.service import Service
from agent_checkpoint.storage import StoreError


@pytest.fixture
def service(tmp_path: Path) -> Service:
    root = tmp_path / "repo"
    root.mkdir()
    subprocess.run(["git", "init", "--quiet", str(root)], check=True)
    (root / "check.py").write_text("assert True\n", encoding="utf-8")
    return Service(
        root,
        tmp_path / "state",
        {
            "test": CheckDefinition(argv=(sys.executable, "check.py")),
        },
    )


def start(service: Service) -> str:
    task = service.start_task(
        "Implement behavior",
        [
            Criterion(id="a", text="Behavior verified", check_ids=("test",)),
        ],
        ["test"],
        "start1",
    )
    return task.task_id


def test_full_task_check_mutation_rerun_lifecycle(service: Service) -> None:
    task = start(service)
    missing = service.complete(task)
    assert missing.status == "unresolved"
    assert missing.next_actions[0].reason_code == "EVIDENCE_MISSING"
    service.run_checks(task, ["test"], "run1")
    assert service.complete(task).status == "ready"
    (service.root / "check.py").write_text("assert False\n", encoding="utf-8")
    stale = service.complete(task)
    assert stale.status == "unresolved"
    assert stale.next_actions[0].reason_code == "EVIDENCE_STALE"
    service.run_checks(task, ["test"], "run2")
    assert service.complete(task).status == "needs_changes"
    (service.root / "check.py").write_text("assert True\n# fixed\n", encoding="utf-8")
    service.run_checks(task, ["test"], "run3")
    assert service.complete(task).status == "ready"


def test_check_replay_does_not_execute_again(service: Service) -> None:
    task = start(service)
    first = service.run_checks(task, ["test"], "run1")
    second = service.run_checks(task, ["test"], "run1")
    assert first == second
    assert len(service.store.events(task, service.worktree_id, "check")) == 2


def test_changed_definition_invalidates_old_task(service: Service) -> None:
    task = start(service)
    service.run_checks(task, ["test"], "run1")
    other = Service(
        service.root,
        service.store.state,
        {
            "test": CheckDefinition(argv=(sys.executable, "-c", "pass")),
        },
    )
    with pytest.raises(StoreError, match="POLICY_CHANGED"):
        other.complete(task)


def test_unknown_checks_and_in_repo_state_are_rejected(service: Service) -> None:
    task = start(service)
    with pytest.raises(StoreError, match="CHECK_NOT_ALLOWED"):
        service.run_checks(task, ["unknown"], "run1")
    with pytest.raises(ValueError, match="STATE_INSIDE_WORKSPACE"):
        Service(service.root, service.root / "mutable-state", {})


def test_corrupt_output_does_not_pass(service: Service) -> None:
    task = start(service)
    service.run_checks(task, ["test"], "run1")
    event = service.store.events(task, service.worktree_id, "check")[-1]
    (service.store.blobs / str(event["output_digest"])).write_bytes(b"tampered")
    report = service.complete(task)
    assert report.status == "unresolved"
    assert report.next_actions[0].reason_code == "EVIDENCE_UNAVAILABLE"


def test_completion_does_not_execute_checks(
    service: Service, monkeypatch: pytest.MonkeyPatch
) -> None:
    task = start(service)
    service.run_checks(task, ["test"], "run1")

    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("Implicit execution")

    monkeypatch.setattr("agent_checkpoint.service.run_check", forbidden)
    assert service.complete(task).status == "ready"


def test_context_change_diagnosis_preserves_stale_and_hides_values(service, monkeypatch):
    monkeypatch.setenv("LANG", "synthetic-original")
    task = start(service)
    service.run_checks(task, ["test"], "context-check")
    monkeypatch.setenv("LANG", "synthetic-private-value")
    report = service.complete(task)
    assert report.status == "unresolved"
    assert report.next_actions[0].reason_code == "EVIDENCE_STALE"
    detail = report.stale_diagnostics[0]
    assert detail.context_comparison == "changed"
    assert detail.changed_components == ("environment",)
    assert detail.workspace_generation_changed is False
    assert "synthetic-private-value" not in report.model_dump_json()
    assert "synthetic-original" not in str(service.store.events(task, service.worktree_id, "check"))
    monkeypatch.setenv("LANG", "synthetic-original")
    assert service.complete(task).status == "ready"


def test_file_change_diagnosis_does_not_blame_context(service):
    task = start(service)
    service.run_checks(task, ["test"], "file-check")
    (service.root / "check.py").write_text("assert True\n# edit\n", encoding="utf-8")
    report = service.complete(task)
    assert report.status == "unresolved"
    detail = report.stale_diagnostics[0]
    assert detail.context_comparison == "unchanged"
    assert detail.changed_components == ()
    assert detail.workspace_generation_changed is True


@pytest.mark.parametrize("component", ["runtime", "executable", "launcher"])
def test_safe_component_names_explain_other_context_changes(service, monkeypatch, component):
    from agent_checkpoint.runner import check_context

    task = start(service)
    service.run_checks(task, ["test"], "component-check")
    context = check_context(service.checks["test"], service.root)
    context[component] = "private-path-or-runtime-value"
    monkeypatch.setattr("agent_checkpoint.service.check_context", lambda *args: context)
    report = service.complete(task)
    assert report.status == "unresolved"
    assert report.stale_diagnostics[0].changed_components == (component,)
    assert "private-path" not in report.model_dump_json()


def test_legacy_context_is_unavailable_not_invented(service, monkeypatch):
    task = start(service)
    service.run_checks(task, ["test"], "legacy-check")
    original_events = service.store.events

    def legacy_events(*args):
        return [
            {k: v for k, v in e.items() if k != "context_fingerprints"}
            for e in original_events(*args)
        ]

    monkeypatch.setattr(service.store, "events", legacy_events)
    assert service.complete(task).status == "ready"
    monkeypatch.setenv("LANG", "synthetic-new-value")
    report = service.complete(task)
    assert report.status == "unresolved"
    assert report.stale_diagnostics[0].context_comparison == "unavailable"
    assert report.stale_diagnostics[0].changed_components == ()


def test_interrupted_request_is_not_reexecuted_and_new_task_recovers(
    service: Service, monkeypatch: pytest.MonkeyPatch
) -> None:
    from agent_checkpoint.runner import run_check

    task_id = start(service)

    def interrupt(*args: object) -> None:
        raise KeyboardInterrupt

    monkeypatch.setattr("agent_checkpoint.service.run_check", interrupt)
    with pytest.raises(KeyboardInterrupt):
        service.run_checks(task_id, ["test"], "interrupted")
    report = service.complete(task_id)
    assert report.status == "unresolved"
    assert report.next_actions[0].kind == "reconcile_interrupted_run"
    assert service.run_checks(task_id, ["test"], "interrupted") == {"status": "pending"}
    assert len(service.store.events(task_id, service.worktree_id, "check")) == 1
    monkeypatch.setattr("agent_checkpoint.service.run_check", run_check)
    service.run_checks(task_id, ["test"], "another-attempt")
    assert service.complete(task_id).status == "unresolved"
    old = service.task(task_id)
    recovery = service.start_task(
        old.request, list(old.criteria), list(old.required_check_ids), "recovery-task"
    )
    assert recovery.criteria == old.criteria
    service.run_checks(recovery.task_id, ["test"], "recovery-check")
    assert service.complete(recovery.task_id).status == "ready"
