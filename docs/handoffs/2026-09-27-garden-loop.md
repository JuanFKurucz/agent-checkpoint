# Project Garden goal — ongoing handoff

Historical incremental handoff. Superseded for current use by the
[final handoff](2026-09-27-garden-final.md), which retains the task/version catalog
and final evidence links. Pending statements below describe earlier points in time.

Full objective: [six-iteration plan](../planning/project-garden-loop.md). Goal remains
active; baseline and iterations 1–5 are verified. Iteration 6 focus continuity is
under validation; consult candidate-iteration-6/validation.json for final gates
when present. The final assessment and goal audit remain required.

## Current locations and identities

- Website D:/Programming/project-garden-lab, separate Git workspace, no commits.
- External evidence/state/driver C:/Users/juanf/AppData/Local/agent-checkpoint/harness/garden-lab.
- Pinned supervisor unchanged 0.1.2. Native MCP works for start/route/checks/complete.
- Candidate source 0.1.9, adds polling focus continuity; not promoted.
- Baseline repository task 35b957317500d92205cb776aa9da3a7c; baseline website task
  71d2f341a55deb34b29dc954fdc6fb68. Both ready at their historical snapshots.
- Iteration 1 repository task 7d412f915d3ea4ecfb21a45c4ed73701; website task
  71469e61b4c66a82b47e26b025c99eb3. Website checks+completion ready.

## Work and evidence

Read [baseline](../reports/garden-baseline.md) and
[iteration 1](../reports/garden-iteration-01.md). Seven website tests pass; browser
edit/reload/mobile and corruption recovery observed. Candidate focused runtime,
MCP and scope tests: 27 passed in 36.97 s. A direct lint check found a long notice
string; it was shortened before final gates. No criteria weakened or checks removed.
All four live routes used Jev/Vercel only, one physical request each on four separate
substantive tasks, no retries or reviews, billing unknown. Exact decisions/tokens
are in reports. Testing instructions applied independently of routing advice.

## Continuing safely

Inspect external candidate-iteration-1/validation.json when present for final native
gates and separately installed artifact smoke results; do not infer it exists.
External files avoid a check/report edit cycle changing the evaluated snapshot.
Do not rerun completed calls using existing request IDs or overwrite evidence files.
The driver rejects duplicate evidence labels. Test suites never invoke Checkpoint.

Iteration 1 final proof: external candidate-iteration-1/validation.json (118 tests,
native ready and installed MCP pass). Iteration 2 tasks: repository
6f7bb5a3b75f7e24c0fd0afc2bd801a0, website 809c7c3777cdec26924d292efe0e1759.
Read [iteration 2 report](../reports/garden-iteration-02.md) and the
[reporting manual](../guides/history-reporting.md). Nine website tests and browser
theme/reduced-motion checks pass; 38 focused repository tests pass.
Next: confirm iteration 2 final gates externally, then deletion/undo on the website
and local dashboard/operation traces in Checkpoint. Shuffled
website order is fixed in the plan. Register the next substantive task before edits.
Use candidate disposable state, never candidate-as-active-supervisor. Native MCP
and CLI may have different execution context identities; use consistent transport
for check/completion pairs. No canonical profile fix has been implemented.

Update: iteration 2 validation.json proves 134 tests and installed six-tool MCP pass.
Iteration 3 tasks: repository 208460e2ba421d0b7efa7ed6ab8eeafc, website
f67856b42120f6736bc03a71cf6fe9da. Read its report and the local-dashboard guide.
Candidate-iteration-3/validation.json will contain final results when verified.
Next paired work is website sorting plus execution-context mismatch diagnosis.
Do not promote the candidate or use it as the active supervisor.

Iteration 3 final evidence: 159 tests/151.62 s, native ready, six-tool installed MCP
pass, 19 runtime/asset files matched. Browser/export proof in its validation.json.
Iteration 4 repository task a1583837fa297ac0a60aacd81b711d21; website task
64017bfe776ea6d3e3e81c0a91e99ec4. Read [iteration 4](../reports/garden-iteration-04.md).
Its candidate context probe demonstrates improved explanations, not relaxed freshness
or a diagnosis of the earlier real host mismatch. Next pair: search/combined filters
and clear historical start/finish pairing in the dashboard. One Jev request per task;
tokens/latency/decision IDs and two agent CLI usage mistakes are recorded in the report.
Active native MCP remains five pinned 0.1.2 tools, not the six candidate tools.

## Local processes

Iteration 5 final manifest proves 179 tests/174.78 s, native ready, 19 matched
runtime files and installed six-tool MCP smoke. Iteration 6 repository task
f715fe39c7c493bee103ba31bf0df892; website b48b23d5abdb83a4261a10dd5c971148.
Seventeen website tests and real keyboard checks pass; installed 0.1.9 focus behavior
and six-tool MCP exchange pass. One Jev request each; exact IDs/metrics in its
[report](../reports/garden-iteration-06.md). Final evidence in its external manifest.
Website restarted for the new focus module: exec 32636, port 4173. Candidate 0.1.8
read-only live viewer exec 88038, port 4177; old 0.1.6 viewer exec 28606, port 4175.
Iteration 6 disposable viewer uses 4176 temporarily; check manifest for stopped state.

Iteration 4 final manifest proves repaired full gates: 167 tests/170.26 s, ready,
19 installed files matched, six-tool MCP smoke passed. Use its repair/venv artifact,
not the earlier failing build. The original failures remain preserved.
Iteration 5 repository task 285954b64103df39a1856808b97d7d5b; website task
6cb7e600939c37fe3e1011727b87363d. Read [iteration 5](../reports/garden-iteration-05.md).
Fifteen website tests and browser combined-filter/edit/delete/undo checks passed;
49 focused Checkpoint tests passed. One Jev request each, IDs/tokens/latencies in
the report. Next pair is website edit/undo focus recovery and dashboard polling
focus preservation, both reproduced in the browser. Final iteration 5 package,
gates and completion are in its external validation manifest when present.

Website server started as a foreground task command `node server.mjs`, loopback
127.0.0.1:4173 (exec session 20399 at creation). Browser session is garden-lab.
Check current handles before reuse; they may be stopped before the turn ends.
Manual stop: Ctrl+C in the owning terminal; `agent-browser --session garden-lab close`.
No hosted telemetry, service installation, recurring jobs, publication, or promotion.

Installed 0.1.6 read-only dashboard was live at 127.0.0.1:4175 (exec 28606), viewing
website history. Stop via Ctrl+C in owning terminal. Prototype 4174 and disposable
fixture 4176 were stopped after iteration 3. Session URLs contain temporary local
capabilities and are not stored in docs. Revalidate handles before claiming liveness.
