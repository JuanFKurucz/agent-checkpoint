# Product definition

Status: proposed design.

Agent Checkpoint helps a coding agent use relevant resources and show whether its work satisfies an explicit task. The host continues to edit code, run authorized tools, load instructions, and manage its agents. Checkpoint records contracts and verification, then supplies bounded recommendations and completion reports.

## Users and outcomes

| User | Need | Observable outcome |
|---|---|---|
| Developer using Codex or Claude Code | Less repeated discovery and premature completion | Fewer rework turns and missing requirements |
| Repository maintainer | Consistent project conventions and checks | Criteria linked to current verification evidence |
| Agent researcher | Determine which interventions help | Replayable decisions and paired task experiments |
| Team operating private repositories | Control provider use and local state | Explicit data policy and inspectable records |

The intended advantage is measured across task success, elapsed time, model usage, provider spend, and human review effort. Quality gains may justify extra cost, but that must be reported as a trade-off.

## Scope by stage

| Capability | Initial slice | Later, conditional on evidence |
|---|---|---|
| Task criteria | Explicit registration; origins and revisions | Richer task hierarchies |
| Skill routing | Known candidates, mandatory instructions preserved, explicit none | Large-catalog ranking |
| Verification | Approved check IDs; recorded results; conservative freshness | Measured dependency-based invalidation |
| Completion | Four criterion states; three readiness states | Policy-specific automation |
| Jev | Skill choice and narrow criterion-evidence classification | Context, check, subagent, and model routing |
| Hosts | CLI and explicit MCP; Codex hook pilot | Claude native hooks and wider packaging |
| Review | Focused criterion review | Repository-specific architecture rubrics |
| Distribution | One local runtime | Tested host plugins |
| CI | Independent deterministic verification | Optional separated semantic evaluation |

Check selection may add checks or recommend optional ones. It must never silently omit a required repository check. A user-requested skill or host-mandated instruction remains mandatory regardless of a routing recommendation.

## Exclusions from the first release

General orchestration, automatic architecture redesign, unrestricted command execution, universal quality scores, semantic release blocking, hosted accounts, and a remote control plane are deferred. Model routing requires a separate experiment and a host mechanism that actually supports the change.

## Requirements

| ID | Requirement | Design location |
|---|---|---|
| REQ-01 | Same core behavior through CLI, MCP, and hooks | [Overview](architecture/overview.md) |
| REQ-02 | Every operation binds to an explicit task and worktree | [Contracts](architecture/contracts-and-evidence.md) |
| REQ-03 | Missing, stale, claimed-only, or semantic-only evidence cannot pass a required criterion | [Evidence](architecture/contracts-and-evidence.md) |
| REQ-04 | Jev selects only eligible resources and cannot grant permissions | [Provider ADR](adr/0003-semantic-decisions.md) |
| REQ-05 | Remote evaluation defaults off; runner does not receive provider credentials | [Security](architecture/security-and-privacy.md) |
| REQ-06 | Continuations are explicit, bounded, durable, and deduplicated | [Workflows](architecture/workflows.md) |
| REQ-07 | Installation preserves existing configuration and host trust | [Usage](guides/usage.md) |
| REQ-08 | Quality, total cost, and total latency claims require comparative evidence | [Evaluation](research/evaluation.md) |

## First demonstration

Use a disposable API repository with a service-layer convention. Request an endpoint with invalid-input validation and tests. Register separate criteria for behavior, test coverage, and required check execution. Route to a real testing skill, implement, then demonstrate that a green test command alone does not prove that the required negative-path test exists. Add the missing test, rerun against the new snapshot, and produce a criterion-by-criterion report.

Each required criterion needs an explicit mechanical or authorized manual satisfaction rule; a positive Jev finding alone cannot establish coverage. Repeat with provider outage, a changed check definition, duplicate stop events, and two worktrees. The baseline and deterministic-only conditions must run the same tasks.

