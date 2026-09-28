"""Versioned domain records and a pure, conservative readiness reducer.

Observation creation belongs to the trusted runner/reviewer boundary, never an
MCP caller. These models validate shape; they do not authenticate their producer.
"""

from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

Name = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=256)]
Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=16384)]
State = Literal["pass", "fail", "unknown", "not_applicable"]
ContextComponent = Literal["definition", "environment", "runtime", "executable", "launcher"]
Fingerprint = Annotated[str, StringConstraints(pattern=r"^[a-f0-9]{64}$")]


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class ContextFingerprints(Record):
    definition: Fingerprint
    environment: Fingerprint
    runtime: Fingerprint
    executable: Fingerprint
    launcher: Fingerprint


class StaleDiagnostic(Record):
    check_id: Name
    evidence_id: Name
    context_comparison: Literal["changed", "unchanged", "unavailable"]
    changed_components: tuple[ContextComponent, ...] = Field(default=(), max_length=5)
    workspace_generation_changed: bool | None = Field(default=None, strict=True)

    @model_validator(mode="after")
    def consistent(self) -> Self:
        if (self.context_comparison == "changed") != bool(self.changed_components):
            raise ValueError("INCONSISTENT_CONTEXT_DIAGNOSTIC")
        if len(set(self.changed_components)) != len(self.changed_components):
            raise ValueError("DUPLICATE_CONTEXT_COMPONENT")
        return self


class Criterion(Record):
    id: Name
    text: Text
    origin: Literal["user", "repository", "agent_proposed"] = "user"
    required: bool = Field(default=True, strict=True)
    evidence_policy: Literal["mechanical", "manual", "semantic_advisory", "informational"] = (
        "mechanical"
    )
    satisfaction_rule: Name = "approved_checks"
    check_ids: tuple[Name, ...] = ()

    @model_validator(mode="after")
    def authority(self) -> Self:
        if self.required and self.evidence_policy in ("semantic_advisory", "informational"):
            raise ValueError("Required criteria need mechanical/manual evidence authority")
        if len(set(self.check_ids)) != len(self.check_ids):
            raise ValueError("Duplicate criterion check IDs")
        return self


class Contract(Record):
    schema_version: Literal["1"] = "1"
    task_id: Name
    worktree_id: Name
    request: Text
    contract_revision: int = Field(default=1, ge=1, strict=True)
    criteria: tuple[Criterion, ...] = Field(min_length=1)
    required_check_ids: tuple[Name, ...] = ()
    scope_exclude: tuple[Name, ...] = ()
    policy_digest: str = ""

    @model_validator(mode="after")
    def unique(self) -> Self:
        if len({c.id for c in self.criteria}) != len(self.criteria):
            raise ValueError("Duplicate criterion IDs")
        if len(set(self.required_check_ids)) != len(self.required_check_ids):
            raise ValueError("Duplicate required check IDs")
        if not any(c.required for c in self.criteria):
            raise ValueError("A task needs at least one required substantive criterion")
        return self


class Observation(Record):
    evidence_id: Name
    task_id: Name
    worktree_id: Name
    contract_revision: int = Field(ge=1, strict=True)
    snapshot_id: Name
    check_id: str = ""
    criterion_id: str = ""
    status: State
    provenance: Literal["checkpoint_runner", "human_attested", "agent_claimed", "semantic_advisory"]
    current: bool = Field(strict=True)
    reviewer: str = ""
    reason: str = ""


class ItemResult(Record):
    id: Name
    status: State
    evidence_ids: tuple[str, ...] = ()
    reason: str = ""


class NextAction(Record):
    """A diagnostic, never a permission grant, command, or retry instruction."""

    kind: Literal[
        "run_check",
        "inspect_check_output",
        "refresh_stale_evidence",
        "reconcile_interrupted_run",
        "inspect_check_unavailable",
        "request_manual_attestation",
        "resolve_contract_gap",
    ]
    reason_code: Literal[
        "EVIDENCE_MISSING",
        "CHECK_FAILED",
        "EVIDENCE_STALE",
        "INPUT_CHANGED",
        "INTERRUPTED_OR_RUNNING",
        "INTERRUPTED",
        "TIMEOUT",
        "OUTPUT_LIMIT",
        "EVIDENCE_UNAVAILABLE",
        "CHECK_UNAVAILABLE",
        "EXECUTABLE_UNAVAILABLE",
        "EXECUTION_UNAVAILABLE",
        "ISOLATION_UNAVAILABLE",
        "SHELL_WRAPPER_UNSUPPORTED",
        "OUTPUT_CAPTURE_INCOMPLETE",
        "SNAPSHOT_UNAVAILABLE",
        "MANUAL_ATTESTATION_UNAVAILABLE",
        "EVIDENCE_BINDING_MISSING",
        "UNSUPPORTED_EVIDENCE_POLICY",
    ]
    priority: Literal["required"] = "required"
    criterion_ids: tuple[Name, ...] = ()
    check_ids: tuple[Name, ...] = ()
    evidence_ids: tuple[Name, ...] = ()
    authorized_execution: Literal[False] = False


class Completion(Record):
    # Contract/config/storage schemas remain v1. Only completion wire output changes.
    schema_version: Literal["2"] = "2"
    task_id: Name
    contract_revision: int
    snapshot_id: Name
    status: Literal["ready", "needs_changes", "unresolved"]
    criteria: tuple[ItemResult, ...]
    required_checks: tuple[ItemResult, ...]
    automatic_continuation_eligible: Literal[False] = False
    next_actions: tuple[NextAction, ...] = ()
    stale_diagnostics: tuple[StaleDiagnostic, ...] = ()

    @model_validator(mode="after")
    def ready_has_no_required_actions(self) -> Self:
        if self.status == "ready" and self.next_actions:
            raise ValueError("READY_WITH_REQUIRED_ACTIONS")
        return self


def completion_actions(
    contract: Contract, checks: dict[str, ItemResult], results: list[ItemResult]
) -> tuple[NextAction, ...]:
    """Explain the reducer's obligations without inventing checks or semantic proof."""
    bindings: dict[str, list[str]] = {key: [] for key in contract.required_check_ids}
    actions: list[NextAction] = []
    for criterion, result in zip(contract.criteria, results, strict=True):
        if not criterion.required:
            continue
        if (
            criterion.evidence_policy == "mechanical"
            and criterion.satisfaction_rule == "approved_checks"
        ):
            for key in criterion.check_ids:
                bindings.setdefault(key, []).append(criterion.id)
            if not criterion.check_ids:
                actions.append(
                    NextAction(
                        kind="resolve_contract_gap",
                        reason_code="EVIDENCE_BINDING_MISSING",
                        criterion_ids=(criterion.id,),
                    )
                )
        elif result.status not in ("pass", "not_applicable"):
            actions.append(
                NextAction(
                    kind="request_manual_attestation"
                    if criterion.evidence_policy == "manual"
                    else "resolve_contract_gap",
                    reason_code="MANUAL_ATTESTATION_UNAVAILABLE"
                    if criterion.evidence_policy == "manual"
                    else "UNSUPPORTED_EVIDENCE_POLICY",
                    criterion_ids=(criterion.id,),
                )
            )
    for key, criterion_ids in bindings.items():
        item = checks.get(key)
        if item is not None and item.status == "pass":
            continue
        if item is None:
            kind, reason = "run_check", "EVIDENCE_MISSING"
        elif item.status == "fail":
            kind, reason = "inspect_check_output", "CHECK_FAILED"
        elif item.reason in ("EVIDENCE_STALE", "INPUT_CHANGED"):
            kind, reason = "refresh_stale_evidence", item.reason
        elif item.reason in ("INTERRUPTED_OR_RUNNING", "INTERRUPTED"):
            kind, reason = "reconcile_interrupted_run", item.reason
        else:
            kind = "inspect_check_unavailable"
            reason = (
                item.reason
                if item.reason
                in {
                    "TIMEOUT",
                    "OUTPUT_LIMIT",
                    "EVIDENCE_UNAVAILABLE",
                    "CHECK_UNAVAILABLE",
                    "EXECUTABLE_UNAVAILABLE",
                    "EXECUTION_UNAVAILABLE",
                    "ISOLATION_UNAVAILABLE",
                    "SHELL_WRAPPER_UNSUPPORTED",
                    "OUTPUT_CAPTURE_INCOMPLETE",
                    "SNAPSHOT_UNAVAILABLE",
                }
                else "CHECK_UNAVAILABLE"
            )
        actions.append(
            NextAction.model_validate(
                {
                    "kind": kind,
                    "reason_code": reason,
                    "check_ids": (key,),
                    "criterion_ids": tuple(criterion_ids),
                    "evidence_ids": item.evidence_ids if item else (),
                }
            )
        )
    return tuple(actions)


def _state(items: list[ItemResult]) -> State:
    if any(i.status == "fail" for i in items):
        return "fail"
    if not items or any(i.status == "unknown" for i in items):
        return "unknown"
    return "pass"


def reduce_completion(
    contract: Contract, snapshot_id: str, observations: list[Observation]
) -> Completion:
    """Reduce validated current observations; input order is oldest to newest.

    The service must establish currentness using snapshot, check-definition,
    policy, execution, and blob validity before calling this pure function.
    """
    valid = [
        o
        for o in observations
        if (
            o.task_id == contract.task_id
            and o.worktree_id == contract.worktree_id
            and o.contract_revision == contract.contract_revision
            and o.snapshot_id == snapshot_id
            and o.current
        )
    ]
    checks: dict[str, ItemResult] = {}
    manual: dict[str, ItemResult] = {}
    for o in valid:
        if o.provenance == "checkpoint_runner" and o.check_id:
            # A required execution cannot be waived with not_applicable.
            state: State = o.status if o.status != "not_applicable" else "unknown"
            checks[o.check_id] = ItemResult(
                id=o.check_id, status=state, evidence_ids=(o.evidence_id,), reason=o.reason
            )
        if o.provenance == "human_attested" and o.criterion_id and o.reviewer:
            if o.status != "not_applicable" or o.reason.strip():
                manual[o.criterion_id] = ItemResult(
                    id=o.criterion_id,
                    status=o.status,
                    evidence_ids=(o.evidence_id,),
                    reason=o.reason,
                )

    required = tuple(
        checks.get(k, ItemResult(id=k, status="unknown")) for k in contract.required_check_ids
    )
    results: list[ItemResult] = []
    for c in contract.criteria:
        result = ItemResult(id=c.id, status="unknown", reason="Missing authoritative evidence")
        if c.evidence_policy == "mechanical" and c.satisfaction_rule == "approved_checks":
            bound = [checks.get(k, ItemResult(id=k, status="unknown")) for k in c.check_ids]
            result = ItemResult(
                id=c.id,
                status=_state(bound),
                evidence_ids=tuple(e for item in bound for e in item.evidence_ids),
            )
        elif c.evidence_policy == "manual":
            result = manual.get(c.id, result)
        results.append(result)
    authoritative = list(required) + [
        r for c, r in zip(contract.criteria, results, strict=True) if c.required
    ]
    state = _state(authoritative)
    status: Literal["ready", "needs_changes", "unresolved"] = (
        "needs_changes" if state == "fail" else "unresolved" if state == "unknown" else "ready"
    )
    return Completion(
        task_id=contract.task_id,
        contract_revision=contract.contract_revision,
        snapshot_id=snapshot_id,
        status=status,
        criteria=tuple(results),
        required_checks=required,
        next_actions=completion_actions(contract, checks, results),
    )
