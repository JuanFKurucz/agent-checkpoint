# ADR-0008: Native bootstrap and pinned self-adoption

Status: Proposed. Date: 2026-09-27. Implementation: not started.

## Context

The project must be buildable before its own runtime exists and repairable when that runtime fails. Self-development creates a risk that a candidate changes the rules or binary judging its own work. The [revised report](../research/revised-plan-consolidation.md) reinforces the existing adoption roadmap.

## Decision

Start with native interactive Codex, explicit task briefs, short repository guidance, direct checks, and independent review. Add skills only for established recurring workflows. A custom launcher/SDK layer requires a measured need.

Use a separately installed, hash-recorded Checkpoint N to assist candidate N+1. Candidate fixtures use separate state. Promotion needs independent checks and review of policy/test changes; trusted hooks cannot point at a live working-tree build. Shadow mode cannot feed recommendations to the active agent.

Retain a host-level disable route and direct checks that do not depend on Checkpoint. Test migrations against copied state, back up before promotion, and restore an N-compatible state when a binary downgrade alone is insufficient.

## Alternatives

An automatically rebuilt working-tree runtime is convenient but changes the authority mid-task. Building a custom orchestrator first creates a bootstrap dependency. Never using the product internally avoids that dependency but loses useful feedback.

## Consequences

Adoption can begin before a public release while remaining reversible. Version records, separate state, and recovery drills add work. Internal feedback is development evidence, not sufficient proof of general coding-agent improvements.

## Revisit conditions

Add programmatic orchestration only after repeated operating friction or experimental-control needs are measured. Change authority or promotion policy only through a separately reviewed decision.

## Delivery and validation

[HARNESS-02–09](../planning/self-adoption-roadmap.md), TASK-15/16/18, and the [development runbook](../runbooks/development-harness.md). A broken binary/database/provider and an incompatible migration must leave direct verification usable.

