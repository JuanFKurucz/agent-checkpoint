# ADR-0009: Non-executable diagnostics and opt-in semantic review

Status: Accepted for the bounded adjustment slice. Date: 2026-09-27.
Candidate implementation: 0.1.3. Active pinned runtime: unchanged 0.1.2.

## Context

The [new report](../research/harness-validation-consolidation.md) identifies two
practical gaps: generic next_actions do not distinguish repair from recovery, and
status-only semantic review has not shown value. Actual Jev abstention is not an
error to eliminate by repeated calls. Required evidence remains deterministic.

## Decision

- Remove routine review from repository instructions; retain explicit experiments
  and live advisory routing within the existing Gateway/data/budget restrictions.
- Generate typed diagnostics from the same reduced evidence that determines
  completion. Include declared check/criterion/run references and bounded reason
  codes, never command strings or arbitrary model-generated actions.
- authorized_execution and automatic_continuation_eligible remain false. Do not
  label a suggested rerun replay-safe or perform it implicitly.
- Bump completion response schema to 2. Contract/config/SQLite schema stay 1.
  Validate the assembled completion response in the shared runtime and MCP output
  boundary; advertise detailed completion success/error schemas.
- Preserve pinned 0.1.2 as supervisor. Build/test candidate independently before a
  separate promotion. Do not overwrite prior reports or reinterpret their schema.

## Alternatives and consequences

Keeping generic diagnostics is cheaper but leaves every consumer to infer recovery.
Model-generated repair plans add cost and authority ambiguity. A new executor is
out of scope. Versioning the output costs consumer migration, but avoids disguising
the changed action shape as the old contract. Other four output schemas remain
generic and need their own discriminated pending/success/error work.

Diagnostics are not complete remediation instructions. Missing manual evidence
still needs an unimplemented authenticated surface. None of this proves that a
criterion's selected tests actually cover its semantics.

## Validation and reversal

Offline tests must distinguish missing, failed, stale, corrupt/unavailable and
unfinished evidence; reject executable/authority fields; preserve readiness; and
exercise schema-valid MCP output plus sanitized invalid-output rejection. No live
Jev call is required for those tests. Revert the candidate without changing active
N/state if compatibility fails. Review policy can be revisited after a held-out
benchmark with a separately approved minimal evidence packet.

Related: ADR-0003, ADR-0004, ADR-0005, ADR-0008. This decision refines operational
policy and diagnostics; it does not accept every historical proposal in those ADRs.
