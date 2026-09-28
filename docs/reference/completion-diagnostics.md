# Completion diagnostics: candidate 0.1.3 / response schema 2

This documents the candidate, not the still-active pinned 0.1.2 supervisor.
`task`, configuration and storage remain schema 1. Completion output is schema 2;
clients expecting schema 1 must branch on version or stay on the old artifact.
Old completion records are retained without rewriting or importing their readiness.

## Meaning and consumer

`ready` means the currently declared required evidence rules pass. It does not prove
semantic coverage or authenticate the criteria's author. `needs_changes` means a
required failure; `unresolved` means required evidence is unknown without a failure.
All actions are diagnostics for the host/operator. Completion runs neither checks
nor providers. It never executes repairs or decides whether reruns are safe.

| kind | Typical reason_code | Consumer action |
|---|---|---|
| run_check | EVIDENCE_MISSING | Inspect declared check and obtain authorized execution |
| inspect_check_output | CHECK_FAILED | Inspect the referenced run output and repair within task scope |
| refresh_stale_evidence | EVIDENCE_STALE / INPUT_CHANGED | Investigate changed inputs; authorize a fresh run with a new request ID |
| reconcile_interrupted_run | INTERRUPTED_OR_RUNNING / INTERRUPTED | Confirm process lifetime first; follow recovery procedure; never blindly replay |
| inspect_check_unavailable | EVIDENCE_UNAVAILABLE / TIMEOUT / other bounded runner codes | Diagnose missing/corrupt output, timeout, execution or isolation limitation |
| request_manual_attestation | MANUAL_ATTESTATION_UNAVAILABLE | Report the missing authenticated surface; do not fabricate a human approval |
| resolve_contract_gap | EVIDENCE_BINDING_MISSING / UNSUPPORTED_EVIDENCE_POLICY | Obtain an appropriate evidence obligation; do not invent an unrelated test |

Check actions are deduplicated per declared required/bound check. They reference
all required criteria bound to that check. Optional unknown criteria do not create
required work. A ready response has no required actions. Advice stays separate.

```json
{
  "kind": "refresh_stale_evidence",
  "reason_code": "EVIDENCE_STALE",
  "priority": "required",
  "criterion_ids": ["behavior"],
  "check_ids": ["tests"],
  "evidence_ids": ["previous-run-id"],
  "authorized_execution": false
}
```

No command, provider-selection, replay_safe or arbitrary action field is accepted.
automatic_continuation_eligible remains false. The host's existing permissions and
the reviewed check configuration remain authoritative. Stale is an evidence reason,
not a new check status; domain states stay pass/fail/unknown/not_applicable.

## Validation and compatibility

The shared runtime validates assembled completion output against CompletionResponse,
including typed advisory findings constrained to semantic_advisory authority. MCP
validates again at its boundary and advertises a success/error union with object
root. Invalid output returns sanitized INVALID_COMPLETION_OUTPUT, not its raw data.
Other four tools still have generic output schemas; strengthening them is ADJ-06.

This uses the existing [MCP structured result contract](https://modelcontextprotocol.io/specification/2025-11-25/server/tools),
not a protocol/SDK upgrade. Error results remain distinct from domain non-ready
results. CLI and MCP invoke the same completion code. No database schema migration
or active-runtime switch accompanies this candidate change.

## Known limits

Generic bindings are still authored through the current task API. This slice does
not authenticate origin, add test/assertion receipts, implement manual attestation,
reconcile pending runs automatically, or produce a repair planner. A request for
manual evidence is a diagnostic of an unsupported surface, not an available tool.
