# Run, inspect and recover the Project Garden laboratory

For a developer using the existing local Windows setup. This guide does not deploy
anything, promote the candidate, or enable another model/telemetry destination.

## Website

Requires Node.js (validated with 24.18.0), no npm packages or remote assets:

```powershell
Set-Location D:/Programming/project-garden-lab
node --test tests/model.test.mjs
node --check app.mjs
node server.mjs
```

Open http://127.0.0.1:4173. Stop with Ctrl+C in that terminal. Existing browser-local
cards survive restart; no real data is used by this experiment. Search, stage/tag
filters and sort are view settings, reset on reload. Edit changes title/stage;
Remove enables one-step Undo until the next removal/reload. Theme is saved separately.
The [website README](D:/Programming/project-garden-lab/README.md) explains keyboard
behavior. Storage failure warns; temporary examples do not overwrite bad stored
data merely by loading. An explicit later save can replace it. Back up anything
you care about before clearing browser site data; clearing is not required recovery.

## Viewer and report

The independently tested 0.1.9 installation is a **read-only viewer**, not the active
supervisor. Its runtime/assets match candidate source. Start a second terminal:

```powershell
& C:/Users/juanf/AppData/Local/agent-checkpoint/harness/garden-lab/candidate-iteration-6/venv/Scripts/python.exe `
  -I -m agent_checkpoint --root D:/Programming/project-garden-lab `
  --state C:/Users/juanf/AppData/Local/agent-checkpoint/harness/garden-lab/state `
  dashboard --port 0 --source-role pinned_supervisor --producer-version 0.1.2
```

Open the full printed local URL including the temporary fragment. Do not publish
or store that capability URL in reports. The page removes it from the address bar;
reload requires reopening the original URL. Port 0 avoids colliding with an existing
viewer. Stop with Ctrl+C. No credential loading is needed for dashboard/report.

Choose a task from the [handoff ID table](../handoffs/2026-09-27-garden-final.md).
The viewer polls every two seconds; Pause stops reads. “Ready” is the **last recorded
completion**, not revalidated approval. Check and operation rows show associations
only inside the returned window. Unknown timestamps/durations stay unknown.
The native overview is local HTML/CSS; expandable/exported Mermaid is source, not
an embedded Mermaid renderer. Metadata JSON and .mmd exports are user-initiated.
See [security, bounds and interpretation](local-dashboard.md).

For a bounded report without the browser:

```powershell
& C:/Users/juanf/AppData/Local/agent-checkpoint/harness/garden-lab/candidate-iteration-6/venv/Scripts/python.exe `
  -I -m agent_checkpoint --root D:/Programming/project-garden-lab `
  --state C:/Users/juanf/AppData/Local/agent-checkpoint/harness/garden-lab/state `
  report --task b48b23d5abdb83a4261a10dd5c971148 --limit 100
```

For Checkpoint's own history, substitute root D:/Programming/agent-checkpoint and
state C:/Users/juanf/AppData/Local/agent-checkpoint/harness/0.1.2/state. Do not point
a candidate execution supervisor at the active checkout/state. A report is safe
read-only inspection, not self-supervision or a permission grant.

## Direct checks and recovery

Development requires Python 3.13, uv, Git, and Node for the offline dashboard DOM
test. Use `uv sync --locked --extra jev` and the direct commands in AGENTS.md.
The actual configured lint/format gates also include scripts. Tests use temporary
repositories and deny external sockets. They need no credentials. Checkpoint is
not recursively invoked from a configured check.

If Checkpoint is unavailable, preserve state and run direct verification. Report
the unavailable harness honestly; do not convert missing evidence to ready. Use
the pinned `scripts/checkpoint.ps1` fallback if its installation is healthy. Use
the same transport for a check/completion pair; changed execution context can
correctly make previous evidence stale. New explicit reruns need new request IDs.
Do not waive freshness or reuse an interrupted request as proof of success.

If the viewer fails, reopen its original capability URL or restart just the viewer.
It cannot repair state, refresh completion or run checks. Keep a stale last-good
display distinct from a successful new read. Do not delete a database to make it load.

## Prepare future promotion — not performed

The final packaged candidate and SHA-256 values are recorded in
[final-audit/validation.json](C:/Users/juanf/AppData/Local/agent-checkpoint/harness/garden-lab/final-audit/validation.json).
Keep the initial iteration installations and the iteration-4 failed/repaired builds.
This goal validates a candidate; it does not authorize replacing pinned 0.1.2.

When the user separately authorizes adoption:

1. Verify the chosen manifest hashes and installed import identity under `python -I`.
   Install its wheel noneditable into a new outside-checkout directory using locked
   dependencies. Never overwrite build-0.1.2 or reuse its venv for candidate edits.
2. Preserve project config, the existing launcher and state with a consistent SQLite
   backup while writers are stopped. Retain the corresponding blobs. Do not copy
   a live database file alone or assume rollback accepts newer state formats.
3. Prepare a new version-pinned launcher with the existing root/state boundaries
   and silent local credential loading. Do not inspect, print or copy key values.
   Exercise the new launcher first with disposable state; preserve Gateway-only
   policy and direct/manual recovery. Do not let startup implicitly call Jev.
4. With compatible state established, explicitly update project-local MCP and CLI
   launcher references together. Add checkpoint_report to enabled_tools only for
   the six-tool candidate. Keep approvals and optional startup behavior unchanged.
5. Reload the Codex MCP connection and verify actual native start/check/complete/report
   calls on disposable acceptance work, including schema 2 output. A standalone
   six-tool smoke is not proof the current Codex connection changed. Do not use CLI
   evidence to hide a native-context mismatch.
6. If acceptance fails, restore the old launcher/config and its matching state
   backup, then reload. Preserve candidate failure evidence. Direct checks remain
   available throughout. Claude/native hooks require their own scoped validation.

These are explicit promotion steps, not an already implemented automated promotion
command or a claim that the candidate is active.
