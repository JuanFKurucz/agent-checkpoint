# Validated internal MVP handoff

Read the [operating report](../reports/mvp-validation-report.md) and
[requirement audit](../reports/mvp-completion-audit.md). Internal candidate 0.1.1 is
implemented and validated; broader public-release, host hooks and M0–M6 research
are not implied complete. No background validation process remains running.

## Preserved runtimes and state

- N: C:/Users/juanf/AppData/Local/agent-checkpoint/self-use/build-83114bf8.
  Unchanged wheel 83114bf8…; active-state remains its separate original directory.
- Candidate: C:/Users/juanf/AppData/Local/agent-checkpoint/self-use/candidate-0.1.1.
  Noneditable installed wheel 8b4d2db9…; exact hashes and dependencies in manifest.
- Promotion drill: self-use/promotion-drill-0.1.1-retry1. Contains frozen source,
  separate environment, backup-state, candidate-state, broken-state, rollback-state,
  launcher.json (rolled back to N) and full report. Real active state untouched.
- First drill self-use/promotion-drill-0.1.1 retained: offline cache-path failure
  before promotion. Do not erase failed evidence or confuse it with the retry.

## Observed acceptance

89 tests pass in current checkout (127.00 s) and isolated archive (137.92 s).
Lint/format/types pass. All 13 runtime files match archive, wheel, checkout and
installed package. All 90 extracted archive files were unchanged after validation.
Installed MCP exchange calls all five tools; native-host invocation is not tested.
Pinned N completed shadow plus two real follow-up changes. Eighteen matched workflow
trials pass, but Checkpoint adds 7.320/11.929/18.527 seconds median workflow overhead
on the three tiny scenarios. This is not proof of agent speed/quality/cost gains.
Copied-state promotion, corrupt-state refusal, disabled-launcher direct checks
(24 passed), and N plus backup rollback are observed.

## Boundaries and next work

Only Jev through Vercel Gateway is authorized. Never inspect .env.local or reuse the
credential pasted in chat. No new live requests occurred during final validation;
Python live Jev remains unverified, unlike the earlier separate synthetic TS smoke.
No native hooks/global host configuration changed. Native Codex/Claude MCP requires
separate setup/authorization; explicit Codex CLI use is the demonstrated integration.

Next priorities: profile CLI/snapshot overhead, then a bounded Python Jev smoke if
approved, native MCP after restart/setup, authenticated manual attestations and
explicit interrupted-run reconciliation, stronger dependency identity and migration
automation. Required manual evidence remains unknown today. Working-tree checks
are not a security sandbox; isolated_snapshot runner mode stays unavailable.

All files remain uncommitted/untracked in the original unborn repository. No pushes
or publication were authorized. Original research exports were preserved. Source
identity is by frozen archive, not a fabricated Git commit. Later docs and two
operator helpers are outside that archive; their hashes are in the artifact report.
