# ADR-0007: Measure the intervention and the provider separately

Status: Proposed. Date: 2026-09-27. Implementation: not started.

## Context

Vendor decision benchmarks and typed responses do not demonstrate better coding outcomes. Only successful tasks can hide spending on failed attempts. See the [research synthesis](../research/synthesis.md).

## Decision

Compare baseline, deterministic Checkpoint, heuristic routing, agent self-judgment, and Jev under matched tasks. Pre-register thresholds and analyze success, false-ready, full spend, and wall time. Keep failed attempts in accounting.

## Alternatives

A Jev-only demo cannot isolate product value. Accuracy without abstention coverage masks selective failures. Tuning on final evaluation data invalidates release evidence.

## Consequences

Research becomes slower than a showcase but supports defensible decisions, including shipping without Jev. Sample size and uncertainty may prevent strong claims from pilots.

## Revisit conditions

Promote automation per decision/rubric/host only after adequate data. A failed gate can narrow scope rather than force abandonment of the evidence core.

## Delivery and validation

[Backlog](../planning/backlog.md): TASK-10, TASK-18, TASK-19. Completion requires their stated acceptance evidence. Related decisions: [ADR index](README.md).

