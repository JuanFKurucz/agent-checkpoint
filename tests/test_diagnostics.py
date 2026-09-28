"""Diagnostics explain evidence gaps; they cannot authorize or execute repairs."""

import pytest
from pydantic import ValidationError

from agent_checkpoint.contracts import Contract, Criterion, Observation, reduce_completion


def task(*, policy="mechanical", bound=("test",), required=True):
    return Contract(
        task_id="task",
        worktree_id="repo",
        request="Verify behavior",
        criteria=(
            Criterion(
                id="behavior",
                text="Behavior",
                evidence_policy=policy,
                check_ids=bound,
                required=required,
            ),
        ),
        required_check_ids=("test",),
    )


def evidence(status="pass", reason=""):
    return Observation(
        evidence_id="run",
        task_id="task",
        worktree_id="repo",
        contract_revision=1,
        snapshot_id="snapshot",
        check_id="test",
        status=status,
        reason=reason,
        provenance="checkpoint_runner",
        current=True,
    )


@pytest.mark.parametrize(
    "status,reason,kind,code",
    [
        ("fail", "", "inspect_check_output", "CHECK_FAILED"),
        ("unknown", "EVIDENCE_STALE", "refresh_stale_evidence", "EVIDENCE_STALE"),
        ("unknown", "INPUT_CHANGED", "refresh_stale_evidence", "INPUT_CHANGED"),
        (
            "unknown",
            "INTERRUPTED_OR_RUNNING",
            "reconcile_interrupted_run",
            "INTERRUPTED_OR_RUNNING",
        ),
        ("unknown", "TIMEOUT", "inspect_check_unavailable", "TIMEOUT"),
        ("unknown", "OUTPUT_LIMIT", "inspect_check_unavailable", "OUTPUT_LIMIT"),
        ("unknown", "EVIDENCE_UNAVAILABLE", "inspect_check_unavailable", "EVIDENCE_UNAVAILABLE"),
    ],
)
def test_diagnostics_distinguish_failures_without_authorizing_execution(status, reason, kind, code):
    result = reduce_completion(task(), "snapshot", [evidence(status, reason)])
    assert result.status == ("needs_changes" if status == "fail" else "unresolved")
    assert result.schema_version == "2"
    assert len(result.next_actions) == 1
    action = result.next_actions[0]
    assert (action.kind, action.reason_code) == (kind, code)
    assert action.check_ids == ("test",) and action.criterion_ids == ("behavior",)
    assert action.evidence_ids == ("run",)
    assert action.authorized_execution is False
    assert result.automatic_continuation_eligible is False


def test_missing_evidence_suggests_declared_check_once():
    result = reduce_completion(task(), "snapshot", [])
    assert len(result.next_actions) == 1
    action = result.next_actions[0]
    assert action.kind == "run_check" and action.reason_code == "EVIDENCE_MISSING"
    assert action.evidence_ids == ()


def test_ready_has_no_required_actions():
    result = reduce_completion(task(), "snapshot", [evidence()])
    assert result.status == "ready" and result.next_actions == ()


@pytest.mark.parametrize(
    "policy,bound,kind,code",
    [
        ("mechanical", (), "resolve_contract_gap", "EVIDENCE_BINDING_MISSING"),
        ("manual", (), "request_manual_attestation", "MANUAL_ATTESTATION_UNAVAILABLE"),
    ],
)
def test_contract_gaps_are_not_disguised_as_checks(policy, bound, kind, code):
    result = reduce_completion(task(policy=policy, bound=bound), "snapshot", [evidence()])
    assert result.status == "unresolved"
    assert result.next_actions[0].kind == kind
    assert result.next_actions[0].reason_code == code
    assert result.next_actions[0].check_ids == ()


def test_optional_unknown_criterion_does_not_create_required_work():
    original = task()
    contract = original.model_copy(
        update={
            "criteria": (
                *original.criteria,
                Criterion(id="optional", text="Optional", required=False, evidence_policy="manual"),
            )
        }
    )
    result = reduce_completion(contract, "snapshot", [evidence()])
    assert result.status == "ready" and result.next_actions == ()


@pytest.mark.parametrize(
    "extra",
    [
        {"authorized_execution": True},
        {"command": "run anything"},
        {"kind": "execute_shell"},
        {"replay_safe": True},
    ],
)
def test_diagnostic_model_cannot_carry_execution_authority(extra):
    from agent_checkpoint.contracts import NextAction

    with pytest.raises(ValidationError):
        NextAction.model_validate(
            {"kind": "run_check", "reason_code": "EVIDENCE_MISSING", "check_ids": ["test"], **extra}
        )
