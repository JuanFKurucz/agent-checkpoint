# Architecture decision records

ADRs 0001–0008 preserve the historical proposed design. Their original status text
is not current implementation status; see [status](../status.md). New decisions
below distinguish accepted scoped changes from still-proposed authority work.

| ADR | Choice | Status |
|---|---|---|
| [0001](0001-runtime-and-adapters.md) | One runtime with thin adapters; Python-first evaluation | Proposed |
| [0002](0002-state-and-freshness.md) | SQLite and blobs outside the checkout | Proposed |
| [0003](0003-semantic-decisions.md) | Bounded replaceable semantics with explicit uncertainty | Proposed |
| [0004](0004-contracts-and-authority.md) | Explicit task contracts and separate readiness from enforcement | Proposed |
| [0005](0005-hosts-and-distribution.md) | Explicit MCP first and capability-gated native automation | Proposed |
| [0006](0006-trust-and-ci.md) | Remote opt-in and independent verification | Proposed |
| [0007](0007-evaluation-and-release.md) | Measure the intervention and the provider separately | Proposed |
| [0008](0008-self-adoption.md) | Native bootstrap and pinned self-adoption | Proposed |
| [0009](0009-diagnostics-and-review-policy.md) | Non-executable diagnostics and opt-in review | Accepted; candidate 0.1.3 |
| [0010](0010-authoritative-evidence-bindings.md) | Authenticated evidence obligations and migration design | Proposed |

Each record includes context, decision, alternatives, consequences, revisit conditions, and linked work. Accept a record explicitly during design review; attach implementation evidence separately. Once accepted, preserve its historical rationale and use a new ADR to supersede it.

Use the [template](template.md) for new consequential decisions. Routine implementation details can remain in the backlog.

