"""Passing narrow evidence cannot be presented as overall product validation."""

import pytest

from agent_checkpoint.contracts import Contract, Criterion, Observation, reduce_completion
from agent_checkpoint.outputs import completion_output_schema, validate_completion_output
from agent_checkpoint.storage import StoreError


def report(status="pass"):
    contract = Contract(
        task_id="garden",
        worktree_id="sandbox",
        request="Build website",
        criteria=(Criterion(id="syntax", text="JavaScript parses", check_ids=("syntax",)),),
        required_check_ids=("syntax",),
    )
    evidence = Observation(
        evidence_id="run",
        task_id="garden",
        worktree_id="sandbox",
        contract_revision=1,
        snapshot_id="snapshot",
        check_id="syntax",
        status=status,
        provenance="checkpoint_runner",
        current=True,
    )
    return {
        **reduce_completion(contract, "snapshot", [evidence]).model_dump(mode="json"),
        "advisory_findings": [],
    }


@pytest.mark.parametrize(
    "status,expected", [("pass", "ready"), ("fail", "needs_changes"), ("unknown", "unresolved")]
)
def test_completion_scopes_its_claim_without_changing_readiness(status, expected):
    output = validate_completion_output(report(status))
    assert output["status"] == expected
    assert output["assessment_scope"] == "declared_evidence_only"
    assert "not overall product correctness" in output["assessment_notice"]
    assert output["automatic_continuation_eligible"] is False


def test_scope_cannot_be_upgraded_by_a_stored_or_supplied_claim():
    with pytest.raises(StoreError, match="INVALID_COMPLETION_OUTPUT"):
        validate_completion_output({**report(), "assessment_scope": "entire_product_verified"})


def test_wire_schema_publishes_the_scope_and_notice():
    properties = completion_output_schema()["$defs"]["CompletionResponse"]["properties"]
    assert properties["assessment_scope"]["const"] == "declared_evidence_only"
    assert "not overall product correctness" in properties["assessment_notice"]["const"]
