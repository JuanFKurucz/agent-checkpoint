# Post-research adjustment roadmap

Current queue, 2026-09-27. Supersedes the old bootstrap-first next-step sequence,
not the historical TASK/HARNESS acceptance requirements. No issue/PR was created.
Source: [reconciled report](../research/harness-validation-consolidation.md).

| ID | State | Work package | Existing traceability | Exit evidence |
|---|---|---|---|---|
| ADJ-01 | Candidate implemented; promotion deferred | Current status/reconciliation, opt-in review, typed diagnostics and strict completion schema | TASK-07/12; HARNESS-06 | Focused/full offline tests, CLI/MCP fixture, unchanged active N, documented schema break |
| ADJ-02 | Next design slice | Authoritative criterion/evidence approval and migration contract | TASK-04/07; ADR-0010 | Threat model and independently approved bindings; v1/v2 and false-coverage fixtures |
| ADJ-03 | Planned | Formal execution profile and cross-transport identity fixtures | TASK-06; HARNESS-06 | Same declared inputs match; relevant changes stale; undeclared harmless inputs do not; edit/revert safeguards retained |
| ADJ-04 | Planned | Independent direct verification/provenance/promotion package | TASK-15/16; HARNESS-05 | Clean wheel install and direct checks; source/lock/artifact identity; rollback with compatible state |
| ADJ-05 | Planned | Profile overhead, then reviewed change-aware verification | TASK-06/10/18; HARNESS-03 | Per-boundary timing; randomized warm/cold trials; requirements expand with scope, never shrink to pass |
| ADJ-06 | Planned | Complete output contracts and compatibility/replay/cancellation fixtures | TASK-11/12 | All five pending/success/error shapes validated; no duplicate effects or raw error leakage |
| ADJ-07 | Planned | Jev routing/abstention evaluation; optional review evidence study | TASK-09/10; HARNESS-07 | Held-out labels, heuristic/host/Jev comparisons; unknown billing distinct from zero; negative result acceptable |
| ADJ-08 | Planned | Native Codex acceptance, then separate observe-only hooks | TASK-13/14; HARNESS-08 | Native host events/tool calls and disable/restart fixtures; no implicit checks/Jev/continuation |
| ADJ-09 | Deferred | Installer/credential boundary, Claude and whole-task release pilot | TASK-16/17/18/19; HARNESS-09 | Owned reversible config edits; separate host tests; independent outcomes and recovery |

## Scope and dependency notes

ADJ-01 is a useful first slice, not completion of the report's three-part core
package. ADJ-02 and ADJ-03 should converge before changing evidence authority or
cache policy. ADJ-04 precedes stronger adoption/promotion. Read-only native Codex
acceptance can proceed independently; hooks wait for correctness and recovery.
Credential migration and external host/CI changes require concrete operator choices.

The active 0.1.2 runtime remains pinned. Candidate 0.1.3 completion schema 2 is not
visible through that runtime until separately validated promotion. Do not point
the active supervisor at editable candidate code to see new fields sooner.

## First next work package: ADJ-02 design and negative fixtures

1. Inspect current Contract/Criterion/save_contract and approved-check bindings.
2. Define who can authorize a user/repository obligation versus agent interpretation;
   specify approval producer and request/policy digest roles without assuming hashes
   authenticate a human. Resolve operator UX before adding writable authority fields.
3. Specify v1 compatibility, opt-in v2 binding schema and migration/rollback rules.
4. Add fixtures: generic green suite with no authorized binding; wrong/missing test;
   attempted criterion weakening; forged origin; manual pass plus required failure.
5. Produce a reviewed ADR update and implementation-sized test plan. Do not change
   active policy, credentials, state or host configuration as part of this design.

## Evaluation and performance gates

Retain the historical 18-trial negative overhead result. The report proposes 70%
less median overhead and sub-second p95 bookkeeping, but neither threshold is
adopted as achieved or justified yet. First measure process, config, database,
enumeration, hashing, executable identity, runner and report boundaries separately.
Pre-register any useful-effect threshold after a variance pilot. Charge maintenance,
human effort and integration overhead; unavailable billing remains null.

Remote evaluation stays Gateway-only, without retries or unapproved evidence.
Review remains opt-in; do not add model calls to demonstrate activity. Richer
evidence, telemetry or another provider requires a new explicit data decision.
