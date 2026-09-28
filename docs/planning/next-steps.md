# Next steps

Status: historical bootstrap queue, superseded for current sequencing by the
[post-research adjustment roadmap](post-research-adjustments.md). The Python runtime
exists; do not recreate its skeleton. See [current status](../status.md). ADJ-01 is
the bounded first candidate change; ADJ-02 authority/binding design is next.

## Prepare the Codex development setup

The requested research has been received and [consolidated](../research/revised-plan-consolidation.md). Use the [development runbook](../runbooks/development-harness.md), [task](../tasks/TEMPLATE.md) and [handoff](../handoffs/TEMPLATE.md) templates to prepare the native Codex bootstrap. The [self-adoption roadmap](self-adoption-roadmap.md) defines independent verification, version pinning, and recovery requirements. Exact installed-host behavior remains to be tested.

This research can proceed alongside the foundation work below. Bootstrap development must work without Checkpoint, Jev, or our future hooks. Do not make building the first runtime depend on already having that runtime installed.

## First work package

Complete TASK-01 and TASK-02: perform the [Python-first runtime/provider comparison](../research/python-langchain-assessment.md), verify exact SDK/host capabilities, and define allowed provider data. Use synthetic examples for early probes; private repository access is unnecessary. Deliver a dated runtime choice, compatibility record, and data-boundary note.

Then TASK-03 creates one package skeleton in the selected language and pins tested dependencies; Python is the preferred candidate, not yet an implemented stack. TASK-04 turns the contracts into executable schemas and fixtures, including evidence_policy and a pure deterministic readiness reducer. Prepare active repository instructions under HARNESS-02 only as part of that implementation work. Record real direct commands in the [verification inventory](../verification.md) after they exist and run successfully. Do not copy report import snippets without an import/build/host test.

The immediate package is native bootstrap plus schemas/reducer/mock fixtures, not a Jev or MCP deployment. An early reducer consumes supplied domain records; TASK-07 later adds durable evidence loading, current snapshot validation, and stored completion reports.

## First useful implementation

Build TASK-05 through TASK-08 with no provider credentials: state store, snapshots/runner, completion aggregation, and mock routing. Demonstrate that an old green test run becomes stale after a relevant edit and that an agent-written “tests passed” claim cannot satisfy observed execution.

## First research decision

TASK-09 and TASK-10 add bounded Jev experiments and compare against simpler alternatives. Freeze labels, splits, thresholds, and budgets before held-out evaluation. Keep the deterministic workflow available if Jev adds no measurable benefit.

## Starting checklist

- [ ] Review the proposed [ADRs](../adr/README.md) and record accepted/revised choices.
- [ ] Select one small repository/task fixture and exact host versions.
- [ ] Complete the compatibility and provider-data records.
- [ ] Create schema fixtures for missing evidence, failed checks, scope mismatch, and stale snapshots.
- [ ] Implement the deterministic slice before native automation.
- [ ] Pre-register the first experiment and preserve failed attempts.

The [backlog](backlog.md) is the canonical task list. No issue creation, package installation, remote evaluation, or product implementation is implied by this documentation update.

