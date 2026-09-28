# Iteration 3 — delete/undo and a local observatory

Status: verified. Pinned native gates passed: 159 tests in 151.62 s plus lint,
format and types; native completion ready at b8912749750ac649b3b7cd2265f0154360c5f86eb785471a8aa9cf6ae7dc97f8.
Installed six-tool MCP smoke passed in 8.672465 s, all 19 runtime/asset files matched.
Final evidence: external garden-lab/candidate-iteration-3/validation.json.

## Paired proposals and implementation

Website: delete a card, undo the most recent deletion at its original position,
preserve intervening edits, persist results and announce changes. Undo lasts until
the next deletion or reload, stated in the UI. An empty board has an explicit sample
restore action, not automatic reseeding. Two tests first failed for missing exports;
all eleven model tests pass. Browser deletion moved focus to Undo and stored two
cards. Editing another card, undoing, then reloading preserved the edit and original
three-card order. No existing nonempty user board is reset automatically.

Tool: local read-only dashboard, Mermaid lifecycle source and timestamped operation
events. Iteration 2 reduced raw-data inspection to one metadata report, but still
required reading JSON to understand history. The viewer now organizes tasks, recorded
checks/completion, Jev usage, reasons and actions, and filterable trace events.

The HTTP tests first failed because the viewer did not exist; the two initial trace
tests then failed because timestamped operations were absent. Focused dashboard,
runtime, reporting and MCP suite passed 62 tests in 54.32 s before one extra pending
replay regression. Review found that pending replies omit task_id; trace completion
now retains the associated task so those calls do not leave misleading open starts.
That added case passed independently and in the final full suite.

## Observed browser behavior

The viewer read real pinned website history and switched between task IDs. It showed
ready with an explicit historical/not-revalidated warning, not current approval.
It displayed the new website check/completion records after polling. Browser offline
emulation produced a stale last-good warning without clearing the report; restoring
network recovered polling. Pause was visible and explicit. Legacy timestamps remain
unknown. Mermaid source is exportable; the local overview is HTML/CSS, not a claim
that the Mermaid rendering library is installed.

Installed viewer verification showed 11 timestamped candidate operation records,
transport and producer identity, with operation filtering. At 390 px viewport the
page width was 390 px. JSON and Mermaid downloads were verified on disk in the
normal Downloads folder; automation's redirected AppData destinations canceled
saving after all bytes arrived. No product change was needed for that recovery.
Prototype and fixture viewers were stopped; installed viewer 4175 and website 4173
remained live at handoff. Session capability URLs are deliberately not recorded.

## Evidence and provider use

Repository task 208460e2ba421d0b7efa7ed6ab8eeafc. Website task
f67856b42120f6736bc03a71cf6fe9da. Website run IDs:
b282f640-0b06-497d-b21b-23070357f45d (unit),
3a598165-5212-4c2b-98db-a1bbab711ccd (syntax).
Pinned website checks 3.808374 s and completion 3.120945 s; ready for declared checks.
Direct eleven-test command 0.308534 s. The recorded first red→green interval is
1.3 s because the implementation patch was already prepared; it is **not** a claim
that the feature took 1.3 s to design. Whole implementation effort is not measured.

Jev repository decision 86cb5b40-afd5-40df-a577-96ade4b8e73a: backend-testing,
411/40 tokens, 0.574277 s, confidence 0.33. Website decision
76beea93-3f69-42ad-becf-c0bf35be42a7: backend-testing, 397/41 tokens,
0.767795 s, confidence 0.87. One physical request per task, no retries/reviews/fallback;
billing unknown. Browser, dashboard polling and candidate tests make no provider calls.

## Usefulness and limitations

The dashboard makes diagnostic information visible without new execution. It does
not discover missing tests, prove semantic coverage, or establish a process is alive.
Tracing adds writes/overhead on candidate operations; no performance improvement is
claimed. Pinned 0.1.2 remains active, without new traces or tools. Candidate 0.1.6 is
independently tested, not promoted. Trace-write failures are sanitized warnings and
can create gaps. Source-role labels are operator declarations, not attestation.

The observability skill guided bounded metadata and explicit unknowns; frontend
design guided the restrained instrument-panel layout; Backend Testing drove isolated
negative tests; browser skill guided observed-ref interaction and screenshots.

## Next paired proposal

Website iteration 4: sorting (fixed shuffled order).
Tool: execution-context mismatch diagnostics. Earlier native/CLI evidence became
stale with identical workspace snapshots, but the old runtime exposed only an
aggregate context digest. Add safe component fingerprints and changed-component
names without logging environment values or relaxing freshness. Use the dashboard
to explain the controlled mismatch experiment and required follow-up checks.
