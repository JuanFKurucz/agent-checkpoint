# Project Garden — final handoff

The baseline and six feature pairs are verified. Read the
[assessment](../reports/garden-final-assessment.md),
[completion audit](../reports/garden-completion-audit.md), and
[operations guide](../guides/garden-lab-operations.md). Final closure evidence lives
outside the evaluated checkout in garden-lab/final-audit/validation.json; it must
exist with passing results before treating documentation closure as complete.

## Identities and locations

- Checkout: D:/Programming/agent-checkpoint; candidate 0.1.9, Python 3.13.11, uv.lock.
- Website: D:/Programming/project-garden-lab; separate Git root, Node 24.18.0.
- Evidence: C:/Users/juanf/AppData/Local/agent-checkpoint/harness/garden-lab.
- Active supervisor: harness/build-0.1.2/venv, noneditable site-packages; five native
  MCP tools verified. State harness/0.1.2/state. CLI fallback is scripts/checkpoint.ps1.
- Website supervisor: the same pinned 0.1.2 interpreter through external run.mjs;
  separate garden-lab/state. Candidate never became either active supervisor.
- Installed viewer: garden-lab/candidate-iteration-6/venv, version 0.1.9, six-tool
  standalone MCP smoke 7.367538 s, 19 runtime/asset files matched. Native candidate
  MCP is not loaded. Final packaged snapshot lives under final-audit (manifest).
- Work remains untracked/uncommitted as on entry. No push, publication or global
  host change. Do not clean or reset these workspaces without explicit authorization.

## Task / iteration catalog

| Slice | Website task | Repository task | Report |
|---|---|---|---|
| Baseline | 71d2f341a55deb34b29dc954fdc6fb68 | 35b957317500d92205cb776aa9da3a7c | [Baseline](../reports/garden-baseline.md) |
| 1 | 71469e61b4c66a82b47e26b025c99eb3 | 7d412f915d3ea4ecfb21a45c4ed73701 | [Recovery/scope](../reports/garden-iteration-01.md) |
| 2 | 809c7c3777cdec26924d292efe0e1759 | 6f7bb5a3b75f7e24c0fd0afc2bd801a0 | [Theme/reports](../reports/garden-iteration-02.md) |
| 3 | f67856b42120f6736bc03a71cf6fe9da | 208460e2ba421d0b7efa7ed6ab8eeafc | [Undo/observatory](../reports/garden-iteration-03.md) |
| 4 | 64017bfe776ea6d3e3e81c0a91e99ec4 | a1583837fa297ac0a60aacd81b711d21 | [Sorting/context](../reports/garden-iteration-04.md) |
| 5 | 6cb7e600939c37fe3e1011727b87363d | 285954b64103df39a1856808b97d7d5b | [Filters/pairing](../reports/garden-iteration-05.md) |
| 6 + closure | b48b23d5abdb83a4261a10dd5c971148 | f715fe39c7c493bee103ba31bf0df892 | [Focus](../reports/garden-iteration-06.md) |

Every candidate-iteration-N/validation.json is verified. Iteration 4 initially failed
format and a regression; its repair/venv is the validated 0.1.7, not the initial
artifact. Final feature suite: 180 tests/172.02 s and native ready at
ba078d618778211148ba4e6a3605be49a6c1ced5549b0839fbccb6339b9d1c5f.
Final documentation changes require fresh gates, stored in the closure manifest.
Website latest completion ready at a257480fba4591157d217f04090d0e453bb33cf38cdf4f7923d9d25d0e893aff;
17 tests, unit run fdb7d183-26a1-4c4c-b697-1bbfae85cec4 and syntax
06e431de-ccf4-4dfc-b230-a922c108f435. Browser verification is separately documented.

Jev: one Vercel request for every table cell/task, 14 total; 5,533 input / 563 output
tokens, billing unknown. Exact decisions/latencies are in the slice reports and
state. No retries, reviews, alternate endpoint/model or hosted telemetry. Closure
reuses the registered iteration-6 task and does not call Jev again. Tests/probes
and report reads require no credentials or live provider. Never inspect .env.local.

## Running local processes

At final feature handoff, website was live on 127.0.0.1:4173, exec session 32636,
browser garden-lab. Read-only installed 0.1.9 viewer was live on 127.0.0.1:4178,
exec 41191, browser checkpoint-final. Final audit rechecks both; see its manifest
for current observed status. Temporary/old viewers 4175, 4176, 4177 were stopped.
Stop either live process with Ctrl+C in its owning terminal (or interrupt that
exact still-live tool session). Close the two browser sessions if no longer needed.
Do not kill unrelated Node/Python processes by name. URLs' local capabilities are
not stored here. No recurring jobs, background agents or installed services exist.

## Continue after this goal

Use the assessment priorities rather than restarting the six completed iterations.
Evidence-authority design, measured overhead, browser automation and safe friendly
task labels are next candidates. Website create-new-project is proposed, not part
of this completed six-pair scope. Native candidate adoption requires the separate
promotion procedure and authorization. Keep direct checks/manual recovery usable.
