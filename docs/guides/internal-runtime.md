# Internal runtime: explicit CLI and MCP

Candidate update: 0.1.3 returns [completion schema 2](../reference/completion-diagnostics.md)
with typed diagnostics and validated output. Active supervisor 0.1.2 still returns
schema 1; see [status](../status.md). Review commands below demonstrate an optional
experiment, not the routine workflow. Required readiness remains deterministic.

Status: validated internal MVP, with a subsequently enabled repo-local 0.1.2 harness.
See [active harness](active-harness.md) for the current pinned launcher and live Jev
approval. Historical validation artifacts remain pinned to their recorded versions.
Python 3.13 is required. Run `uv sync --locked --extra jev` from the repository.
No credential is needed for the default offline workflow.

## Configuration and trust

`checkpoint.json` is the reviewed launcher-owned JSON configuration. Configuration
uses camelCase; tool payloads use snake_case. The current supported config is
schemaVersion, mode (observe/advise), checks, skills and provider. Unknown fields
and duplicate JSON keys fail; the broader research YAML is not an accepted input.

Checks contain argv, cwd, timeoutSeconds, maxOutputBytes, envAllow, executionMode,
and required. They execute native programs without a shell. Windows .cmd/.bat
wrappers are unsupported. Four approved checks in this repository invoke uv
offline: Ruff lint, Ruff format check, mypy, pytest. Required configured checks are
always included; callers cannot waive them. Config changes invalidate existing
task policy. Review modified configuration before starting a new task.

State is stored outside the checkout, by default below LOCALAPPDATA/agent-checkpoint
on Windows. `--state` explicitly selects a separate store. Never point candidate
tests at active self-use state. Local filesystem access is the trust boundary; this
is not a sandbox against a process that can edit the same files or database.

## Try a task

Create a request Markdown file and a contract JSON file outside the checkout (so
changing them does not accidentally change task inputs). The contract can be:

```json
{
  "request_id": "my-task-v1",
  "criteria": [
    {"id": "behavior", "text": "Required behavior has passing regression tests", "check_ids": ["tests"]}
  ]
}
```

Run these from the repository; replace TASK with the returned opaque task ID:

```powershell
uv run --locked --extra jev agent-checkpoint doctor --json
uv run --locked --extra jev agent-checkpoint task start --request-file REQUEST.md --contract-file CONTRACT.json
uv run --locked --extra jev agent-checkpoint route --task TASK --kind skill
uv run --locked --extra jev agent-checkpoint check run --task TASK lint format types tests
uv run --locked --extra jev agent-checkpoint complete --task TASK --json
uv run --locked --extra jev agent-checkpoint review --task TASK
uv run --locked --extra jev agent-checkpoint evidence export --task TASK --format jsonl
```

Use global `--root`, `--config`, `--state` options before the subcommand when calling
from another directory or an independently installed runtime. Completion does not
run checks or call providers. Review explicitly returns PROVIDER_DISABLED by
default. Mechanical check bindings must use satisfaction_rule=approved_checks
(the default). A passing generic test suite is only as good as its actual coverage;
it does not independently establish a human's interpretation of every requirement.
Required manual criteria remain unknown until an authenticated attestation surface
is implemented; an agent cannot submit a claimed human pass through these tools.

`task show TASK` reads the latest contract. `task revise TASK --contract-file FILE
--expected-revision N` accepts additive revisions only. Supply a stable --request-id
to replay safely; CLI generates one when omitted. Check runs also accept an optional
--expected-snapshot-id. Replaying a pending request does not execute it again.

Exit codes: 0 successful operation/ready; 2 invalid input/configuration; 3 failed
check/needs_changes; 4 pending/unknown/unavailable/unresolved; 5 storage/runtime or
scope/precondition error. Every command emits JSON except evidence export (JSONL)
and MCP (protocol only). Doctor reports configured capability, not native-host or
live-provider certification.

## MCP

Launch `agent-checkpoint --root REPO --config CONFIG --state STATE mcp --stdio`.
The five tools are checkpoint_start_task, checkpoint_route, checkpoint_run_checks,
checkpoint_review and checkpoint_completion. `tools/list` exposes authoritative
schemas. Tool arguments cannot override roots, commands, provider policy or
evidence provenance. MCP gets structured content and JSON text. Check failures are
domain results, not transport errors. Invalid requests get sanitized errors.

A real local client/server exchange has been tested with mcp 2.2.0 on Windows.
This is not yet proof of native Codex or Claude Code integration. No global host
configuration or hooks are changed by this CLI. Planned init/uninstall commands
are not implemented; explicit launcher configuration/manual removal is the current
integration and recovery path.

## Provider and privacy

Only Jev through Vercel AI Gateway is supported. The optional Python adapter fixes
the endpoint, model alias and AI_GATEWAY_API_KEY environment name; no other models,
direct TypeSafe endpoint, redirects or implicit retries. An enabled provider also
needs remoteAllowed, spendAcknowledged and either exact approvedInputDigests or
explicit approvedPayloadKinds (single_route/criterion_evidence) in trusted config.
Payload-kind approval is opt-in and defaults empty. This is a local scope gate,
not a financial hard-cap mechanism. Keep it
disabled until the exact request data and spend are approved. Never paste or inspect
keys in agent tools. The runtime does not load `.env.local` automatically.

Snapshot v2 never opens `.env` or `.env.*`; it includes only opaque metadata identity
and rejects tracked credential files. This detects ordinary file changes but cannot
prove identical secret content. Other relevant ignored inputs are content hashed.
Generated cache/build directories are excluded; tracked inputs there are errors.
Working-tree checks detect ordinary edits, not hostile metadata preservation or
concurrent changes after a report. Isolated execution is still explicitly unavailable.

Version 0.1.1 additionally fingerprints the resolved check executable and Python
launcher (path, SHA-256 and file-generation metadata). It recomputes that identity
after execution and when reusing evidence. Relative executable paths resolve from
the configured check directory. Unreadable or oversized executable identity is
unavailable, not a pass. This does not attest every loaded DLL, interpreter module,
external service or excluded dependency directory; preserve the locked environment
and use a fresh install for promotion. Reports are observations, not filesystem locks.

## Recovery

Use direct AGENTS.md commands if Checkpoint fails. Stop the stdio process or remove
the explicit launcher entry to disable it; there are no hooks to bypass. Preserve
the outside-checkout state directory for diagnosis. Do not delete or weaken contract
evidence to force ready. Interrupted pending runs remain unknown; until explicit
recovery is implemented, register a new task with the same substantive requirements
and rerun checks after confirming old check processes have stopped.

The offline interrupted-request fixture confirms that retrying the same request
returns pending without executing it, and even a later successful run cannot hide
the unfinished attempt. A new task with identical substantive criteria can recover;
the old task and its unresolved history are retained.

## Repeatable workflow comparison

Use an independently installed Python interpreter, not an editable checkout, for
the measured runtime:

```powershell
& INSTALLED_PYTHON -I scripts/measure_scenarios.py --python INSTALLED_PYTHON --output NEW_REPORT.json --repetitions 3
```

Replace both INSTALLED_PYTHON occurrences with the absolute interpreter path.
The command creates and retains disposable repositories outside the checkout,
finishes all baseline trials first, then runs Checkpoint trials with identical
acceptance commands. Scenarios are passing, failure/repair, and stale/repair.
Every subprocess attempt, exit, output and duration is saved, including failures;
existing report paths are refused. Setup time is excluded, full workflow time is
included, and providers remain disabled. This small fixed-order workflow experiment
does not measure autonomous coding quality or prove performance improvements.

## Candidate promotion and rollback drill

`scripts/promotion_drill.py` is an independent operator tool, not a Checkpoint
readiness command or host hook. Use its `--help` and the exact invocation in the
[operating report](../reports/mvp-validation-report.md). It requires preserved N and
candidate build directories, expected wheel/source hashes, an existing active-state
path to back up read-only, the original repository root, and a fresh output directory
outside both. Keep UV_CACHE_DIR available when using the configured offline cache.

It extracts and checks frozen source, verifies installed code against the wheel,
backs up SQLite consistently, verifies referenced blobs, and switches only a
disposable launcher. Corrupt fixture state must fail; manual disablement and direct
tests must still work; rollback selects N with backup-derived state. Do not use this
script as a production migration tool. The real launcher is never switched, and
irreversible schema migration requires a separate reviewed plan. Preserve all output
directories, including failed attempts, until their evidence is no longer needed.
