"""Domain authority must not depend on an agent's completion narrative."""

import pytest
from pydantic import ValidationError

from agent_checkpoint.contracts import Contract, Criterion, Observation, reduce_completion


def contract() -> Contract:
    return Contract(
        task_id="task1",
        worktree_id="workspace1",
        request="Reject invalid inputs",
        criteria=(Criterion(id="AC1", text="Invalid inputs rejected", check_ids=("behavior",)),),
        required_check_ids=("test",),
    )


def observation(check: str, **overrides: object) -> Observation:
    values: dict[str, object] = dict(
        evidence_id="ev-" + check,
        task_id="task1",
        worktree_id="workspace1",
        contract_revision=1,
        snapshot_id="snapshot1",
        check_id=check,
        status="pass",
        provenance="checkpoint_runner",
        current=True,
    )
    values.update(overrides)
    return Observation.model_validate(values)


def test_empty_contract_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Contract(task_id="x", worktree_id="w", request="Do work", criteria=())


@pytest.mark.parametrize("policy", ["semantic_advisory", "informational"])
def test_required_advisory_policy_is_invalid(policy: str) -> None:
    with pytest.raises(ValidationError):
        Criterion(id="a", text="Looks good", evidence_policy=policy)


def test_missing_observations_are_unknown() -> None:
    result = reduce_completion(contract(), "snapshot1", [])
    assert result.status == "unresolved"
    assert result.criteria[0].status == "unknown"


def test_check_results_satisfy_only_explicitly_bound_criteria() -> None:
    result = reduce_completion(contract(), "snapshot1", [observation("test")])
    assert result.status == "unresolved"
    assert result.criteria[0].status == "unknown"


def test_matching_authoritative_evidence_is_ready() -> None:
    result = reduce_completion(
        contract(), "snapshot1", [observation("test"), observation("behavior")]
    )
    assert result.status == "ready"


@pytest.mark.parametrize(
    "overrides",
    [
        {"provenance": "agent_claimed"},
        {"provenance": "semantic_advisory"},
        {"snapshot_id": "old"},
        {"task_id": "other"},
        {"worktree_id": "other"},
        {"contract_revision": 2},
        {"current": False},
    ],
)
def test_invalid_or_stale_provenance_cannot_pass(overrides: dict[str, object]) -> None:
    result = reduce_completion(
        contract(),
        "snapshot1",
        [
            observation("test"),
            observation("behavior", **overrides),
        ],
    )
    assert result.status == "unresolved"


def test_failed_check_dominates_missing_criterion() -> None:
    result = reduce_completion(contract(), "snapshot1", [observation("test", status="fail")])
    assert result.status == "needs_changes"
    assert result.criteria[0].status == "unknown"


def test_manual_criterion_is_not_satisfied_by_a_check() -> None:
    c = contract().model_copy(
        update={
            "criteria": (Criterion(id="review", text="Review behavior", evidence_policy="manual"),)
        }
    )
    assert reduce_completion(c, "snapshot1", [observation("test")]).status == "unresolved"


def test_duplicate_criteria_and_unknown_fields_are_rejected() -> None:
    c = contract()
    with pytest.raises(ValidationError):
        Contract.model_validate({**c.model_dump(), "criteria": [c.criteria[0], c.criteria[0]]})
    with pytest.raises(ValidationError):
        Criterion(id="a", text="Anything", status="pass")


def test_contract_fields_are_frozen() -> None:
    c = contract()
    with pytest.raises(ValidationError):
        c.request = "Actually skip everything"
