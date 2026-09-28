# ADR-0004: Explicit task contracts and separate readiness from enforcement

Status: Proposed. Date: 2026-09-27. Implementation: not started.

## Context

An agent can omit requirements, change its criteria, or interpret every conversational stop as an unfinished implementation. Advisory semantics can otherwise become accidental blocking. See the [research synthesis](../research/synthesis.md).

## Decision

Register tasks explicitly. Preserve criterion origin and immutable revisions. Use pass/fail/unknown/not_applicable and ready/needs_changes/unresolved. Effective policy comes from trusted configuration. Host continuation is a separate action limited to configured mechanical gaps in v1.

Declare evidence_policy as mechanical, manual, semantic_advisory, or informational. Required criteria must have mechanical/manual satisfaction rules; semantic_advisory and informational items are optional only. Missing manual evidence stays unknown. Start hook adoption in observation with zero continuations, then permit at most one mechanical continuation in an explicitly enabled pilot. Completion reduces stored evidence and findings; it does not trigger checks or provider calls.

## Alternatives

Free-form completion prompts lack provenance. Automatic prompt-to-contract enforcement risks false task activation. Letting a caller choose a weaker mode allows self-approval.

## Consequences

Reports remain honest without forcing semantic loops. More explicit task setup is required. A ready report covers only the stated contract and evidence rules.

## Revisit conditions

Revisit automatic task drafting with a separate quality study; never silently remove user/repository requirements.

## Delivery and validation

[Backlog](../planning/backlog.md): TASK-04, TASK-07, TASK-14. Completion requires their stated acceptance evidence. Related decisions: [ADR index](README.md).

