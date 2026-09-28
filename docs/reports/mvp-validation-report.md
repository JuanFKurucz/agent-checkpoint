# Internal MVP validation report

Date: 2026-09-27. The deterministic internal MVP is implemented and validated as
candidate **0.1.1**. A pinned predecessor assisted two genuine development tasks;
the clean installed candidate passed matched scenarios, MCP exchange, and a local
promotion/rollback drill. [Full requirement audit](mvp-completion-audit.md).
No general coding-agent performance benefit or native host MCP success is claimed.

## Verified surfaces

| Surface | Evidence | Limit |
|---|---|---|
| Core/storage/runner | Passing offline tests, SQLite and subprocess fixtures | Working-tree observations, not a sandbox or isolated execution |
| CLI | Subprocess task/check/complete lifecycle fixture; real installed self-use | Planned init/uninstall and authenticated manual attestations absent |
| MCP | Actual stdio client/server exchange lists and calls all five tools | Protocol test, not native Codex/Claude tool invocation |
| Python Jev adapter | Offline endpoint/model, retry, budget, timeout, schema and bounded-response tests | Live Python compatibility unverified; gateway alias is not an exact model-version pin |
| Live Jev | One synthetic AI SDK request through Vercel | Separate example; no repository data sent; billing unverified |
| Self-use | One shadow task, two genuine follow-up tasks through independently installed N | Candidate promoted and rolled back only in a disposable drill; active N unchanged |

Runtime: Windows, CPython 3.13.11, uv 0.9.22, SQLite, pydantic 2.13.5,
mcp 2.2.0, typesafe-sdk 0.7.2, pywin32 312. Exact dependency graph is in uv.lock.
Jev is optional; no LangGraph or hosted LangSmith is enabled. The standalone
TypeScript example is user-requested setup evidence, not a second product runtime.

Historical independent direct verification after both follow-ups: Ruff lint/format,
mypy (13 source files), and 83 tests in 78.25 seconds all pass. The exact test command
was `uv run --locked --extra jev pytest -q
--junitxml=artifacts/local/self-use-direct-tests.xml`. JUnit is local ignored
evidence. These checks ran directly without using N's completion verdict.

Selected the plain TypeSafe Python SDK, configured exclusively for Vercel, over
langchain-typesafe for this MVP: it provides the required async decision primitive,
explicit retry control and a testable transport without adding LangChain runnable,
middleware or tracing layers. LangChain remains a valid future composition option.
This is a dependency/complexity decision backed by the implemented tests, not a
head-to-head performance claim or a claim that the LangChain integration is inferior.

## Installed artifact and source identity

Build N is `agent-checkpoint==0.1.0`, independently installed from a wheel into:

```text
C:/Users/juanf/AppData/Local/agent-checkpoint/self-use/build-83114bf8/venv
```

Wheel SHA-256: `83114bf8ca716c0183d31667fa9e3c6b4184e9c50ea6dffbdce72e8d40087637`.
Source archive SHA-256: `3bbbd501bf2e649c38b29d2b97d2aa42e72033573ceda5127e85d3bc8d51de81`.
Both archives, exported requirements and manifest are preserved beside that venv.
The repository has no commit yet; do not invent a source revision. The source
archive identifies the packaged inputs. `python -I` imports were observed resolving
to this venv's site-packages, not the edited checkout. N was unchanged during both
follow-up tasks. Active state is the separate self-use/active-state directory;
candidate tests use disposable temp stores.

Installation commands, after direct Ruff/format/mypy/77-test verification:

```text
uv build --no-sources
uv export --locked --extra jev --no-dev --no-emit-project --format requirements-txt --output-file N/requirements.txt
uv venv --python 3.13 N/venv
uv pip sync --offline --python N/venv/Scripts/python.exe N/requirements.txt
uv pip install --offline --no-deps --python N/venv/Scripts/python.exe N/agent_checkpoint-0.1.0-py3-none-any.whl
```

Here N is the absolute build directory above; substitute it literally when rerunning.
No package was published and no global tool/host configuration was edited.

Historical unpromoted candidate after the two follow-ups: dist/agent_checkpoint-0.1.0-py3-none-any.whl,
SHA-256 `c49a661409dca3becdd24b28859ad2fc62674f64445a9528210b3fc8631b71a4`.
It has the same prototype version string; use the hash to distinguish it from N.
It is built but not installed/promoted as the active runtime.

## Actual self-use

Invocations use N's Python, never `uv run agent-checkpoint` for the active supervisor:

```text
N/venv/Scripts/python.exe -I -m agent_checkpoint --root D:/Programming/agent-checkpoint --state C:/Users/juanf/AppData/Local/agent-checkpoint/self-use/active-state <command>
```

Task request/contract files live in the outside-checkout self-use directory.
Commands run included task start with --request-file/--contract-file, route with
--request-id, check run with approved IDs, and complete --json. All mutations used
recorded request IDs. [Machine-readable record](self-use-2026-09-27.json) contains
the exact task IDs, attempts, artifact identities, report snapshots and timings.

1. Shadow: `9f8941309f492a5bcea4818e78b22d04`, after direct verification of the
   completed runtime increment. Four approved checks passed; report ready matched
   the independent result. No shadow output guided that already-completed work.
2. Advisory freshness: `b815f3c9f197edfcf8b324ba8d08715a`. Register → local route →
   add regression tests → N runs tests and records two failures → inspect
   needs_changes → fix → three direct regression tests pass → N runs all four
   checks (80 tests) → ready. Old findings are excluded from current advice after
   input, revision or edit/revert changes; history remains available. Positive
   mocked advice cannot satisfy missing mechanical evidence.
3. Bounded responses: `573bdefdea3467f9ad4b3e8cae766fbc`. Register → direct tests
   expose two failures → N reports unresolved because direct failures were not
   imported as trusted evidence → fix → 14 direct gateway tests pass → local route
   → N runs all four checks (83 tests) → ready. Responses exceeding 64 KiB stop
   reading and close; compression is rejected before decompression; accounting
   remains one physical request with no retry.

These reports describe snapshots at publication. Writing this report and making
later changes invalidates currentness; historical ready must not be reused as a
claim about the latest checkout. The tests did not need credentials or live models.

## Host capability record

Codex CLI `0.158.0-alpha.2.1` accepted a temporary `-c` stdio configuration via
`codex mcp get checkpoint --json`. Command, args and empty credential forwarding
were returned correctly. This checks native configuration parsing, not connection
or tool execution. Tool discovery exposed no way to reload this session's tools.
Native MCP invocation remains unverified; explicit Codex command execution of the
installed CLI is the demonstrated integration.

Official docs describe project-scoped MCP configuration and restarting after
adding a server. The intended command is N's Python with `-I -m agent_checkpoint`,
absolute --root/--state, and `mcp --stdio`. Allow more than the default tool deadline
for the full test suite; use a reviewed tool_timeout_sec such as 600. No credentials
are necessary for the offline setup. [Official MCP setup](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).

Claude Code `2.1.41` is installed. No new Claude session/model call was launched;
native compatibility remains unverified. Hooks are disabled for both hosts.

## Live-provider evidence

Only Jev through Vercel AI Gateway is authorized. The earlier GPT setup run is
historical and superseded. See [Jev smoke metadata](gateway-smoke-2026-09-27.json):
testing selected, 692 ms measured evaluation, 350 input/38 output tokens, SDK retries
disabled. One sample is connectivity evidence, not a latency or quality guarantee.
The SDK may fill missing returned model metadata from the requested alias; exact
upstream version remains unverified. No private source was transmitted.

## Internal-MVP acceptance gates

- [x] Conservative executable identity and interruption-recovery review; external
  dependency attestation limits documented.
- [x] Controlled isolated candidate promotion, consistent copied state, rollback
  and broken-runtime manual escape demonstration.
- [x] At least three equivalent baseline/intervention scenarios, all attempts and
  unknown cost/token fields, descriptive analysis only.
- [x] Reproducible clean final candidate installation, final direct checks and
  source/artifact inventory after the remaining changes.
- [x] Complete requirement-by-requirement audit and final operating report.

No task backlog checkbox is promoted merely because this partial prototype works.

## Candidate 0.1.1: freshness and matched measurements

Independent direct checks passed: Ruff lint/format on src/tests/scripts, mypy on
13 source files, and **89 tests in 127.00 seconds**. Two executable-freshness tests
failed before the fix, then passed. All 19 runner/service tests passed in 40.12 s.
The interruption fixture proves pending replay does not rerun, an unfinished run
cannot be hidden by a newer pass, and a same-requirements new task can recover.

The runner now fingerprints resolved executable and launcher bytes plus generation
metadata, rechecks after execution and when reusing evidence. External DLLs/modules,
remote services and excluded dependency directories are not fully attested; use the
locked clean environment, and do not interpret this as a hostile-filesystem sandbox.

The separately installed candidate lives at
`C:/Users/juanf/AppData/Local/agent-checkpoint/self-use/candidate-0.1.1`.
Wheel SHA-256: `8b4d2db9a124117a6e91e6b1248c16481f6d57d65934af0cd2114bf16bb7b33e`.
Source archive SHA-256: `265e0e1fb13eb0b8179b4209a16dc7ecea70bb8aa2cd843ea1cbbae406322018`.
The frozen archive predates the later promotion/smoke helper scripts and report
updates; those are validation tooling, not modifications to this runtime wheel.
Its requirements.txt and manifest.json are preserved beside the artifacts.
Install used uv venv, offline pip sync of exported locked dependencies, and offline
pip install --no-deps of this wheel. `python -I` imports resolved to its site-packages.

The installed MCP smoke called all five tools, observed missing → checked → ready,
mandatory local routing, explicit PROVIDER_DISABLED review, and rejection of an
unknown wire field. Protocol 2025-11-25 identified server version 0.1.1; 9.059 s wall
time, zero provider calls. [Machine-readable exchange](installed-mcp-2026-09-27.json).
This is still not a native Codex/Claude MCP result.

### Descriptive workflow comparison

All **18 trials passed**: three scenarios × two conditions × three repetitions.
All nine baseline trials completed before any intervention trial. Each used a fresh
repository and the exact same acceptance argv/script; setup time was excluded.
The Checkpoint condition additionally registered criteria and inspected evidence.
The baseline was direct command execution, not a simulated coding agent.

| Scenario | Baseline median seconds | Checkpoint median seconds | Added seconds |
|---|---:|---:|---:|
| Passing | 0.150 | 7.470 | 7.320 |
| Failure → repair | 0.306 | 12.234 | 11.929 |
| Pass → edit → stale → failure → repair | 0.451 | 18.978 | 18.527 |

These results show substantial overhead for tiny local tasks, not a latency/cost
improvement. Fixed ordering, process startup, Windows Git/snapshot work, and a small
sample limit inference. No autonomous agents or live providers participated. Each
condition ran respectively one, two or three acceptance attempts; repair reruns are
intentional, not provider retries. Provider requests/retries were zero; token/billing
fields remain null. No claim of reduced agent errors, tokens or spending is made.

[All commands, attempts, exits, outputs and times](workflow-measurements-2026-09-27.json)
were emitted by scripts/measure_scenarios.py. Reproduce with the candidate Python:

```powershell
& 'C:/Users/juanf/AppData/Local/agent-checkpoint/self-use/candidate-0.1.1/venv/Scripts/python.exe' -I scripts/measure_scenarios.py --python 'C:/Users/juanf/AppData/Local/agent-checkpoint/self-use/candidate-0.1.1/venv/Scripts/python.exe' --output NEW_MEASUREMENTS.json --repetitions 3
& 'C:/Users/juanf/AppData/Local/agent-checkpoint/self-use/candidate-0.1.1/venv/Scripts/python.exe' -I scripts/installed_smoke.py --output NEW_MCP_REPORT.json
```

Both helpers refuse to overwrite prior reports and retain disposable fixture state
outside the checkout. They do not read .env.local or enable remote providers.

## Promotion, failure and rollback

The independent drill used the frozen candidate source archive extracted into a
separate operator-owned directory, a new development environment, and copied state.
Direct Ruff/format/mypy passed; all 89 tests passed in 137.92 seconds. These commands
ran independently, not through Checkpoint. Installed runtime files were compared
byte-for-byte with the wheel before selecting the candidate. After the drill, all
90 archived files still matched the archive and all 13 runtime Python files matched
archive, wheel and current checkout. This controls candidate inputs for the local
drill; it is not an OS sandbox or the unimplemented isolated_snapshot runner mode.

SQLite backup captured three tasks and 33 events; nine referenced output blobs were
digest-verified into separate state. A disposable launcher selected N, then N+1,
with an identical retained contract. Corrupt fixture state returned exit 5 /
STORAGE_UNAVAILABLE. With the drill launcher disabled, 24 direct contract/service
tests passed in 27.02 seconds. Selecting the preserved N artifact with a fresh copy
of the backup restored the contract successfully. Schema stayed v1; irreversible
migration compatibility was not tested or implied. New candidate records were not
merged into old state. The real active launcher/state were never switched.

The initial offline attempt failed before promotion because the validation helper
omitted UV_CACHE_DIR from its environment allowlist. It used the wrong cache and
could not resolve cached mypy. The corrected retry forwards only that nonsecret
cache path in addition to its OS environment allowlist. Both attempts are retained:
[failed preflight](promotion-attempt-1-2026-09-27.json),
[successful full drill](promotion-drill-2026-09-27.json).

Reproduce from the checkout with a **new**, outside-checkout output directory:

```powershell
uv run --locked --offline --extra jev python -I scripts/promotion_drill.py --candidate 'C:/Users/juanf/AppData/Local/agent-checkpoint/self-use/candidate-0.1.1' --baseline 'C:/Users/juanf/AppData/Local/agent-checkpoint/self-use/build-83114bf8' --active-state 'C:/Users/juanf/AppData/Local/agent-checkpoint/self-use/active-state' --root 'D:/Programming/agent-checkpoint' --output 'C:/Users/juanf/AppData/Local/agent-checkpoint/self-use/NEW-DRILL' --wheel-sha256 8b4d2db9a124117a6e91e6b1248c16481f6d57d65934af0cd2114bf16bb7b33e --source-sha256 265e0e1fb13eb0b8179b4209a16dc7ecea70bb8aa2cd843ea1cbbae406322018
```

The helper refuses existing output directories. Keep the archive, wheel, exported
requirements, backup and reports together. Both successful and failed drill
directories were retained. [Artifact inventory and helper hashes](artifact-validation-2026-09-27.json)
distinguish the frozen source from later validation scripts/documentation. No Git
commit, publication, CI run or global host configuration change was fabricated.

## Limits and prioritized next work

1. Measure and reduce local overhead before wider adoption: long-lived MCP instead
   of many CLI cold starts, then snapshot/Git profiling with unchanged evidence rules.
   The three tiny scenarios cannot predict end-to-end coding outcomes.
2. Validate the Python Jev adapter live with a newly confirmed synthetic data/spend
   budget. Keep remote use disabled meanwhile. Exact upstream weights identity and
   actual billed cost remain unknown; do not send repository code by implication.
3. After explicit setup/restart approval, exercise native Codex MCP; separately
   authorize a Claude test. CLI integration remains the proven host path.
4. Add authenticated manual attestations, explicit interrupted-run reconciliation,
   and stronger declared dependency identity before widening evidence policies.
5. Build routine release/migration automation and stronger isolation before public
   distribution or hooks. This internal drill is not production migration assurance.

The Backend Testing skill guided isolated regression fixtures and credential-free
mock transport tests. Required passes remain deterministic; the system was never
allowed to waive an acceptance criterion just because its own report said ready.
