# ADR-0010: Authoritative evidence obligations, not inferred semantic proof

Status: Proposed; not implemented. Date: 2026-09-27.

## Context

Current check_ids bindings and additive revisions protect explicit obligations,
but do not authenticate their author or establish meaningful test coverage.
The report proposes request digests, authority labels and requiredEvidence records.
Those are useful identities only when backed by a producer/approval contract.

## Proposed decision

Define ready as satisfaction of the current declared authoritative evidence
obligations, never universal implementation correctness. Add an opt-in new contract
version only after specifying who approves bindings and how that approval is
captured independently of agent-written origin fields. Keep legacy contracts
explicitly labeled legacy; never silently upgrade them to authenticated authority.

Start with owner-approved check_pass bindings. Consider test_case or
artifact_assertion only with a deterministic producer that proves the expected
test/assertion ran for the current inputs. A test name is not an execution receipt.
Missing authority/binding/evidence stays unknown. Semantic advice never satisfies
required obligations. Existing obligations cannot be weakened by agent revision.

Separate requirement authority, observation provenance and verdict aggregation.
An authenticated manual pass cannot waive a failed independently required check.
Repository-owned policy is a reviewed local boundary, not same-user tamper proof.

## Alternatives and consequences

A digest alone is cheap but does not authenticate consent. A generic model reviewer
cannot create binding authority. Requiring human approval for every trivial check
would add overhead; a reviewed policy template could amortize it, with its scope
and version bound to the task. The owner-facing approval UX remains unresolved.

Compatibility tests must cover v1 reads, opt-in v2 writes, attempted weakening,
unapproved bindings, test-not-collected, wrong assertion, stale evidence, independent
CI disagreement and rollback. No automatic state migration or active promotion is
authorized by this proposal.

## Revisit / next step

Produce the authority threat model, approval example, strict fixtures and migration
plan before implementation. See ADJ-02 in the adjustment roadmap and ADR-0004.
