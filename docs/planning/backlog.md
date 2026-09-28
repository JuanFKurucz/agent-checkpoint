# Implementation backlog

Historical broad acceptance backlog. Do not infer runtime absence from the original
unchecked status or provisional .ts paths. See [current status](../status.md) and
[ADJ work packages](post-research-adjustments.md) for implemented subsets and the
current sequence; broad TASK criteria are not marked complete by this slice.

Status: all tasks planned and unchecked. This is a local execution backlog, not a record of created GitHub issues. Paths below are intended outputs and may not exist. Owner roles are unassigned. Existing .ts filenames are provisional identifiers from the original proposal, not a language requirement; TASK-01/03 will map them to the chosen package layout before implementation.

## Dependency summary

| Task | Priority | Milestone | Depends on | Deliverable |
|---|---|---|---|---|
| TASK-01 | P0 | M0 | None | Verify foundations and compatibility |
| TASK-02 | P0 | M0 | None | Define provider data boundary |
| TASK-03 | P0 | M0 | 01 | Create the minimal runtime skeleton |
| TASK-04 | P0 | M0 | 03 | Implement task and result schemas |
| TASK-05 | P0 | M1 | 04 | Build durable state and blob storage |
| TASK-06 | P0 | M1 | 05 | Implement snapshots and approved check execution |
| TASK-07 | P0 | M1 | 04,05,06 | Implement deterministic completion |
| TASK-08 | P0 | M1 | 04,05 | Implement catalogs and local providers |
| TASK-09 | P0 | M2 | 01,02,08 | Add bounded Jev provider |
| TASK-10 | P0 | M2 | 07,08,09 | Freeze and run offline experiments |
| TASK-11 | P1 | M3 | 07,08 | Implement explicit CLI |
| TASK-12 | P1 | M3 | 01,11 | Implement five-tool MCP surface |
| TASK-13 | P1 | M4 | 10,12 | Implement verified Codex hook adapter |
| TASK-14 | P1 | M4 | 13 | Add opt-in bounded continuations |
| TASK-15 | P1 | M5 | 11 | Implement independent CI verification |
| TASK-16 | P1 | M5 | 12,14 | Implement installer, packaging, and recovery |
| TASK-17 | P1 | M5 | 12 | Verify and prototype Claude native hooks |
| TASK-18 | P1 | M6 | 10,14,15 | Run controlled whole-task trials |
| TASK-19 | P1 | M6 | 16,18 | Conduct observe-only field trial and release review |
| TASK-20 | P2 | Future | 19 | Evaluate expansions individually |

Dependencies refer to task IDs in this file. Research tasks can record a negative result and still complete; dependent implementation must follow that result rather than assuming Jev was selected.

The separate [harness backlog](self-adoption-roadmap.md) uses HARNESS IDs for the Codex setup and staged internal adoption. It references these product capabilities without duplicating or completing their implementation tasks.

## Task cards

### TASK-01: Verify foundations and compatibility

- [ ] Completed with linked validation evidence.
- Priority: P0. Milestone: M0. Owner role: Integration engineer.
- Depends on: none.
- Planned outputs: `docs/research/compatibility-spike.md`, `tests/fixtures/hosts/`.
- Work: Run the [Python-first comparison](../research/python-langchain-assessment.md): langchain-typesafe versus direct typesafe-sdk, Python MCP STDIO, packaging, cold-start, cancellation/retries, and tracing defaults. Retain TypeScript/Node 24 as the alternative. Record the runtime decision, exact package/host versions, negotiated protocol, and jev-1.13.0 evaluation target. Validate minimal exchanges using synthetic data; distinguish documentation checks from live compatibility.
- Acceptance: Every claimed capability has a source/date/version; at least one candidate STDIO exchange has captured input/output, or the blocker is explicit.
- Traceability: REQ-01; Q-03; ADR-0001/0005.

### TASK-02: Define provider data boundary

- [ ] Completed with linked validation evidence.
- Priority: P0. Milestone: M0. Owner role: Maintainer/data owner.
- Depends on: none.
- Planned outputs: `docs/research/provider-data-boundary.md`.
- Work: Record allowed evidence classes, redaction/deny behavior, credential placement, current terms needing organizational review, retention assumptions, and who may enable remote use. Enterprise ZDR availability is documented; this account's agreement remains unverified. Do not infer authorization from API-key presence.
- Acceptance: A synthetic allowed bundle and a secret-containing denied bundle are specified; unresolved retention terms cannot be described as zero retention.
- Traceability: REQ-05; Q-02; ADR-0006.

### TASK-03: Create the minimal runtime skeleton

- [ ] Completed with linked validation evidence.
- Priority: P0. Milestone: M0. Owner role: Runtime engineer.
- Depends on: TASK-01.
- Planned outputs: One package manifest and lockfile (`pyproject.toml` for Python, or `package.json`/`tsconfig.json` if TypeScript is selected), core and adapter modules, updated planned paths.
- Work: Scaffold the runtime selected in TASK-01; select package manager, schema library, SQLite implementation, and test runner. Pin exact resolved dependencies and runtime. Establish one package and import boundaries; do not require LangGraph or hosted LangSmith merely to use Python.
- Acceptance: A minimal build and offline test run succeed on Windows; core imports no MCP/host code; package decisions and exact versions are recorded.
- Traceability: REQ-01; Q-06; ADR-0001.

### TASK-04: Implement task and result schemas

- [ ] Completed with linked validation evidence.
- Priority: P0. Milestone: M0. Owner role: Core engineer.
- Depends on: TASK-03.
- Planned outputs: `src/contracts/`, `src/core/task-service.ts`, `src/core/readiness-reducer.ts`, `tests/contracts/task-contract.test.ts`.
- Work: Encode criterion origins, required flags, evidence_policy, satisfaction rules, identity, immutable revisions, optimistic concurrency, and completion/error shapes. Implement explicit task registration/revision validation and a pure readiness reducer over supplied domain records. Durable evidence orchestration remains TASK-07.
- Acceptance: Round-trip fixtures validate; empty contracts, required advisory-only authority, scope mismatch, unauthorized weakening, duplicate IDs, and stale revision updates are rejected. A positive semantic fixture alone cannot pass a required criterion; missing manual evidence remains unknown.
- Traceability: REQ-02; Q-05; ADR-0004.

### TASK-05: Build durable state and blob storage

- [ ] Completed with linked validation evidence.
- Priority: P0. Milestone: M1. Owner role: Runtime engineer.
- Depends on: TASK-04.
- Planned outputs: `src/storage/`, `src/evidence/blob-store.ts`, `tests/integration/storage.test.ts`.
- Work: Implement migrations, transactional records, atomic blob writes, digest verification, scoped queries, crash recovery, and retention policy. Design bounded busy retries and backup/restore.
- Acceptance: Concurrent tasks/worktrees remain isolated; interrupted writes cannot become success; recovery retains budgets; corrupted/missing blobs become unavailable.
- Traceability: REQ-02/03; Q-06/10; ADR-0002.

### TASK-06: Implement snapshots and approved check execution

- [ ] Completed with linked validation evidence.
- Priority: P0. Milestone: M1. Owner role: Runtime engineer.
- Depends on: TASK-05.
- Planned outputs: `src/evidence/snapshot.ts`, `src/evidence/check-runner.ts`, `tests/integration/freshness.test.ts`.
- Work: Canonicalize scope manifests; handle unborn HEAD, untracked/ignored relevant inputs, check scripts, mode changes, and declared environment. Run approved argv with explicit working_tree/isolated_snapshot modes, filtered environment, output limits, descendant-process cancellation, and before/during/after freshness observation. Required isolated execution must not silently fall back.
- Acceptance: Edit-during-run, edit/revert uncertainty, changed policy, changed check script, untracked file, cross-worktree, timeout, and Windows quoting fixtures never silently produce current passing evidence; provider secret absent from child environment.
- Traceability: REQ-03/05; Q-04/11; ADR-0002/0006.

### TASK-07: Implement deterministic completion

- [ ] Completed with linked validation evidence.
- Priority: P0. Milestone: M1. Owner role: Core engineer.
- Depends on: TASK-04, TASK-05, TASK-06.
- Planned outputs: `src/core/completion-service.ts`, `src/policy/`, `tests/unit/completion.test.ts`.
- Work: Use TASK-04's reducer to aggregate authoritative mechanical/manual evidence; keep semantic findings separate. Load correctly scoped records, compute current snapshot, and persist unknown causes and constrained next actions.
- Acceptance: Failed required check dominates a positive semantic fixture; required unknown is unresolved; empty/malformed contract never ready; neither implicit check execution nor provider calls occur during completion.
- Traceability: REQ-03/06; ADR-0004.

### TASK-08: Implement catalogs and local providers

- [ ] Completed with linked validation evidence.
- Priority: P0. Milestone: M1. Owner role: Core engineer.
- Depends on: TASK-04, TASK-05.
- Planned outputs: `src/catalog/`, `src/providers/types.ts`, `src/providers/mock.ts`, `src/providers/heuristic.ts`, `src/core/routing-service.ts`.
- Work: Discover or explicitly register resources, hash definitions, preserve mandatory skills, filter eligible IDs, and include none. Use validated discriminated provider results. Add deterministic and mock fixtures.
- Acceptance: Uninstalled/disallowed IDs are rejected; mandatory instructions remain; disappearing resources invalidate cached recommendations; none differs from provider failure.
- Traceability: REQ-04; ADR-0003.

### TASK-09: Add bounded Jev provider

- [ ] Completed with linked validation evidence.
- Priority: P0. Milestone: M2. Owner role: Provider engineer.
- Depends on: TASK-01, TASK-02, TASK-08.
- Planned outputs: `src/providers/jev.ts`, `src/core/review-service.ts`, `tests/contracts/jev.test.ts`.
- Work: Integrate the provider library selected in TASK-01 (Python LangChain adapter or direct SDK; TypeScript only if selected) with jev-1.13.0 as the initial evaluation pin, typed routing and three-way evidence questions, requested/returned model tracking, optional native confidence fields, physical-call/retry accounting, deadlines, input limits, caching, and spend estimates. Verify actual cancellation/retry controls and telemetry destinations; do not stack retries blindly or silently replace the requested model.
- Acceptance: Synthetic opt-in smoke works if credentials are separately authorized; offline timeout/malformed/disabled fixtures work without credentials; no private data or full environment leaks; outage maps to unknown/abstention.
- Traceability: REQ-04/05; Q-09; ADR-0003.

### TASK-10: Freeze and run offline experiments

- [ ] Completed with linked validation evidence.
- Priority: P0. Milestone: M2. Owner role: Evaluation lead.
- Depends on: TASK-07, TASK-08, TASK-09.
- Planned outputs: `evals/protocols/pilot-v1.md`, `evals/datasets/`, `evals/results/`.
- Work: Create independently labeled routing/evidence examples with repository-family splits. Resolve the earlier and revised report's candidate thresholds into one precommitted protocol, including coverage, uncertainty, budget limits, and pricing assumptions. Compare deterministic, heuristic, self-judge, and Jev. Preserve disagreement and failures. Do not choose gates after viewing held-out results.
- Acceptance: Reproduction manifest, held-out results, calibration/risk-coverage analysis, cost/latency, and a go/no-go note exist. No final-test labels used for tuning.
- Traceability: REQ-08; Q-01/05/09; ADR-0007.

### TASK-11: Implement explicit CLI

- [ ] Completed with linked validation evidence.
- Priority: P1. Milestone: M3. Owner role: Interface engineer.
- Depends on: TASK-07, TASK-08.
- Planned outputs: `src/adapters/cli/`, `tests/contracts/cli.test.ts`.
- Work: Implement documented task, route, check, review, completion, doctor basics, and export commands against shared services. Review returns disabled/unknown when semantic provider is unavailable.
- Acceptance: Help and examples execute on fixture repo; JSON and exit codes match reference; wrong task and failed check are distinguishable; secrets excluded from output.
- Traceability: REQ-01/03; ADR-0001.

### TASK-12: Implement five-tool MCP surface

- [ ] Completed with linked validation evidence.
- Priority: P1. Milestone: M3. Owner role: Integration engineer.
- Depends on: TASK-01, TASK-11.
- Planned outputs: `src/adapters/mcp/`, `tests/contracts/mcp.test.ts`, `docs/integrations/compatibility.md`.
- Work: Register schemas and STDIO serving using the pinned compatible SDK. Mirror compact results for text-only clients as needed. Smoke-test explicit workflows in Codex and Claude Code.
- Acceptance: Five tools discoverable; outputs match CLI fixtures; no log pollution on stdout; exact host tuple and unsupported capabilities recorded.
- Traceability: REQ-01; Q-03; ADR-0005.

### TASK-13: Implement verified Codex hook adapter

- [ ] Completed with linked validation evidence.
- Priority: P1. Milestone: M4. Owner role: Codex integrator.
- Depends on: TASK-10, TASK-12.
- Planned outputs: `src/adapters/codex/`, `tests/contracts/codex-hooks.test.ts`.
- Work: Implement only verified prompt/session/tool/stop payloads. Map host sessions to explicit tasks; record partial observation coverage; avoid transcript scraping. Validate compaction restoration output fields, early SessionStart without MCP, and local SessionEnd bookkeeping. M2 may recommend deterministic-only mode.
- Acceptance: No-task, planning turn, compaction/restart, malformed payload, interrupted session, and unknown-capability fixtures are safe; actual hook smoke is recorded.
- Traceability: REQ-02/06; Q-07; ADR-0005.

### TASK-14: Add opt-in bounded continuations

- [ ] Completed with linked validation evidence.
- Priority: P1. Milestone: M4. Owner role: Core engineer.
- Depends on: TASK-13.
- Planned outputs: `src/core/continuation-service.ts`, `tests/integration/continuation.test.ts`.
- Work: Persist per-task event deduplication, atomic pass reservations, effective-mode checks, and host response mapping. Start with zero passes in observe/advise; the first explicitly enabled enforce pilot permits one task-wide pass for configured actionable mechanical gaps. Subagent observations cannot multiply that budget.
- Acceptance: Concurrent duplicate stop events cannot multiply passes; restarts do not reset cap; semantic-only gaps/outages do not force continuation; exhausted task remains unresolved or needs_changes honestly.
- Traceability: REQ-06; ADR-0004.

### TASK-15: Implement independent CI verification

- [ ] Completed with linked validation evidence.
- Priority: P1. Milestone: M5. Owner role: CI engineer.
- Depends on: TASK-11.
- Planned outputs: `src/adapters/ci/`, `tests/integration/ci-provenance.test.ts`, `selected CI workflow`.
- Work: Review current platform security guidance; rerun checks against exact commit using trusted definitions. Validate artifact producer/commit/digests and keep untrusted code outside credential-bearing evaluation.
- Acceptance: A forged local pass and mismatched artifact are rejected; a PR weakening its own policy cannot approve itself; required checks rerun independently.
- Traceability: REQ-03/05; ADR-0006.

### TASK-16: Implement installer, packaging, and recovery

- [ ] Completed with linked validation evidence.
- Priority: P1. Milestone: M5. Owner role: Distribution engineer.
- Depends on: TASK-12, TASK-14.
- Planned outputs: `src/installer/`, `packaging/plugins/`, `tests/integration/install.test.ts`.
- Work: Build preview/apply/uninstall with ownership manifests, pinned runtime, preserved host configuration, explicit trust, doctor capability reporting, migration/backup behavior, and retention controls.
- Acceptance: Double install is idempotent; uninstall preserves unrelated entries and evidence unless explicitly requested; paths with spaces work; hooks never fetch latest; recovery tested.
- Traceability: REQ-07; Q-10; ADR-0005.

### TASK-17: Verify and prototype Claude native hooks

- [ ] Completed with linked validation evidence.
- Priority: P1. Milestone: M5. Owner role: Claude integrator.
- Depends on: TASK-12.
- Planned outputs: `src/adapters/claude-code/`, `tests/contracts/claude-hooks.test.ts`, `docs/integrations/claude-code.md`.
- Work: Recover current primary hook/plugin contracts; implement only supported lifecycle mappings through shared core. Retain explicit MCP when native capability is absent.
- Acceptance: Documented capability matrix plus payload and live smoke results; equivalent domain results to Codex for shared fixtures; no copied incompatible response semantics.
- Traceability: REQ-01/06; Q-08; ADR-0005.

### TASK-18: Run controlled whole-task trials

- [ ] Completed with linked validation evidence.
- Priority: P1. Milestone: M6. Owner role: Evaluation lead.
- Depends on: TASK-10, TASK-14, TASK-15.
- Planned outputs: `evals/protocols/end-to-end-v1.md`, `evals/results/end-to-end/`.
- Work: Execute randomized paired conditions with repeated trials, isolated workspaces, independent hidden checks, budget accounting, and blinded review. Use the pre-registered protocol and report all attempts.
- Acceptance: Quality and false-ready intervals, total cost per accepted task, p95 wall-time deltas, failures, and condition-specific recommendation are reproducible.
- Traceability: REQ-08; Q-01; ADR-0007.

### TASK-19: Conduct observe-only field trial and release review

- [ ] Completed with linked validation evidence.
- Priority: P1. Milestone: M6. Owner role: Maintainer.
- Depends on: TASK-16, TASK-18.
- Planned outputs: `docs/research/field-trial.md`, `docs/release-readiness.md`.
- Work: Recruit consenting repositories; record interventions/disagreement and real overhead without blocking. Validate manuals on built artifacts and choose release scope. Native Claude support additionally requires TASK-17.
- Acceptance: Gate results, compatibility tuples, open limitations, recovery evidence, and explicit release/no-release decision recorded; no unsupported savings claim.
- Traceability: REQ-07/08; ADR-0007.

### TASK-20: Evaluate expansions individually

- [ ] Completed with linked validation evidence.
- Priority: P2. Milestone: Future. Owner role: Research lead.
- Depends on: TASK-19.
- Planned outputs: `Separate future ADR and experiment per expansion`.
- Work: Prioritize context filtering, optional check selection, subagent routing, model routing, repository-specific architecture review, then any remote deployment need. Define benefits and failure cases before implementation.
- Acceptance: Each proposed addition has its own held-out comparison, host capability proof, and scope decision; required checks and user authority remain intact.
- Traceability: Q-12/13/14; ADR-0003/0007.

## Completion discipline

Replace a checkbox only when its acceptance evidence is linked. A passing documentation check is not completion of a runtime task. Update the [roadmap](roadmap.md) when the milestone gate is met, and record any design change in the relevant [ADR](../adr/README.md).

