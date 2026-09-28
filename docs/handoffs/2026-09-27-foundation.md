# Foundation increment handoff

Historical snapshot. Continue from [gateway-only increment](2026-09-27-gateway-only.md)
for current user constraints and results; the credential-wait section below is no
longer current.

Goal remains active and incomplete. Previous goal turn: concrete implementation
progress, not a wait or blocker. No background process is left running.

## Current executable state

Python package under src/agent_checkpoint. contracts.py is a frozen, extra-forbidden
domain model and pure reducer. storage.py uses transactional SQLite, idempotent
contract creation/additive revision, scoped append-only events, call reservation,
and content-addressed bounded blobs. snapshot.py hashes Git and all relevant files
(including ignored files), rejects unsupported links/submodules, and records stat
generations for edit/revert detection. runner.py executes approved argv through a
gated bootstrap with Windows Job Object lifetime control and bounded output.

Full rerun: 46 tests passed in 39.79 seconds; Ruff formatting/check and mypy pass.
uv build produced a 0.1.0 wheel/sdist including service.py. JUnit output is at
artifacts/local/foundation-tests.xml (ignored local evidence). These
artifacts are foundations only, not the separately installed self-use build N.
Exact commands are in root AGENTS.md. No provider requests or host config edits.

## Next implementation work

1. Service orchestration now implements start_task/run_checks/complete, pending
   replay prevention, recorded starts/results, policy pinning and blob/freshness
   checks. Add trusted repository configuration, revision API and concurrency tests.
   Review overlapping runs: latest completion event currently wins; ensure pending
   or late-finishing older runs cannot mask a newer failure or interrupted check.
   Revalidate contract revision at report publication. Validate executable identity
   (currently argv/runtime/environment identity, not executable bytes).
2. Add CLI, local catalog/routing, explicit unavailable review, and all five MCP tools.
3. Implement and validate isolated candidate materialization and promotion checks;
   runner currently refuses isolated_snapshot. Do not remove this refusal without
   a tested stronger path.
4. Add bounded optional direct Python Jev adapter after inspecting installed SDK
   signatures/retry controls. Use `rg --no-ignore` to inspect .venv files. Run commands
   with `--extra jev` or uv removes the optional extra from the environment.
5. Install independently validated N outside checkout/state. Use it for two genuine
   follow-up tasks (choose actual remaining improvements, not mock demonstrations).
6. Three baseline/intervention scenarios, promotion/rollback and manual escape,
   installed-host capabilities, reproducible final report. See goal prompt for full
   acceptance; no smaller definition of success is authorized.

## Known limitations and review targets

Working-tree metadata cannot prove absence of all concurrent mutation. Snapshot
limits are explicit errors. Process lifetime control is not a security sandbox.
Windows .bat/.cmd check wrappers are deliberately unsupported until safe argv
handling is tested; use resolved native executables. Only additive contract revision
is currently allowed because a user-attestation authority boundary is not implemented.
Core storage models do not authenticate callers; the service/API boundary must do so.
No task backlog checkbox has been marked complete.

User replied to live-call question authorizing Vercel Gateway and additionally
requested an AI SDK index.ts holiday-generation example using openai/gpt-5.5.
Implemented examples/vercel-gateway with npm, ai 7.0.118, tsc and native Node 24
execution. Typecheck passes. `npm start` stopped at missing local key; no remote
generation performed. Root .env.local was created with EMPTY placeholder and is
Git-ignored. Never inspect, print, log or commit its contents. User was asked to
enter a replacement key locally and reply ready; a credential had been pasted into
chat and MUST NOT be copied into files/tool arguments/handoffs.

Vercel public catalog lists openai/gpt-5.5 and typesafe-ai/jev. Official TypeSafe
gateway URL: https://ai-gateway.vercel.sh/typesafe (systemone at /v1/systemone).
Gateway model aliases are not proof of the underlying versioned Jev model; retain
requested/returned identity and label reproducibility limits rather than accepting
a silent model-pin substitution. Recheck pricing and bounded call authorization.

Existing docs were untracked before work; do not assume ownership or commit.
