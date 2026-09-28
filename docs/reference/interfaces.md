# Interface reference

Status: internal CLI and all five MCP tools now implemented and exercised in local
tests. See [implemented runtime manual](../guides/internal-runtime.md) for runnable
commands and supported fields. The examples below retain the broader design:
mechanical satisfaction rules other than approved_checks, policy-ID review,
authenticated manual attestation, init/uninstall and hook integration remain
unimplemented. Core result items currently use id/reason, not check_id/reason_code.
Completion adds advisory_findings and next_actions in the shared API; semantic
findings never supply required authority. Native host integration is still unverified.

## Shared conventions

Wire fields use snake_case; repository configuration uses camelCase. Validate both at boundaries. Results are versioned JSON objects. IDs are opaque. Timestamps are UTC. Errors must not expose credentials or raw private input.

All task operations resolve repository/worktree from trusted installation context and verify stored task bindings. Callers cannot redirect a known task to an arbitrary filesystem root.

Mutating requests accept request_id for idempotency. Revisions require expected_contract_revision. Optional expected_snapshot_id is a concurrency precondition; it never replaces the runtime's snapshot calculation.

Caller-supplied mode, provenance, provider credentials, or success claims cannot change effective policy. A versioned schema will reject unknown fields once TASK-04 implements it.

## Five MCP tools

| Tool | Principal input | Result | Effects |
|---|---|---|---|
| checkpoint_start_task | request, criteria, scope, required_check_ids, request_id; optional task_id and expected_contract_revision for revision | task_id, contract_revision, normalized criteria, warnings | Creates or explicitly revises contract |
| checkpoint_route | task_id, kind, phase, optional allowed_candidate_ids | selected IDs, mandatory IDs, abstention reason, decision_id | Records bounded decision and usage |
| checkpoint_run_checks | task_id, check_ids, request_id, optional expected_snapshot_id | run IDs, snapshots, states, evidence IDs | Executes approved checks |
| checkpoint_review | task_id, criterion_ids or policy_ids, evidence_ids | focused findings, native decision references, missing evidence | Records semantic analysis if enabled |
| checkpoint_completion | task_id, optional expected_snapshot_id | readiness, criteria, check states, advisory findings, next actions | Records report from existing evidence/findings; never runs checks or provider calls |

Initially route kind supports skill only. Unsupported kinds return UNSUPPORTED_CAPABILITY. allowed_candidate_ids can narrow the eligible catalog, not add resources or exclude mandated instructions.

Return structuredContent and compact JSON text where supported by the tested client/SDK combination. MCP stdout contains protocol messages only.

## Task example

```json
{
  "request_id": "request_demo_1",
  "request": {"text": "Add input validation and invalid-input tests."},
  "criteria": [
    {
      "id": "AC-001",
      "text": "Malformed input is rejected.",
      "origin": "user",
      "required": true,
      "evidence_policy": "mechanical",
      "satisfaction_rule": "behavior_evidence"
    },
    {
      "id": "AC-002",
      "text": "An automated test exercises malformed input.",
      "origin": "user",
      "required": true,
      "evidence_policy": "manual",
      "satisfaction_rule": "coverage_evidence"
    }
  ],
  "scope": {"exclude": ["deployment"]},
  "required_check_ids": ["typecheck", "test"]
}
```

This is an application payload, not an invented MCP transport envelope. Criterion rules resolve to trusted definitions; arbitrary caller-provided rules cannot replace them. In this example coverage needs an authorized reviewer; a repository with a suitable executable coverage rule can define it as mechanical instead. Required semantic_advisory/informational policies are invalid. A Jev answer is not a reviewer attestation.

## Completion example

Synthetic identifiers and results illustrate an incomplete task.

```json
{
  "schema_version": "1",
  "task_id": "task_demo",
  "contract_revision": 1,
  "snapshot_id": "snapshot_demo_v2",
  "status": "unresolved",
  "required_checks": [
    {"check_id": "typecheck", "status": "pass", "evidence_ids": ["ev_types"]},
    {"check_id": "test", "status": "pass", "evidence_ids": ["ev_tests"]}
  ],
  "criteria": [
    {
      "id": "AC-001",
      "required": true,
      "status": "pass",
      "evidence_ids": ["ev_behavior"]
    },
    {
      "id": "AC-002",
      "required": true,
      "status": "unknown",
      "evidence_ids": [],
      "reason_code": "MISSING_COVERAGE_EVIDENCE"
    }
  ],
  "advisory_findings": [],
  "next_actions": [
    {"type": "gather_evidence", "criterion_id": "AC-002"}
  ],
  "automatic_continuation_eligible": false
}
```

The tests passed, but the report cannot establish required coverage without its declared manual evidence. Even a positive Jev finding would not supply that authority. Missing manual review does not authorize a mechanical stop-hook continuation.

## Error and non-success taxonomy

| Code | Meaning | Recovery |
|---|---|---|
| INVALID_INPUT | Payload fails schema | Correct request |
| TASK_NOT_FOUND / TASK_SCOPE_MISMATCH | Identity is absent or wrong | Select/register correct task |
| REVISION_CONFLICT / SNAPSHOT_CHANGED | Request refers to obsolete state | Refresh; do not replay mutations blindly |
| CHECK_NOT_ALLOWED | Check is not approved | Use configured ID or request policy change |
| POLICY_CHANGED | Governing definition changed | Review and invalidate earlier evidence |
| PROVIDER_DISABLED / PROVIDER_UNAVAILABLE | Remote decision cannot run | Abstain or report unknown |
| BUDGET_EXHAUSTED | Call/time/spend limit reached | Report unresolved; no hidden retry |
| UNSUPPORTED_CAPABILITY | Host/provider cannot do requested operation | Explicit workflow or documented fallback |
| STORAGE_UNAVAILABLE | Durable state cannot be read/written | Recover storage; never invent success |

A nonzero test exit is a recorded failed check, not an invalid MCP request. Transport errors and domain results must remain distinguishable.

## CLI vocabulary

Use --host consistently; older sources used --agent. Target commands are:

```text
agent-checkpoint init --host codex --dry-run
agent-checkpoint init --host codex --apply
agent-checkpoint doctor --json
agent-checkpoint task start --request-file task.md --contract-file contract.json
agent-checkpoint task show task_demo
agent-checkpoint task revise task_demo --contract-file contract.json --expected-revision 1
agent-checkpoint route --task task_demo --kind skill
agent-checkpoint check run --task task_demo typecheck test
agent-checkpoint review --task task_demo
agent-checkpoint complete --task task_demo --json
agent-checkpoint evidence export --task task_demo --format jsonl
agent-checkpoint mcp --stdio
agent-checkpoint uninstall --host codex --dry-run
```

Proposed CLI exit codes: 0 successful operation/ready completion; 2 invalid input/config; 3 needs_changes; 4 unresolved; 5 runtime/provider/storage failure preventing the operation. A recorded failed check uses 3. Doctor with missing required capabilities uses 4. Hook adapters translate internal results to host-specific exit/output rules and must not reuse these codes blindly.

## Provider interface

Use a discriminated union for single_route and criterion_evidence requests/results. Include policy/rubric version, validated candidate IDs, evidence identity, cancellation/deadline, and usage metadata. Do not allow a generic type parameter to assert an arbitrary unvalidated return shape.

Semantic outcomes are selected/none or supported/contradicted/insufficient. Application errors and unavailable results remain distinct from a legitimate none selection. Confidence/probability fields are optional according to primitive; missing confidence is never fabricated.

Review persists semantic findings; completion consumes them without remote side effects. Completion can write an audit report, so describing it as read-only means no repository edits or execution, not zero storage writes or an unconditional MCP read-only annotation.

## Reconciled names from the revised report

Keep `--host`, `request_id`, `contract_revision`, `worktree_id`, `kind`, `selected`, and result `status` as the canonical vocabulary already used here. The report's `--agent`, `idempotency_key`, `revision`, `workspace_id`, `resource_kind`, `selected_ids`, and `readiness` are conceptual equivalents, not a second accepted API. Review continues to accept criterion/policy IDs and evidence IDs. No compatibility aliases are required for an unimplemented API.

The runtime resolves trusted repository/worktree context; caller-provided identity cannot redirect a task. Route supports skill in v1; the report's subagent/check examples remain future extensions. Check-run output will include execution_mode plus before/after snapshot and freshness, as defined in the domain model.

See [configuration](configuration.md) and [semantic ADR](../adr/0003-semantic-decisions.md).

