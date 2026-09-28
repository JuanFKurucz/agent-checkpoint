# Project Garden evaluation loop

Goal activated 2026-09-27 (local date). Six bounded iterations **after** baseline;
none should be counted complete without both website and tool evidence.

## Identities and boundaries

- Website: D:/Programming/project-garden-lab (separate Git workspace).
- Experiment records/state: C:/Users/juanf/AppData/Local/agent-checkpoint/harness/garden-lab.
- Supervisor: independently installed 0.1.2; candidate starts at 0.1.3, advances to 0.1.4.
- Repository baseline task: 35b957317500d92205cb776aa9da3a7c (native MCP).
- Website baseline task: 71d2f341a55deb34b29dc954fdc6fb68 (pinned CLI).
- Website criteria require its own checks; repository checks do not prove website quality.
- Dashboard and new reporting tools are not implemented at goal start.
- No hosted telemetry, deployment, promotion, or additional model authorization.

## Measurements defined before baseline

External driver records UTC start, monotonic subprocess elapsed time, exit status,
and sanitized tool/test responses. Check time is measured by the runner; workflow
time additionally includes process startup, snapshots, routing, and completion.
Direct and harness checks use the same unchanged website files and check commands.
Single paired observations are descriptive, not causal performance conclusions.
Implementation time is elapsed wall time between test-first and final website edits;
it includes reasoning/tool latency and is not pure coding time. Browser verification
and harness checks are separate measured phases. Record retries and their causes.
Unknown metrics stay unknown; costs are not inferred from token counts.

## Iteration protocol

Before each iteration announce one website change and one tool improvement or
diagnostic experiment, with criteria and risks. Register tasks before edits. Route
once where useful, do not create tasks to evade provider limits. Implement website,
observe real friction, reproduce the selected tool issue, then test the candidate
in disposable state. Run full repository gates through pinned MCP after changes;
website gates and completion use pinned CLI consistently. Record browser results.

Randomize website backlog using seed 20260927 and Fisher-Yates with the LCG
`state = (1664525 * state + 1013904223) mod 2^32`, choosing `state mod (i+1)`.
Initial backlog: search-filters, persistence-recovery, keyboard-focus,
undo-delete, sorting, theme-reduced-motion. Record derived order before iteration 1.
Tool changes are selected from observed friction, not randomized.

Derived order: **persistence-recovery → theme-reduced-motion → undo-delete →
sorting → search-filters → keyboard-focus**. Do not reshuffle after observing results.

## Acceptance ledger

- [x] Baseline: direct and pinned workflow, browser screenshots, limitations.
- [x] Iteration 1: paired proposals, evidence, report, next proposals.
- [x] Iteration 2: paired proposals, evidence, report, next proposals.
- [x] Iteration 3: paired proposals, evidence, report, next proposals.
- [x] Iteration 4: paired proposals, evidence, report, next proposals.
- [x] Iteration 5: paired proposals, evidence, report, next proposals.
- [x] Iteration 6: paired proposals, evidence, report, next proposals.
- [x] Local read-only dashboard, metadata traces, Mermaid decision maps.
- [x] Independent candidate package verification; no silent promotion.
- [x] Final assessment, setup/manual recovery, evidence-linked handoff and audit documents.

Final closure requires the passing external manifest described by the
[completion audit](../reports/garden-completion-audit.md). Document existence is
not itself proof that final gates passed. See [final findings](../reports/garden-final-assessment.md).

The prior observability task eff6c7eaca9bd690a4e938dda5566e0a established an
execution-context discrepancy between native and CLI completion and a Jev timeout.
Those are investigation leads, not implemented improvements or verified root causes.
