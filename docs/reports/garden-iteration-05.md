# Iteration 5 — combined filters and truthful trace pairing

Status: verified. Pinned gates passed 179 tests in 174.78 s, lint/format/types;
native completion ready at 5df3f56f5b90377b154ea669d66cacd542800749db9c0a4d4cd57a631d620b27.
Installed six-tool MCP smoke passed in 8.682588 s and 19 runtime/asset files matched.
Evidence: external garden-lab/candidate-iteration-5/validation.json. Not promoted.

## Paired proposals and observed results

Website: search title/story/tag, combine exact stage and tag filters, preserve
saved cards and sorting, and distinguish no matches from an empty saved board.
Risks were accidental persistence mutations, broken edit/delete targeting, and
confusing zero matches with deleted data. The missing filter export first failed;
15 model tests now pass, including case/whitespace, three searchable fields,
AND combinations, empty input, nonmutation and sort compatibility. Browser tests
observed route search, Harvest plus Outside, Seed yielding zero of three, clear
restoring all three without a data reset, and delete/undo of the filtered card.
Editing that card to Walk a new route retained the matching view. Search-to-stage-
tag keyboard order worked. A 390 px viewport had 390 px document width; desktop
and mobile screenshots were visually inspected. View settings reset on reload.

Checkpoint: completed check starts still displayed INTERRUPTED_OR_RUNNING and
legacy zero durations in the old dashboard. Annotate matching starts/finishes
within the bounded report, without rewriting events or claiming liveness. Tests
first reproduced missing pairing fields and later caught an incomplete-association
group being paired too optimistically. Pairing now distinguishes observed pairs,
counterparts not observed in the returned window, ambiguity, and unavailable
associations. Duplicate/reversed sequences or conflicting associations stay
ambiguous. Check/operation IDs never cross-pair. Started durations remain unknown.
Raw stored status/reason remains in JSON; display labels do not alter readiness.

The focused reporting/dashboard/MCP suite passed 49 tests in 17.32 s. Direct Ruff,
format, mypy and dashboard JavaScript syntax checks passed before final gates.
The independent installed replay uses synthetic stored events, not real executions:
completed pair, unmatched start, duplicate starts, database unchanged, provider zero.
See external evidence/iteration-5-pairing-before.json and the after record when
validated. The old installed 0.1.7 read took 0.005658 s; no performance gain is claimed.

## Measurements and supervision

Repository task 285954b64103df39a1856808b97d7d5b; website task
6cb7e600939c37fe3e1011727b87363d. Both registered and routed before edits.
Pinned 0.1.2 native MCP supervises repository gates; pinned CLI supervises website
checks. Candidate tests use disposable state and are never the active supervisor.
Exact request/run IDs and durations are in external evidence/iteration-5-*.json
and candidate-iteration-5/validation.json. The website red command began
02:27:58.715Z, green began 02:28:43.950Z: 45.235 s elapsed, not pure coding time.
The direct green command took 0.3492145 s. Overall implementation effort is unknown.

Jev repository decision 360552e2-339d-4761-a224-c83b560c62dc selected documentation,
387/39 tokens, 6.128870 s, confidence 0.44. Website decision
dbb8e95f-3c25-4bc3-afb2-714ec7613b68 selected frontend-design, 399/41 tokens,
0.630458 s, confidence 0.36. One physical Vercel request per substantive task;
no review, retries or fallback. Billing unknown. Mandatory testing applied
independently. Frontend Design informed the responsive grouped toolbar while
preserving the existing botanical design. No measured routing-quality benefit.

## Usefulness and next pair

This improves interpretation, not detection or readiness authority. Raw start
records are still unknown, but a finish observed in the same window is now clear.
Bounded windows are explicitly incomplete observations. Browser work independently
found two focus problems; check status alone did not find them. Backend Testing
guided isolated regression coverage; Agent Browser supplied interaction evidence.

Next website proposal: keyboard/focus recovery after edit, delete/undo and filtered
changes. Saving the edited card currently leaves document.activeElement as BODY.
Next Checkpoint proposal: preserve task-button focus during polling. In installed
0.1.6, focusing task 64017bfe… yielded BUTTON, then BODY after a 2.3-second poll.
Both are observed, not inferred defects. Fix focus without moving it unexpectedly,
changing selected tasks, or introducing any mutation/provider path to the viewer.
