# Codex integration design

Status: proposed. The official hook documentation was checked on 2026-09-27; installed-host behavior and wire fixtures still require TASK-13 validation.

## Explicit workflow first

The first integration exposes the five [MCP tools](../reference/interfaces.md) over a pinned local STDIO runtime. A workflow skill explains when to register a task, route resources, gather evidence, and request a completion report. The skill is instruction content; installing it alone does not connect Jev or install the runtime.

Respect existing repository instructions, mandatory skills, approval settings, and sandbox controls. Checkpoint advice does not replace these.

## Candidate hook mapping

| Event | Proposed operation | Guard |
|---|---|---|
| SessionStart | Recover session mappings and capabilities | Do not infer task identity solely from cwd |
| UserPromptSubmit | Resolve active task and offer optional routing advice | No automatic registration of conversation/planning turns |
| PostToolUse | Record documented observations and invalidate evidence | Missing visibility is not execution proof |
| SubagentStop | Evaluate explicitly assigned child contract | No parent completion inferred from child stop |
| Stop | Compute readiness and possibly translate a mechanical continuation | Explicit opt-in, verified capability, deduplication, durable cap |
| Interrupt / SessionEnd | Record interrupted work and retain resumable state | Never synthesize success |

PreToolUse interception, permission handling, and general command screening are deferred. Do not parse private transcripts as the primary integration contract.

Compaction/session events may preserve or restore task handles where the tested output contract permits it. Do not assume PostCompact supports context injection merely because it exists. The adapter must validate the appropriate documented context channel for each event.

### Checked lifecycle constraints

Official [hook guidance](https://learn.chatgpt.com/docs/hooks) says MCP hooks use an existing connection: SessionStart can precede server availability, and SessionEnd cannot use MCP-tool hooks. Use a small local helper for early/late bookkeeping. Stop can request continuation; tool visibility is incomplete. These facts do not establish installed-surface parity.

## Continuation behavior

The report describes decision=block for requesting another pass. That exact response must be fixture-tested against the chosen host version before use. Only actionable configured mechanical gaps qualify initially. Semantic-only uncertainty produces a report without forced continuation.

Observe first with zero continuations. A separate mechanical pilot may allow one task-wide continuation after deduplication/restart tests pass. Keep subagent stop reporting-only initially; it cannot create an independent continuation budget outside the parent task cap.

Persist total task passes outside the host process. Session restarts, subagent events, compaction, and repeated stop delivery must not reset or multiply the budget. A last assistant message is a claim, not trusted evidence.

## Distribution and installation

Prefer a tested plugin bundle when it can carry the runtime registration, workflow skill, and optional hooks. Otherwise provide explicit configuration with previewed merges. Packaging remains conditional on current host manifest support. Preserve hook trust review.

Doctor must distinguish desired hooks, installed hooks, trusted hooks when observable, and effective supported events. If trust cannot be observed, report unknown and provide the manual host step.

## Required adapter tests

Malformed/unknown event; no active task; two tasks in one repo; duplicate event; repeated stop; process restart; interruption; no hook trust; provider timeout; disappeared skill; stale evidence; child task mismatch; user cancellation; unsupported output field. Verify no new permission or fabricated success is introduced.

