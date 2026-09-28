# Internal MVP execution record

Post-goal update: the completed internal MVP was followed by active 0.1.2 adoption
and a [0.1.3 adjustment slice](post-research-adjustments.md). See [current status](../status.md).
The chronological record below remains evidence for the earlier goal, not a request
to restart it or a claim that the candidate was promoted.

Current result: internal MVP 0.1.1 validated. The chronological increments below
retain earlier pending states; the [completion audit](../reports/mvp-completion-audit.md)
and [operating report](../reports/mvp-validation-report.md) are authoritative for
current goal acceptance. Broader TASK/HARNESS milestones remain separately scoped.

Goal activated 2026-09-27. Full objective: runnable deterministic product, CLI/MCP,
bounded optional Jev, actual pinned self-use on two follow-up tasks, isolated promotion
and recovery, three baseline comparisons, and an evidence-backed validation report.

## Work sequence and evidence gates

1. TASK-01/03/04, HARNESS-02/03: runtime decision, locked package, direct commands,
   strict contracts and pure readiness tests. Implemented foundation; broader TASK-01/04
   acceptance and host/provider compatibility remain open.
2. TASK-05/06/07/08: scoped durable state, snapshots, approved runner, truthful
   completion and local routing. Store, snapshots, working-tree runner and basic
   start/check/complete orchestration implemented; configuration, concurrency hardening,
   isolation and local routing remain open.
   Update: trusted JSON configuration, additive revision API, concurrent report
   publication guards, local skill routing and current advisory filtering now run.
   Isolated promotion execution and explicit interrupted-run recovery remain open.
3. TASK-09/11/12: bounded optional provider, CLI and five MCP tools. Pending.
   Gateway-only provider adapter now implemented with offline tests; CLI/MCP and
   provider service integration remain pending.
   Update: CLI and all five MCP tools share the same validated runtime. Real stdio
   protocol exchange passes. Remote review wiring uses fixed Gateway policy and
   exact approved-input digests; default remains unavailable/offline.
4. HARNESS-04/05/06: shadow run, two actual advisory self-use tasks, separate installed
   N/candidate N+1, promotion and rollback. Pending.
   Update: independently installed build 83114bf8 completed shadow and two real
   follow-up tasks. Promotion/rollback and broader HARNESS acceptance remain pending.
5. MVP experiments/report: three baseline/intervention fixtures, installed artifact
   verification, sanitized measurements, setup and recovery instructions. Pending.

Full public-release and native-hook milestones remain outside this internal MVP.
No task is marked complete simply because part of it is implemented.

## Verified first increment

- CPython 3.13.11, uv 0.9.22; dependencies resolved in uv.lock.
- 40 isolated offline tests pass (2026-09-27): reducer, contracts, SQLite revisions,
  replay/scope/corruption, bounded blobs, input identity, mutation/edit-revert,
  subprocess outcomes, secret-environment filtering, output limits and timeouts.
- Windows Job Object tests verify descendant termination on timeout AND normal
  parent exit. Required isolation currently returns ISOLATION_UNAVAILABLE, not pass.
- Ruff check and mypy pass; wheel and source distribution build successfully.
- This is not yet a user-facing runtime: CLI/MCP/services, provider adapter, installed
  self-use, promotion and final measurements/report remain to be implemented.

The Backend Testing skill drove test-first isolated fixtures and network denial.
Six additional service fixtures pass: full unknown/pass/stale/fail/rerun lifecycle,
idempotent check replay, changed policy, unavailable checks, corrupt output, and
completion without implicit check execution. Broader concurrency checks remain open.

## Added user request: Vercel Gateway example

User authorized gateway setup and requested AI SDK generateText with openai/gpt-5.5.
The separate examples/vercel-gateway npm package is installed and typechecks. After
local credential entry, GPT-5.5 generation succeeded (historical evidence only).
The user then restricted all model usage to Jev through Vercel AI Gateway. The
runnable example now uses Jev evaluation, not GPT. One synthetic Jev request passed:
testing selected, 350 input / 38 output tokens, 692 ms evaluation time. Root
.env.local stays Git-ignored; never copy chat credentials or inspect the local value.

The gateway example does not migrate the Python core. Its updated Jev smoke verifies
only that separate TypeScript request, not the Python adapter's live compatibility.
Gateway TypeSafe compatibility can inform the Python adapter once identity/budget
semantics are tested. The Python adapter has offline transport tests; its own live
compatibility is not yet demonstrated. No repository code has been transmitted.

## Second increment (gateway-only and concurrency)

Jev-only Python adapter added with fixed Vercel endpoint/model/key environment,
redirects and proxy inheritance disabled, explicit opt-in, byte/deadline limits,
durable task-call budgets and request replay, no retries, sanitized error codes,
and unknown billing / unverified exact model version. Offline response tests cover
malformed/unknown choice/model mismatch, timeout and budget exhaustion.

Check evidence now uses run-start order, refuses orphan/duplicate transitions, and
keeps overlapping unfinished runs unresolved. Report publication atomically checks
contract revision and evidence high-water to reject concurrent changes. State
written before the phase field existed must be treated as prototype-only, not
migrated into trusted evidence. CLI/MCP and final self-use/report gates remain open.
Full rerun: 64 tests pass in 40.93 s; Ruff format/check and mypy pass; wheel/sdist
build. Latest handoff: [gateway-only](../handoffs/2026-09-27-gateway-only.md).

## Third increment (usable runtime and actual self-use)

Built strict configuration, CLI, five flat-schema MCP tools, local mandatory-skill
routing, scoped unavailable/optional review, revision and snapshot preconditions,
safe errors and `.env` metadata-only snapshots. Seventy-seven tests passed before
building N. Installed its locked wheel independently outside the checkout and
verified site-packages imports under `python -I`.

N then shadow-checked the completed work. Used unchanged N for two genuine tasks:
current-only advisory findings (red → fix → 80 tests and ready), then bounded Jev
response transport (direct red → fix → 83 tests and ready). Active state stayed
outside the checkout; candidate fixtures stayed in disposable stores. No remote
request was made during self-use. Native Codex configuration parsing was checked
with ephemeral -c overrides; native MCP invocation remains unverified.

See the [partial validation report](../reports/mvp-validation-report.md),
[machine-readable self-use record](../reports/self-use-2026-09-27.json),
[runtime manual](../guides/internal-runtime.md), and
[current handoff](../handoffs/2026-09-27-runtime-self-use.md).

## Current decisions

Use installed CPython 3.13.11 with uv. Evaluate the direct TypeSafe client first:
PyPI currently lists typesafe-sdk 0.7.2 and langchain-typesafe 0.0.1a3. LangChain adds
framework dependencies we do not need for the deterministic runtime. Keep Jev in an
optional extra; provider calls and hosted tracing remain disabled. MCP candidate is
2.2.0. Source checks do not prove installed compatibility; pin resolved versions in
uv.lock and test actual imports and local exchanges.

Sources: [direct SDK](https://github.com/typesafe-ai/typesafe-sdk-python),
[LangChain integration](https://docs.langchain.com/oss/python/integrations/providers/typesafe),
[MCP Python](https://github.com/modelcontextprotocol/python-sdk).

## Scope boundaries

Existing Markdown files were untracked on entry; preserve them. No Git commits,
remote writes, host-global configuration changes, provider requests, or telemetry
are authorized by implication. Offline tests use disposable state and deny sockets.

## Fourth increment (final internal-MVP validation)

- TASK-05–08: executable/launcher identity now participates in freshness; two red
  regressions passed after the fix. Interrupted requests remain unresolved without
  hidden reruns; an equivalent new task can recover.
- TASK-03/11/12: distinct 0.1.1 wheel installed offline/noneditable; all runtime files
  verified; installed CLI scenarios and all-five-tool MCP exchange passed.
- HARNESS-03/06: three scenarios with three repetitions in each condition, all nine
  baseline runs before intervention; 18/18 outcomes pass. Added median workflow
  overhead is 7.320/11.929/18.527 s; no agent quality/cost benefit is established.
- HARNESS-05: frozen archive direct checks and 89 tests pass; consistent SQLite
  backup and nine blob checks; disposable promotion, corrupt-state failure, manual
  disable, 24 direct escape tests and N/state rollback pass. Initial offline cache
  failure retained. Actual active N and its state remain untouched.
- Final acceptance: current checkout 89 tests/127.00 s; extracted archive 89 tests/
  137.92 s; current Ruff lint/format (27 files), mypy (13 source files) pass. Ninety
  extracted files unchanged; 13 source/wheel/current/installed runtime files match.
- Python live Jev and native host MCP remain explicitly unverified, as allowed by
  the internal goal. Only Jev through Vercel is authorized. No new live calls made.
