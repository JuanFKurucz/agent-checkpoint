# ADR-0006: Remote opt-in and independent verification

Status: Proposed. Date: 2026-09-27. Implementation: not started.

## Context

Provider requests can expose repository content; checks execute repository code; local records cannot certify a release against an adversarial same-user process. See the [research synthesis](../research/synthesis.md).

## Decision

Default remote evaluation off. Separate runner execution from provider credentials and restrict data bundles. Validate CI artifact origin and rerun required checks with trusted definitions against the candidate commit.

## Alternatives

Unrestricted payloads ease prototyping but violate controlled data use. Accepting a local ready report as CI proof fails independence. Environment filtering alone is not sandboxing.

## Consequences

Additional configuration and isolated CI work are necessary. Local operation stays useful without provider availability. Actual retention and organizational terms require review.

## Revisit conditions

Revisit when provider terms or deployment environments change. No zero-retention or self-hosted Jev claim without evidence.

## Delivery and validation

[Backlog](../planning/backlog.md): TASK-02, TASK-06, TASK-15. Completion requires their stated acceptance evidence. Related decisions: [ADR index](README.md).

