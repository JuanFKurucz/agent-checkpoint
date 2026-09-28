# ADR-0003: Bounded replaceable semantics with explicit uncertainty

Status: Proposed. Date: 2026-09-27. Implementation: not started.

## Context

Jev's incremental value is unproven. Broad code-quality judgments conflate independent requirements and confidence can be misread as correctness. See the [research synthesis](../research/synthesis.md).

## Decision

Implement a provider-independent discriminated contract. Begin with skill choice and criterion-evidence classification. Preserve native optional probability fields. Use an explicit none candidate and application-owned unknown. Keep deterministic gates authoritative.

Use `jev-1.13.0` as the initial controlled-evaluation pin, subject to an authorized API smoke test; reject silent model substitution and do not use moving aliases in reproducibility-sensitive runs. Required criteria need mechanical/manual authority. A semantic supported/contradicted/insufficient finding is advisory and cannot alone pass or fail a required criterion. See [model verification](../research/sources.md).

## Alternatives

Hard-wiring Jev prevents meaningful ablation. Asking the coding agent itself remains a benchmark condition. Universal quality scores have no defensible initial threshold.

## Consequences

Supports mocks, offline tests, and simpler alternatives. Rubric design, privacy, and coding-domain calibration remain necessary. No guaranteed speed or cost improvement follows.

## Revisit conditions

Add decision kinds separately when held-out and live-task evidence justify them. Semantic blocking requires a new ADR and policy-specific trial.

## Delivery and validation

[Backlog](../planning/backlog.md): TASK-08, TASK-09, TASK-10. Completion requires their stated acceptance evidence. Related decisions: [ADR index](README.md).

