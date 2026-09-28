"""Shared services. Adapters supply configured checks, never arbitrary tool argv."""

from pathlib import Path
from typing import Literal
from uuid import uuid4

from pydantic import Field

from agent_checkpoint.contracts import (
    Completion,
    ContextFingerprints,
    Contract,
    Criterion,
    Observation,
    Record,
    StaleDiagnostic,
    State,
    reduce_completion,
)
from agent_checkpoint.runner import CheckDefinition, check_context, context_fingerprints, run_check
from agent_checkpoint.snapshot import SnapshotError, capture, worktree_identity
from agent_checkpoint.storage import Store, StoreError, digest


class CheckEvent(Record):
    run_id: str
    check_id: str
    contract_revision: int = Field(ge=1)
    phase: Literal["started", "finished"] = "started"
    status: State = "unknown"
    reason: str = "INTERRUPTED_OR_RUNNING"
    snapshot_id: str = ""
    generation: str = ""
    output_digest: str = ""
    definition_digest: str = ""
    exit_code: int | None = None
    duration_seconds: float = 0
    execution_mode: Literal["working_tree", "isolated_snapshot"] = "working_tree"
    context_fingerprints: ContextFingerprints | None = None


def latest_checks(events: list[CheckEvent]) -> dict[str, CheckEvent]:
    """Use start order, never finish order; any unfinished run prevents a pass."""
    runs: dict[str, CheckEvent] = {}
    for event in events:
        previous = runs.get(event.run_id)
        if event.phase == "started":
            if previous is not None:
                raise StoreError("DUPLICATE_RUN_START")
        elif previous is None:
            raise StoreError("RUN_WITHOUT_START")
        elif (
            previous.phase != "started"
            or previous.check_id != event.check_id
            or previous.contract_revision != event.contract_revision
        ):
            raise StoreError("INVALID_RUN_TRANSITION")
        runs[event.run_id] = event
    latest = {event.check_id: event for event in runs.values()}
    for event in runs.values():
        if event.phase == "started":
            latest[event.check_id] = event.model_copy(
                update={"status": "unknown", "output_digest": ""}
            )
    return latest


class Service:
    def __init__(
        self,
        root: Path,
        state: Path,
        checks: dict[str, CheckDefinition],
        required_check_ids: tuple[str, ...] = (),
        policy_context: object = None,
    ) -> None:
        self.root = root.resolve()
        if state.resolve().is_relative_to(self.root):
            raise ValueError("STATE_INSIDE_WORKSPACE")
        self.worktree_id = worktree_identity(self.root)
        self.store = Store(state)
        self.checks = checks.copy()
        self.required_check_ids = required_check_ids
        if not set(required_check_ids) <= checks.keys():
            raise ValueError("REQUIRED_CHECK_NOT_DEFINED")
        self.policy_digest = digest(
            {
                "checks": {k: v.model_dump() for k, v in checks.items()},
                "required": required_check_ids,
                "context": policy_context,
            }
        )

    def start_task(
        self,
        request: str,
        criteria: list[Criterion],
        required_check_ids: list[str],
        request_id: str,
        *,
        task_id: str | None = None,
        expected_contract_revision: int | None = None,
        scope_exclude: tuple[str, ...] = (),
    ) -> Contract:
        required = tuple(dict.fromkeys((*self.required_check_ids, *required_check_ids)))
        wanted = set(required) | {k for c in criteria for k in c.check_ids}
        if not wanted <= self.checks.keys():
            raise StoreError("CHECK_NOT_ALLOWED")
        if any(
            c.evidence_policy == "mechanical" and c.satisfaction_rule != "approved_checks"
            for c in criteria
        ):
            raise StoreError("UNSUPPORTED_SATISFACTION_RULE")
        contract = Contract(
            task_id=task_id
            or digest({"worktree": self.worktree_id, "request_id": request_id})[:32],
            worktree_id=self.worktree_id,
            request=request,
            criteria=tuple(criteria),
            required_check_ids=required,
            policy_digest=self.policy_digest,
            contract_revision=(expected_contract_revision + 1) if expected_contract_revision else 1,
            scope_exclude=scope_exclude,
        )
        return self.store.save_contract(contract, request_id, expected_contract_revision)

    def task(self, task_id: str) -> Contract:
        task = self.store.get_contract(task_id, self.worktree_id)
        if task.policy_digest != self.policy_digest:
            raise StoreError("POLICY_CHANGED")
        return task

    def run_checks(self, task_id: str, check_ids: list[str], request_id: str) -> dict[str, object]:
        contract = self.task(task_id)
        if not check_ids or not set(check_ids) <= self.checks.keys():
            raise StoreError("CHECK_NOT_ALLOWED")
        if len(set(check_ids)) != len(check_ids):
            raise StoreError("DUPLICATE_CHECK_ID")
        scope = "check:" + task_id
        replay = self.store.claim_request(
            scope,
            request_id,
            {
                "check_ids": check_ids,
                "revision": contract.contract_revision,
            },
        )
        if replay is not None:
            return replay
        runs: list[dict[str, object]] = []
        for check_id in check_ids:
            definition = self.checks[check_id]
            event = CheckEvent(
                run_id=str(uuid4()),
                check_id=check_id,
                contract_revision=contract.contract_revision,
                execution_mode=definition.execution_mode,
            )
            self.store.append_event(task_id, self.worktree_id, "check", event.model_dump())
            try:
                outcome = run_check(self.root, definition)
                output_digest = self.store.put_blob(outcome.output)
                event = CheckEvent(
                    run_id=event.run_id,
                    check_id=check_id,
                    contract_revision=contract.contract_revision,
                    phase="finished",
                    status=outcome.status,
                    reason=outcome.reason,
                    snapshot_id=outcome.before.id,
                    generation=outcome.before.generation,
                    output_digest=output_digest,
                    definition_digest=outcome.definition_digest,
                    exit_code=outcome.exit_code,
                    duration_seconds=outcome.duration_seconds,
                    execution_mode=definition.execution_mode,
                    context_fingerprints=outcome.context_fingerprints,
                )
            except (SnapshotError, ValueError, OSError):
                event = event.model_copy(
                    update={"phase": "finished", "reason": "CHECK_UNAVAILABLE"}
                )
            self.store.append_event(task_id, self.worktree_id, "check", event.model_dump())
            runs.append(event.model_dump())
        response: dict[str, object] = {"status": "completed", "task_id": task_id, "runs": runs}
        self.store.finish_request(scope, request_id, response)
        return response

    def complete(self, task_id: str) -> Completion:
        guard = self.store.report_guard(task_id, self.worktree_id)
        contract = self.task(task_id)
        report_snapshot = capture(self.root, context=contract.model_dump())
        events = self.store.events(task_id, self.worktree_id, "check")
        check_events: list[CheckEvent] = []
        for payload in events:
            event = CheckEvent.model_validate(payload)
            if event.contract_revision == contract.contract_revision:
                check_events.append(event)
        latest = latest_checks(check_events)
        observations: list[Observation] = []
        diagnostics: list[StaleDiagnostic] = []
        for check_id, event in latest.items():
            state: State = "unknown"
            reason = event.reason or "CHECK_UNAVAILABLE"
            definition = self.checks.get(check_id)
            if definition is not None and event.output_digest:
                try:
                    context = check_context(definition, self.root)
                    current = capture(self.root, context=context)
                    self.store.get_blob(event.output_digest)
                    if (
                        current.id == event.snapshot_id
                        and current.generation == event.generation
                        and digest(definition.model_dump()) == event.definition_digest
                    ):
                        state, reason = event.status, event.reason
                    else:
                        reason = "EVIDENCE_STALE"
                        prior = event.context_fingerprints
                        fingerprints = context_fingerprints(context)
                        changed = (
                            [
                                key
                                for key in ContextFingerprints.model_fields
                                if getattr(prior, key) != getattr(fingerprints, key)
                            ]
                            if prior is not None and fingerprints is not None
                            else []
                        )
                        diagnostics.append(
                            StaleDiagnostic.model_validate(
                                {
                                    "check_id": check_id,
                                    "evidence_id": event.run_id,
                                    "context_comparison": "unavailable"
                                    if prior is None or fingerprints is None
                                    else "changed"
                                    if changed
                                    else "unchanged",
                                    "changed_components": tuple(changed),
                                    "workspace_generation_changed": current.generation
                                    != event.generation,
                                }
                            )
                        )
                except (SnapshotError, StoreError):
                    reason = "EVIDENCE_UNAVAILABLE"
            observations.append(
                Observation(
                    evidence_id=event.run_id,
                    task_id=task_id,
                    worktree_id=self.worktree_id,
                    contract_revision=contract.contract_revision,
                    snapshot_id=report_snapshot.id,
                    check_id=check_id,
                    status=state,
                    provenance="checkpoint_runner",
                    current=True,
                    reason=reason,
                )
            )
        final_snapshot = capture(self.root, context=contract.model_dump())
        if (
            final_snapshot.id != report_snapshot.id
            or final_snapshot.generation != report_snapshot.generation
        ):
            observations = []
            diagnostics = []
        report = reduce_completion(contract, final_snapshot.id, observations)
        report = report.model_copy(update={"stale_diagnostics": tuple(diagnostics)})
        self.store.publish_report(task_id, self.worktree_id, guard, report.model_dump())
        return report
