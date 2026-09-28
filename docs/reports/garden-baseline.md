# Project Garden baseline

Recorded 2026-09-27 local / 2026-09-28 UTC. Website and evidence paths are in the
[evaluation plan](../planning/project-garden-loop.md). No performance benefit claimed.

## Observed measurements

| Operation | Elapsed seconds | Result |
|---|---:|---|
| Direct unit command | 0.272151 | 3 tests pass |
| Direct syntax command | 0.121448 | pass |
| Pinned start | 1.206946 | task registered |
| Pinned route | 1.758480 | Jev selected backend-testing |
| Pinned two-check command | 3.480817 | both pass |
| Pinned completion | 2.797070 | ready for declared criteria |

Direct check commands total 0.393599 s; pinned checks+completion total 6.277887 s.
Including start+route, pinned workflow total is 9.243313 s. Startup, snapshot and
protocol overhead are included. Single observations, sequential rather than
randomized comparison; no attribution to individual overhead causes or p95 estimate.
Website implementation envelope: first red result at 01:36:08.230Z to first green
at 01:37:10.891Z (~62.7 s), including reasoning and tool latency. Browser validation
was separate and not instrumented as one continuous timed phase.

Raw experiment command records: external evidence/baseline-*.json. Check run IDs:
1da1fd1d-c49e-41a7-bf5b-3045481524c2 (unit),
6b2dce60-ef73-4a2f-855d-9f4c0b57ae48 (syntax).
Website task: 71d2f341a55deb34b29dc954fdc6fb68.

## Browser evidence and discovery

Actual browser editing changed “A quieter morning” to “Morning notebook” and stage
to Harvest. Reload retained the edit. Desktop/mobile screenshots were inspected;
mobile renders one column without clipped cards. The first unquoted @e7 reference
was consumed by PowerShell: no browser click occurred. Quoting refs recovered it.

Setting synthetic localStorage to `{broken` and reloading produced zero cards.
Another completion call, without source changes, still reported ready with the same
snapshot. That is correct for the declared syntax/model obligations but **not** a
complete website validation. This experiment demonstrates missing test coverage,
not invalid freshness or a justification to let advisory Jev decide pass/fail.
Screenshots: baseline-desktop.png, baseline-mobile.png, baseline-malformed-storage.png
under the external evidence directory. Browser content used no real user data.

## Provider and repository verification

Website Jev decision 8223ddbe-7cac-4825-8f88-f84ab890016b: one physical request,
390 input / 41 output tokens, 0.553235 s, confidence 0.13, dollars unknown.
Repository decision 565f6f55-106a-49db-be06-25d5cca69c4f: one request,
399/40 tokens, 0.678239 s, confidence 0.52, dollars unknown. No retries or review.
The skill already applied independently; routing added no demonstrated decision value.

Native repository task 35b957317500d92205cb776aa9da3a7c passed lint/format/types/tests
and completion before iteration 1 repository edits. Test-run elapsed: 143.045621 s.
This historical readiness is not current evidence after edits.

## Next paired proposal

Website: recover from invalid/unavailable storage, warn accurately, preserve stored
data until explicit save. Tool: expose declared-evidence assessment scope in validated
completion output and MCP description without altering readiness semantics.
