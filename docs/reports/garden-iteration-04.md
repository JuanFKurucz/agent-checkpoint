# Iteration 4 — sorting and stale-context explanations

Status: verified after repair. Final pinned gates passed 167 tests in 170.26 s plus
lint/format/types. Native completion ready at ae645756026332ea6c9454700ded506623ca4befea04cc2b12aea31d51876626.
Full evidence is external garden-lab/candidate-iteration-4/validation.json. Repaired
installed six-tool MCP smoke passed in 8.285719 s; all 19 runtime/asset files matched.
Source 0.1.7 remains a candidate; supervisor stays pinned 0.1.2.

## Paired proposals and acceptance

Website: stable title and growth-stage sorting as a view, preserving saved order,
edits and delete/undo. Risks: mutating the stored array or acting on the wrong card
after a reorder. Thirteen model tests pass; two new tests cover numeric/case-insensitive
stable ordering, original order, no mutation, empty input, invalid mode and undo.
The import first failed because sortCards was absent. Browser stage sorting moved
the Seed card first; editing it to Harvest repositioned it. Title sorting, deleting
and undoing that card retained its ID and order. Reload restored original view order
and persisted edits. The UI explicitly says the view preference resets on reload.

Checkpoint: the earlier native/CLI mismatch only exposed EVIDENCE_STALE. Add safe
component diagnostics without relaxing readiness. Two first tests reproduced the
missing detail for environment versus file mutation, then passed after implementation.
The focused service/report/diagnostics suite passed 45 tests in 40.19 s. Tests include
legacy absent fingerprints, runtime/executable/launcher changes, redacted reporting
and unchanged readiness semantics. No raw values or executable paths are retained
in the new fingerprint fields. An import-order lint error was corrected.

## Controlled installed replay

The same script ran with independently installed 0.1.6 and 0.1.7, each in its own
synthetic repository/state. One explicit check passed; changing synthetic LANG made
completion unresolved in both, with only two check events (start/finish): completion
did not rerun. 0.1.6 had no context explanation; 0.1.7 reported environment changed
and workspace file metadata unchanged. Whole probe times were 4.086143 and 4.531069 s.
These are single descriptive samples, **not a speedup or a causal overhead estimate**.
The probe does not establish which component caused the historical real host mismatch.
That earlier record cannot be retroactively diagnosed. See [guide](../guides/context-diagnostics.md).

The first full native gate found 165 passing tests and one regression: an existing
alternate-context fixture crashed while creating diagnostic fingerprints. It also
found formatting missing in the probe script (the configured gate includes scripts,
unlike the narrower direct command). Native completion correctly returned needs_changes.
Unsupported/extended context shapes now yield unavailable diagnostic fingerprints;
the full original context still determines freshness. The existing regression was
preserved and a partial/extended-layout case added. Repaired artifacts are installed
separately under candidate-iteration-4/repair; the initial build is retained, not promoted.

## Evidence and friction

Repository task a1583837fa297ac0a60aacd81b711d21; website task
64017bfe776ea6d3e3e81c0a91e99ec4. Request IDs and exact run IDs are retained in external
evidence/iteration-4-*.json and the candidate validation manifest. Website red test
started 02:13:51.702Z; green command started 02:14:14.290Z (22.588 s elapsed, not pure
coding effort). Direct green command took 0.311373 s. Browser work/checks are separate.
Whole tool implementation effort was not measured.

Two avoidable agent CLI mistakes used --criteria-file instead of --contract-file,
and --checks instead of positional check IDs. Both exited at argument parsing and
executed no checks/provider calls. Help and corrected invocations recovered; failed
records remain. Website routing occurred after its new tests were written, before
implementation: a sequencing deviation, not a claim of full protocol compliance.
Backend Testing already applied independently of routing.

Jev repository decision dccde8bc-5cae-4ca7-a086-224b7a86863c selected backend-testing:
384/40 tokens, 0.822558 s, confidence 0.27. Website decision
565fe20f-68d4-4bd3-b250-eb27d1bd4d07 selected backend-testing: 393/41 tokens,
0.601226 s, confidence 0.22. One physical request per substantive task, no retries,
reviews or fallback. Billing unknown. Advice did not change the already-required
testing approach. Candidate fixtures and dashboard made no provider calls.

## Usefulness and next pair

The controlled context change was genuinely caught before a ready claim in both
versions. The candidate adds actionable cause categories, not better detection.
It directs inspection toward execution context, without pretending to know the raw
value or allowing automatic repair. Test design still determines semantic coverage;
Jev routing did not demonstrate added benefit in this iteration. The agent's two
CLI mistakes added overhead and required reading help; they are not product defects.

Next website proposal: search and combined filters, next in the fixed shuffled order.
Next Checkpoint proposal: clarify historical started/finished pairs in the dashboard.
Its current event rows show INTERRUPTED_OR_RUNNING even for starts with an observed
finish. Keep raw history intact but annotate observed completion versus missing
finish within the bounded window; never claim process liveness. This addresses an
observed interpretation problem without expanding authority.
