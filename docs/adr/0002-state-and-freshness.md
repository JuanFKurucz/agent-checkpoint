# ADR-0002: SQLite and blobs outside the checkout

Status: Proposed. Date: 2026-09-27. Implementation: not started.

## Context

Hooks and MCP processes can restart independently. Repository-local mutable evidence changes the workspace being evaluated and is easy to edit accidentally. See the [research synthesis](../research/synthesis.md).

## Decision

Persist metadata in SQLite and bounded output in content-addressed blobs under OS user data. Scope every record to repository, worktree, task, revision, and snapshot. Start with conservative whole-relevant-workspace invalidation.

Distinguish working_tree verification from isolated_snapshot execution. The former cannot prove absence of transient concurrent changes; critical promotion checks require controlled materialized inputs. Record execution mode and refuse silent fallback when the stronger mode is required.

## Alternatives

Repository JSON is useful for configuration but poor for concurrent runtime state. JSONL is an export format. Remote databases add unnecessary service and privacy requirements.

## Consequences

Transactions and recovery become tractable; migrations, locks, retention, and crash consistency need work. This placement is not protection against a same-user attacker.

## Revisit conditions

Revisit storage after measured contention or cross-machine requirements. Refine invalidation only after correctness and overhead measurements.

## Delivery and validation

[Backlog](../planning/backlog.md): TASK-05, TASK-06, TASK-07. Completion requires their stated acceptance evidence. Related decisions: [ADR index](README.md).

