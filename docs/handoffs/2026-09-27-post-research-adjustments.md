# Post-research adjustments handoff

Date: 2026-09-27. User authorized consolidation and starting adjustments, not an
unbounded implementation of every recommendation. First slice: ADJ-01.

## Delivered

- Preserved the complete supplied report, including its stated 2026-09-28 date and
  unresolved citation markers; normalized-text comparison confirms preservation.
- Added current status, code-grounded reconciliation, accepted ADR-0009, proposed
  ADR-0010, current adjustment roadmap, and completion diagnostic reference.
- Corrected entry points and labeled old bootstrap/roadmap text as historical.
- Routine semantic review is now opt-in in AGENTS.md. Jev routing and all five tools
  remain available, with unchanged Gateway policy and payload approvals.
- Candidate 0.1.3 implements completion schema 2 diagnostics and validated completion
  success/error output. No arbitrary commands, execution grants or retry promises.
- The installed active supervisor stays at 0.1.2; no state migration, promotion,
  credential relocation, host reload, publication, hooks or external CI change.

## Verification observed before final pinned check run

17 new cases failed against the prior behavior; implementation made them pass.
Focused diagnostics/service/runtime/MCP suite: 45 passed in 41.61 s.
Full independent offline suite: **113 passed in 82.44 s**. Ruff lint and formatting
pass (29 Python files); mypy passes (14 source files). Tests use isolated repositories
and mock/disabled providers, not active state or real external calls.

Tests cover missing, failed, stale, unavailable/corrupt and interrupted results;
missing binding/manual surface; optional unknown criteria; execution-field rejection;
malformed advisory authority rejection; and actual stdio schema 2 completion.
These establish tested behavior, not semantic coverage of arbitrary future tasks.

Separate candidate artifacts and final live-task verification are retained outside
the checkout under C:/Users/juanf/AppData/Local/agent-checkpoint/harness/candidate-0.1.3.
Consult its validation report/manifest for installation identity and final result;
the source archive necessarily predates those external outputs. Do not infer native
Codex invocation or active promotion from a standalone installed MCP test.

## Self-use record

Pinned task: f0e443af3d1f30e363912ea5a2f72864. Candidate never supervised itself.
One live Jev routing request through Vercel selected backend-testing:
decision e5f0f01c-011c-4338-921a-b43b68ba0bd1, 446 input / 40 output tokens,
0.860094 s, zero retries, billed dollars unknown. Reported confidence was 0.09;
this is advice, not evidence of correctness or calibration. The testing skill was
also independently applicable to the task. No routine review call was made under
the revised opt-in policy. No source files or raw check blobs were sent.

The ADR skill guided context/options/consequences and scoped statuses; Backend
Testing guided test-first isolated fixtures and provider mocking.

## Next task

ADJ-02: define and review an authenticated approval path for evidence bindings,
including compatibility/migration and negative fixtures. Do not add writable
authority strings and call the problem solved. ADJ-03 formalizes existing shared
execution context without removing relevant identity inputs. See the
[roadmap](../planning/post-research-adjustments.md) for dependencies and acceptance.
