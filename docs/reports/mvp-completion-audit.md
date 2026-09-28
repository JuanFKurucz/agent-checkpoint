# Internal MVP requirement audit

Date: 2026-09-27. Scope is the original working-MVP goal, not the entire proposed
TASK/M0–M6 or HARNESS backlog. Evidence identifies frozen candidate 0.1.1, not an
unqualified claim about future checkout contents. Its 13 runtime Python files match
the current checkout, source archive, wheel and separate installed package.

## Required executable increments

| Requirement | Authoritative evidence | Result / boundary |
|---|---|---|
| Python choice and SDK comparison | ADR-0001; Python assessment; locked typesafe-sdk 0.7.2 versus LangChain dependency rationale | Met; direct SDK goes only through Vercel, no parallel product runtime |
| Reproducible environment and direct commands | pyproject.toml, uv.lock, AGENTS.md; extracted-archive uv sync/lint/format/mypy/pytest logs in promotion report | Met on Windows/CPython 3.13.11; public multi-platform distribution not claimed |
| Compact plan, task and handoff records | implementation-progress.md mapped to TASK/HARNESS IDs; persisted three self-use contracts and handoffs | Met; broader backlog boxes are not automatically marked done |
| Versioned immutable contracts and authority | contracts.py/storage.py; contract freezing, revision conflict/weakening and provenance tests | Met; manual evidence stays unknown without authenticated attestation, rather than accepting agent claims |
| Task/worktree scope, durable SQLite, bounded blobs | storage and snapshot tests; source scope checks; atomic transaction/replay tests | Met; IDs alone cannot cross worktrees; corrupt blobs/database do not pass |
| Snapshots and approved execution | snapshot.py/runner.py; environment, mutation, edit/revert, limits, executable and child-process fixtures | Met for working-tree observations; isolated_snapshot requests explicitly unavailable |
| Deterministic completion and local skill routing | reducer/service/runtime tests; installed CLI scenario results and installed MCP smoke | Met; mandatory skills retained, local ties abstain |
| Provider-independent semantic advice | runtime review and advisory-freshness tests with mocked decisions; required semantic-policy rejection | Met; positive/negative advice cannot determine required mechanical/manual readiness |
| Same core via CLI and all five MCP tools | runtime.call wiring; CLI lifecycle tests; actual installed five-tool stdio exchange | Met; stdout protocol-only, unknown authority fields rejected |
| No implicit tests or provider calls from completion | service completion test and code path; installed missing-result smoke; runtime complete never calls remote | Met; disabled review explicitly PROVIDER_DISABLED |
| Bounded optional Jev | 14 gateway tests; literal endpoint/model/key policy, request hook, timeout, persistent call budget, no retries, response cap | Met offline; live Python compatibility and exact model-version attestation unverified |

## Self-use, recovery and validation

| Requirement | Authoritative evidence | Result / boundary |
|---|---|---|
| Independent pinned N after direct checks | N wheel/source hashes, requirements/manifest and installed site-packages path; 77-test preinstall record | Met; N preserved unchanged, baseline wheel hash rechecked |
| Shadow after completed work | task 9f8941309f492a5bcea4818e78b22d04; four recorded approved checks and historical ready snapshot | Met; not treated as advice that guided prior work |
| At least two real follow-up tasks | b815f3c9f197edfcf8b324ba8d08715a and 573bdefdea3467f9ad4b3e8cae766fbc; retained contracts, events/blobs and self-use record | Met; advisory freshness and bounded response fixes, red/gap → repair → independent checks |
| Active N separate from candidate fixtures | N directory + active-state; candidate venv and disposable pytest/scenario/drill stores | Met; no rebuilt candidate substituted during the two tasks |
| Actual CLI host use, actual MCP protocol exchange, native attempt | Codex shell invocations of N; installed MCP smoke; native codex mcp get temporary configuration record | Met via permitted CLI fallback; native session tool reload unavailable, restart setup documented |
| Claude capability status | installed Claude 2.1.41 record; no new coding-model session authorized under Jev-only boundary | Met reporting requirement; native Claude MCP remains unverified |
| Controlled promotion with isolated inputs/copied state | promotion-drill JSON: independent tests on extracted archive, installed-file verification, SQLite backup, local launcher switch | Met for the local drill; 90 archive files unchanged afterward, all 13 code files match wheel; no security-sandbox claim |
| N+1 must not certify itself | promotion helper imports no Checkpoint core and gates on direct commands/file comparisons, never a candidate ready verdict | Met; current runtime cannot grant its own promotion |
| Rollback and manual escape during failure | corrupt disposable database → STORAGE_UNAVAILABLE; disabled drill pointer; 24 direct tests; N plus backup-derived state restored | Met; schema remained v1, no irreversible-migration compatibility claim |
| Passing/failing/missing/stale and full rerun lifecycle | service lifecycle test; all three scenario reports include register/check/report/edit/stale/rerun results | Met; failures retained in all-attempt logs |
| Edit-during-check, contract/check changes | runner mutation/edit-revert/context tests, storage/runtime revision tests, service changed-definition test | Met; generation is ordinary-mutation detection, not hostile metadata protection |
| Cross-task/worktree isolation and duplicate mutations | parameterized provenance tests, task binding and worktree tests, replay conflict and concurrent claim tests | Met |
| Interrupted execution and corrupt/unavailable state | injected KeyboardInterrupt fixture, pending replay/new-task recovery, process timeout, corrupt blob/database and missing-executable fixtures | Met; no automatic pending-run reconciliation or authenticated cancellation endpoint |
| Provider timeout, malformed response and exhausted budgets | gateway and concurrent persistent-budget tests | Met with mock transport; automated tests have no live API dependency |
| Windows paths with spaces and descendant cancellation | runner, CLI/MCP and scenario fixtures; Windows Job Object normal-exit and timeout tests | Met on this Windows host |
| Three repeatable baseline/intervention scenarios | workflow-measurements JSON, three repetitions each, nine baseline trials before nine Checkpoint trials | Met; 18/18 outcomes pass, identical acceptance argv/script per condition |
| Timings, attempts, overhead, usage uncertainty | each subprocess exit/output/time retained; median deltas in operating report; null tokens/billing and zero provider requests/retries | Met; descriptive fixed-order microbenchmark, not agent-performance evidence |
| Live Jev kept separately scoped | one prior synthetic Gateway TS smoke; Python adapter left offline/unverified; no private code transmitted | Met; no additional live calls, no GPT fallback |
| Clean installed runnable candidate and artifact identity | frozen wheel/sdist hashes, noneditable offline install, installed scenarios/MCP, archive-source-wheel-installed file comparisons | Met; source has no Git commit, so archive hashes provide identity |
| Manuals, reproducible demo/measurement and operating report | internal-runtime.md; measure_scenarios.py, installed_smoke.py, promotion_drill.py; mvp-validation-report.md + JSON records | Met; helpers preserve failed attempts and do not overwrite reports |
| Authority boundaries | project/temporary files only; Git-ignored .env.local never opened; providers/hooks disabled, no pushes/global host edits | Met; obsolete GPT smoke is historical only |

## Explicitly not claimed

No demonstrated coding-quality, token, cost or latency improvement; the tiny local
workflow measurements show added overhead. No native hook enforcement, public
release, hosted telemetry, CI certification, authenticated manual-attestation API,
complete external dependency attestation or production migration system. Native
Codex/Claude MCP and live Python Jev are unverified capabilities explicitly allowed
as limitations by the goal; they are not described as passing tests.

This audit uses the full required internal-MVP scope. The broader design documents
remain a roadmap, and their unimplemented surfaces have not been redefined as done.
