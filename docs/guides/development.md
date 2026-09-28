# Developer guide

Current implementation: Python 3.13 with pyproject.toml and uv.lock. Use AGENTS.md's
direct commands, the [active harness](active-harness.md), and the
[Project Garden operating guide](garden-lab-operations.md). Node.js is needed only
for the development suite's offline dashboard DOM regression. Candidate 0.1.9 is
validated separately; active self-supervision stays pinned to 0.1.2.

## How this project will use its own tooling

Follow the [harness and self-adoption roadmap](../planning/self-adoption-roadmap.md): native Codex and direct checks first, then a separately installed and pinned Checkpoint build in shadow/advisory mode. A candidate source checkout is not the trusted installed runtime. Keep verification and the manual disable path usable when Checkpoint is broken.

The research response is [consolidated](../research/revised-plan-consolidation.md).
The [bootstrap runbook](../runbooks/development-harness.md),
[task template](../tasks/TEMPLATE.md), [handoff template](../handoffs/TEMPLATE.md),
and [verification inventory](../verification.md) retain broader proposed work.
The active harness guide describes what is actually configured. The original
[research prompt](../research/prompts/codex-harness-deep-research.md) is historical.

## Start at the next unfinished task

Use [next steps](../planning/next-steps.md) and the dependency table in the [backlog](../planning/backlog.md). New work should state its task ID, affected contract/ADR, acceptance check, and validation output. No GitHub issues or implementation commits have been created by this documentation pass.

## Implementation boundaries

Keep core services independent of host and protocol types. Inject provider, storage, runner, clock, and catalog interfaces. Keep external schema validation at every boundary. Use immutable domain records for revisions and execution observations.

Fixture tests must not need provider credentials. A mock should cover none, insufficient evidence, malformed response, timeout, and budget exhaustion, not merely a successful choice. A real provider implementation should be replaceable without changing completion aggregation.

## Verification layers

| Layer | What to prove |
|---|---|
| Unit | Aggregation precedence, identity checks, candidate eligibility, budget calculations |
| Property/invariant | Unknown never silently becomes pass; adding a failed required check cannot improve readiness |
| Integration | SQLite transactions, restart recovery, blob integrity, runner cancellation, snapshot invalidation |
| Adapter contract | Same domain result through CLI/MCP; malformed host payloads and repeated events |
| End-to-end | Incomplete feature, correction, current evidence, final report |
| Evaluation | Intervention improves independently judged outcomes under the frozen protocol |

Use small disposable repositories for staged, unstaged, untracked, renamed, deleted, ignored-input, and concurrent-worktree cases. Include edits during checks and edit/revert races. Windows path/argv/process behavior is a required target because the current workspace uses Windows.

## Documentation acceptance

New commands need actual help output and runnable examples before usage pages become release manuals. Config defaults and field names must match schemas. A host enters supported status only when its compatibility record contains passing contract and smoke tests.

For each completed task, link test output or an artifact, update only its checkbox, and record unresolved limitations. Do not mark a milestone done because its documentation exists.

## Release candidate checklist

- [ ] Exact dependency/runtime and host matrix recorded.
- [ ] Schemas and docs agree; fixture payloads validate.
- [ ] Required evidence invariants pass.
- [ ] Credential and isolation boundaries tested.
- [ ] Installation is idempotent and uninstall preserves unrelated configuration.
- [ ] Independent CI reruns required checks.
- [ ] Evaluation claims include uncertainty and failed-attempt costs.
- [ ] Native continuations remain opt-in and bounded.
- [ ] Usage examples run on the built artifact.

