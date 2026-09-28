# Runtime and pinned self-use handoff

Goal remains active, incomplete. Previous turn made concrete progress, not a wait
or blocker. Read the original goal attachment before continuing. Current code is
candidate work; do not redefine the goal around the now-working CLI.

## Current executable surface

Shared Runtime validates strict wire requests. config.py reads bounded unique-key
JSON, camelCase configuration and approved checks/skills/provider policy. CLI supports
doctor, task start/show/revise, check run, route, review, complete, evidence export,
and mcp --stdio. project.scripts installs agent-checkpoint. MCP uses actual mcp 2.2.0
low-level APIs and flat Pydantic schemas, snake_case internal SDK fields, structured
content plus compact JSON; stdout remains protocol-only. CLI errors are sanitized.

Service revisions are additive and preserve request/scope/required criteria/checks.
Repository mandatory checks cannot be waived. Routing always retains mandatory
skills; optional selection is local keyword/abstention by default. Review is
explicitly unavailable without provider approval and cannot pass required evidence.
Remote calls need launcher-owned spend acknowledgement and exact input digest
approval; wire requests cannot enable them. Only Jev through Vercel is authorized.

Snapshot v2 never opens `.env`/`.env.*`; opaque metadata detects ordinary changes
and tracked credential files are rejected. This is not exact secret-content proof.
Never inspect the real `.env.local`. Fixed cache exclusions remain; state must be
outside the evaluated checkout.

Two post-N changes are present in source, NOT in installed N:

1. runtime.py filters current advisory findings by revision, snapshot and generation;
   historical review events remain available in export. Three regression fixtures
   cover input edits, additive revisions and edit/revert. Advice never passes tests.
2. gateway_transport.py buffers at most 64 KiB response content, closes streams,
   requests identity encoding, rejects compressed responses, preserves timeout and
   one-call/no-retry semantics. Three new stream fixtures plus prior gateway tests.

## Installed build N — keep unchanged

Directory: C:/Users/juanf/AppData/Local/agent-checkpoint/self-use/build-83114bf8

- Python: venv/Scripts/python.exe; invoke with -I -m agent_checkpoint.
- Wheel 0.1.0 SHA-256: 83114bf8ca716c0183d31667fa9e3c6b4184e9c50ea6dffbdce72e8d40087637.
- Wheel, source archive, requirements, config and manifest are preserved there.
- Installed noneditable with offline locked dependencies after direct 77-test,
  Ruff/format/mypy verification. Imports were observed in that venv's site-packages.
- Active state: C:/Users/juanf/AppData/Local/agent-checkpoint/self-use/active-state.
- Candidate fixtures use pytest temp stores. Never point them at active state.
- No Git commit exists; source archive hash, not invented commit, identifies N.

Actual tasks:

- Shadow: 9f8941309f492a5bcea4818e78b22d04, ready after direct checks.
- Follow-up 1: b815f3c9f197edfcf8b324ba8d08715a, N observed two failures/needs_changes,
  then all four checks/80 tests passed and ready after the genuine freshness fix.
- Follow-up 2: 573bdefdea3467f9ad4b3e8cae766fbc, direct red tests → unresolved → fix →
  direct 14 gateway tests → N's four checks/83 tests → ready.

All reports are historical snapshots. Subsequent docs/source edits make those old
results stale; never claim they certify the current checkout. Full sanitized
records and exact artifact hashes are in docs/reports/self-use-2026-09-27.json.
The live AI SDK Jev smoke remains separate; no live model call happened this turn.

Final direct rerun after the two fixes: 83 tests pass in 78.25 s; Ruff lint/format
and mypy (13 source files) pass. JUnit: artifacts/local/self-use-direct-tests.xml.
No verification process remains running at handoff.
Latest unpromoted candidate wheel in dist (also version 0.1.0; distinguish by hash):
`c49a661409dca3becdd24b28859ad2fc62674f64445a9528210b3fc8631b71a4`.
Candidate source archive: `73dc636b624e404c83213ab513ba6fd9ba40e9ed9089330c7bc24dcf42fe8ae4`.
N's original wheel/source archive remain preserved in its separate build directory.

## Native host evidence

Codex 0.158.0-alpha.2.1: help inspected, ephemeral `codex mcp get checkpoint --json
-c mcp_servers.checkpoint.command=... -c mcp_servers.checkpoint.args=...` accepted
the pinned stdio launcher. No persistent/global configuration edited. No tool to
reload this session's MCP surface was available. Real Python MCP client/server
exchange is tested, but native host calls remain unverified. Official docs require
restart after adding a server; see report citation. CLI self-use is demonstrated.
Claude Code 2.1.41 exists; no coding-model session was launched (Jev-only constraint),
so native compatibility is unverified. Hooks stay disabled.

## Next work, in priority order

1. Harden executable/dependency identity in freshness: current check_context hashes
   argv/definition/environment/Python version, not resolved executable bytes.
   Add tests and use N for any further real development if useful. Preserve N.
2. Explicit interrupted-run recovery / process identity review. Current pending
   runs remain unknown; manual escape starts a new same-requirements task after
   confirming old processes stopped. No silent pending→pass path exists.
3. Controlled isolated candidate materialization/promotion and consistent copied
   state, rollback artifact+state, manual disable/broken-runtime escape. Current
   runner explicitly refuses isolated_snapshot. Do not claim isolation via rename
   or a working-tree check, and do not let N+1 certify its own promotion.
4. Three repeatable baseline/intervention scenarios with equivalent fresh starts,
   same checks, all attempts, overhead and unknown usage/costs. Self-use timings
   do NOT satisfy this controlled comparison requirement.
5. Build a distinct final candidate artifact, clean install, direct full verification,
   installed CLI/demo and MCP protocol checks. Preserve source/artifact identities.
6. Complete docs/reports/mvp-validation-report.md and audit the FULL goal before
   update_goal complete. Current report deliberately has unchecked acceptance gates.

Other gaps to keep visible: authenticated manual review absent; init/uninstall
planned only; no exact gateway weights/version pin; Python live compatibility not
tested. Current configuration/manual documents supported subsets without claiming
the whole original backlog done. Broader TASK/HARNESS checkboxes remain unpromoted.

Backend Testing drove test-first isolated fixtures. OpenAI Docs supplied native MCP
setup evidence. No memory guidance was used. No publication, pushes, global host
edits, background jobs or private-data uploads were performed.
