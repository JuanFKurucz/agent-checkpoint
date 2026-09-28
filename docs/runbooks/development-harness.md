# Native Codex development harness

Status: proposed operating manual. No AGENTS.md, project scripts, skills, launcher, or host integration has been installed by this consolidation. Use the [first work package](../planning/next-steps.md) to implement the bootstrap.

## Day-one operating loop

1. Open the intended repository/worktree in native Codex and identify the task.
2. Use a [task brief](../tasks/TEMPLATE.md) with original requirements, scope, and observable acceptance checks.
3. Read the relevant ADRs and only applicable skills. Add a repository skill later when a repeated workflow warrants it.
4. Make a focused change. Use one primary agent; delegate only with authorization and a separable assignment.
5. Run the repository's actual direct commands, once created and recorded in the [verification inventory](../verification.md).
6. Review the diff and evidence separately from the implementing narrative. Record unresolved requirements honestly.
7. Leave a [handoff](../handoffs/TEMPLATE.md) for interruption or transfer.

A docs-only task needs relevant document checks, not invented npm scripts. A coding task needs real commands created by the scaffold. A reviewer must return concrete findings/evidence; agreement alone is not validation.

## Instruction and state placement

| Artifact | Content |
|---|---|
| Future root AGENTS.md | Short durable invariants and pointers; no fake commands |
| ADRs | Technical choices, alternatives, revisit conditions |
| Task brief | User requirements, repository requirements, scope, acceptance evidence |
| Handoff | Current state, observed results, unresolved work, next action |
| Optional skill | A proven repetitive workflow with clear trigger |
| External runtime state | Task/evidence records once Checkpoint exists |
| Verification inventory | Commands actually available and validated |

Native interactive Codex is the default. Investigate a thin non-interactive launcher if a ten-task pilot repeatedly loses measurement/handoff data or repeats the same machine-readable operation. The report suggests over 20% incomplete records or repetition in at least five tasks as provisional triggers, not validated thresholds. Use a programmatic SDK only for a demonstrated control requirement.

See the [official non-interactive documentation](https://learn.chatgpt.com/docs/non-interactive-mode) before choosing machine-readable commands and telemetry. Missing billing or usage data stays unavailable, not an invented estimate.

## Introducing Checkpoint

Follow H0–H5 in the [self-adoption roadmap](../planning/self-adoption-roadmap.md). Adopt deterministic shadow reports, then explicit advice. Jev and hooks are separate experiments. Every active runtime and policy revision must be identifiable.

Hook observation and mechanical continuation are separate stages. Observation cannot inject advice into the active agent while being counted as a non-intervening condition. The first mechanical pilot allows one task-wide pass only after its fixtures succeed.

## Recovery and disablement

Disable the specific Checkpoint integration through supported host configuration when possible. Official [hook guidance](https://learn.chatgpt.com/docs/hooks) documents the broader configuration escape:

```toml
[features]
hooks = false
```

This affects hooks broadly, not just Checkpoint; respect managed settings and preserve unrelated configuration. It is documented syntax, not a change applied here. Remove/disable the toolkit-owned MCP/plugin registration separately if necessary, using an ownership record once installation exists.

Recovery must work when the runtime, database, or provider is unavailable. Continue direct checks and manual evidence records. Do not erase state to make the system appear healthy.

For migration failures, restore the previous artifact and its consistent compatible state. Preserve post-migration records separately and disclose unavailable evidence. Candidate tests must not touch the active N database.

## Before promoting N+1

Confirm artifact hash/source identity, separate candidate state, independent checks, review of changed policies/tests, host compatibility, migration-on-copy results, and a tested rollback. A ready response from N+1 alone is never promotion evidence.

