# Iteration 1 — persistence recovery and honest completion scope

Status: verified. Final native gates passed: 118 tests in 136.21 s, lint/format/types
pass, completion ready at snapshot 602d111f7111062b0abebbb14573fd691c5fdeb6ebab58d8b91d510eb900491a.
Independent installed 0.1.4 MCP exchange passed in 8.602949 s; all 14 runtime files
matched source. Full record: external garden-lab/candidate-iteration-1/validation.json.
That snapshot is historical after subsequent iteration edits; candidate was not promoted.

## Paired proposals and rationale

Website: recover from malformed/unavailable browser storage without silently
overwriting it. Tool: explicitly scope completion to declared evidence. The baseline
showed a blank browser board alongside ready syntax/model evidence. Neither change
claims authenticated semantic coverage or auto-repair authority.

## Implemented and observed

- Website loader validates bounded arrays, card fields, stages and unique IDs;
  empty saved arrays remain empty. Invalid data produces temporary examples and a
  warning. Reads never overwrite storage. Failed writes warn that edits are unsaved.
- Four added model cases first failed because loader/saver exports were missing;
  all seven cases then passed. The browser recovered from the same `{broken` value,
  rendered three cards, warned, and retained the malformed value unchanged.
- Candidate completion includes assessment_scope=declared_evidence_only and a
  constant notice: declared obligations are not overall product correctness or
  semantic coverage. Attempts to strengthen that claim are rejected. Reducer and
  provider authority are unchanged. Active 0.1.2 does not expose these new fields.
- Five new scope cases: four failed before implementation, one negative rejection
  already passed. Runtime and actual stdio regression assertions were also added.

The Backend Testing skill drove red/green isolated cases; frontend-design guided
the botanical layout. Browser skill required fresh snapshots after DOM transitions.

## Measurements / evidence

Website task 71469e61b4c66a82b47e26b025c99eb3, repository task
7d412f915d3ea4ecfb21a45c4ed73701. Website check run IDs:
9ff4adee-0ba8-4b0b-9382-a50956b0fd69 (unit),
ca076d43-dd6b-4e8a-82ef-2cd9e6a44d1a (syntax).
Website checks+completion: 3.637153 + 3.242534 = 6.879686 s; direct seven-test command
0.311655 s (not an equivalent syntax+completion workflow). No speedup claim.
Implementation red-to-green envelope ~15.4 s; browser validation separate.
External evidence/iteration-1-*.json and iteration-1-recovery-mobile.png retain results.

Jev website decision fa2c3f44-e4d1-465a-8c48-cf3669290c92: one physical request,
399/41 tokens, 0.654105 s, backend-testing, confidence 0.88. Repository decision
56050136-9cd1-4707-b111-d7b81a8b46b6: one request, 396/39 tokens, 0.509181 s,
documentation, confidence 0.52. All dollars unknown. No retries or semantic review.
Documentation routing did not supersede mandatory applicable testing instructions.

## Helpfulness and limits

Browser experimentation, not Checkpoint, found the storage defect. Checkpoint
recorded the regression results and their freshness. The new notice improves the
meaning of the output, but does not discover untested behavior. Browser tests are
still manual; keyboard restoration remains a later iteration. Pinned completion
still uses schema 1. Recorded evidence is historical after subsequent edits.

## Next paired proposal

Website iteration 2: theme preference and reduced-motion support (shuffled order).
Tool: local bounded, read-only task reporting. Current diagnosis requires manually
joining tool output, check IDs and external timing files; a metadata-only report
should expose that history without executing checks or mistaking history for fresh
completion. This is the foundation for the requested live visual dashboard.
