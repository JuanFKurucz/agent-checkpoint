# Iteration 6 — keyboard continuity in the website and observatory

Status: verified. Full pinned gates passed 180 tests in 172.02 s plus lint/format/types;
native completion ready at ba078d618778211148ba4e6a3605be49a6c1ced5549b0839fbccb6339b9d1c5f.
Installed six-tool MCP passed in 7.367538 s, 19 runtime/asset files matched. Evidence:
external garden-lab/candidate-iteration-6/validation.json. Candidate 0.1.9 is not promoted.

## Paired proposals and observed before/after

Website: saving an edit left document focus on BODY; Undo focused the first card,
not necessarily the restored one. Return to the relevant visible edit button, or
search if filters hide it. Keep native dialog cancel/escape behavior, tab order,
visible focus and announcement text. Risks: focus stealing or an inaccessible
filtered-out target. A missing focus helper first failed an isolated test.

Browser verified keyboard Enter opens editing; saving Field notes returned to its
edit button. Renaming a Zinnia match so it no longer matched returned focus to search
with zero of three projects. Delete moved to Undo; keyboard undo returned to the
second card, not the first. Changing the filter before Undo recovered to search.
Cancel and Escape returned to the opener. Skip to projects focused the board.

An additional browser check found native Shift+Tab from the first modal field left
document focus. A second red regression drove explicit boundary wrapping, without
intercepting Escape or interior navigation. Browser verified first→last with Shift+Tab
and last→first with Tab. Seventeen website tests pass. Mobile dialog width 351 px in
a 390 px viewport, document width 390 px; its visible focus and layout were inspected.
This is a bounded keyboard/visual check, not full screen-reader or accessibility certification.

Checkpoint: installed 0.1.8 task-button focus changed BUTTON→BODY after a 2.3-second
poll. Candidate 0.1.9 keeps existing button nodes on unchanged polls; changed order
restores the retained button with preventScroll. Removed buttons fall back to the
Pause/Resume control. External focus is never captured. An offline minimal-DOM
regression first failed because the new rendering boundary was absent, then passed
retained/reordered/removed/external-focus and selected-state cases. Pytest invokes
this Node regression; no network, credentials, state or provider is involved.

Installed candidate browser verification retained the task button after polling,
kept trace-filter focus, and in a synthetic in-page reorder/removal fixture retained
the exact button object then recovered to Pause. The disposable fixture viewer
does not supervise development. All six candidate MCP tools also passed their
independent installed exchange. Dashboard focus does not change evidence authority.

## Identity, timing and routing

Repository task f715fe39c7c493bee103ba31bf0df892; website task
b48b23d5abdb83a4261a10dd5c971148. Both registered and routed before edits.
Website request IDs garden-iteration-6 / garden-iteration-6-route-1; remaining
check/run IDs are in external evidence/iteration-6-*.json. Native repository final
gate IDs and timings are in candidate-iteration-6/validation.json.

First website red began 02:44:39.431Z; first green 02:45:27.278Z: 47.847 s elapsed,
not pure coding effort. Further browser work found the dialog issue, so this is
not total feature time. Dialog red/green began 02:46:39.466Z / 02:46:40.951Z with the
patch already prepared. Final direct 17-test command took 0.338100 s. Whole design,
implementation and browser effort is unknown; do not infer savings from these samples.

Jev repository decision 3feff36f-9913-4a17-8de0-cf4b6231d85d selected documentation,
393/39 tokens, 0.674050 s, confidence 0.66. Website decision
4f186aa0-8ea7-42a9-ba85-0169bba180e6 selected backend-testing, 391/41 tokens,
0.586111 s, confidence 0.18. One physical Vercel request per task; no review,
retries, fallback or hosted telemetry. Billing unknown. No additional decision
benefit established: tests were already mandatory. Backend Testing drove isolated
regressions; Agent Browser exposed the modal gap; Frontend Design preserved the
existing layout and visible-focus treatment.

## Helpfulness, recovery and next proposals

Checkpoint recorded and gated the declared checks; it did not find the focus defects.
Browser evaluation did. The viewer improvement removes a reproduced interaction
failure, not model latency or cost. The Node DOM fixture is intentionally small and
does not substitute for browser verification. The website server needed a controlled
restart to serve the new focus module; no data was reset. Two exploratory reads of
nonexistent package.json/conftest.py produced harmless lookup errors, not product failures.

All six bounded feature pairs are now implemented, subject to final verification.
Next website proposal (future work, not an extra loop iteration): create-new-project
flow with validation and keyboard handling. Next Checkpoint proposal: measure
check-startup/snapshot overhead and evaluate a narrowly scoped batching design;
preserve freshness and explicit execution. Final assessment/audit will prioritize
this against authoritative evidence bindings and friendly task navigation.
