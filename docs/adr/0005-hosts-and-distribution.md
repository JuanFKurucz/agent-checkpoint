# ADR-0005: Explicit MCP first and capability-gated native automation

Status: Proposed. Date: 2026-09-27. Implementation: not started.

## Context

The report has more concrete Codex hook information than Claude hook information. A common plugin shape alone cannot guarantee common behavior. See the [research synthesis](../research/synthesis.md).

## Decision

Ship the same core through explicit MCP/CLI, then a tested Codex hook pilot and a separately verified Claude hook adapter. Prefer host-native plugins when validated. Pin runtime installation; preserve configuration ownership and host trust.

## Alternatives

A generic wrapper cannot observe all internal actions. Rewriting user config wholesale is brittle. Hook-time download of latest introduces uncontrolled changes.

## Consequences

Portable explicit workflows arrive earlier. Automatic behavior differs by tested host capability; documentation must name those differences.

## Revisit conditions

Add hosts only with recorded capability and contract tests. Change packaging independently from domain logic.

## Delivery and validation

[Backlog](../planning/backlog.md): TASK-12, TASK-13, TASK-16, TASK-17. Completion requires their stated acceptance evidence. Related decisions: [ADR index](README.md).

