# Project Garden — final six-iteration assessment

Recorded 2026-09-27 local / 2026-09-28 UTC. Audience: the developer deciding how to
use and improve Checkpoint. This is an internal consumer trial, not a benchmark of
Codex versus Claude, a public release, or evidence of general cost/latency gains.

## Outcome

The separate [Project Garden website](D:/Programming/project-garden-lab/README.md)
works with local persistence, recovery, appearance preferences, sorting, combined
search/filters, edit/delete/undo and keyboard focus recovery. Seventeen website
tests and recorded browser interactions cover these flows. Candidate Checkpoint
0.1.9 contains six tested improvements; the active supervisor remains pinned 0.1.2.
The final feature gates passed 180 tests plus lint/format/types and native completion.
The final documentation/package closure is evidenced by external
[final-audit/validation.json](C:/Users/juanf/AppData/Local/agent-checkpoint/harness/garden-lab/final-audit/validation.json),
not by this document asserting its own completion.

The [local read-only observatory](../guides/garden-lab-operations.md) shows baseline
and six website task histories, check outcomes, Jev usage, historical completion,
event pairing, and a decision overview with Mermaid source/export. Candidate
operation timing appears where recorded; legacy timestamps remain unknown.

## Six feature pairs

| Iteration / report | Website result | Checkpoint improvement | Demonstrated benefit / limit |
|---|---|---|---|
| [1](garden-iteration-01.md) | Malformed/blocked persistence recovery | Explicit declared-evidence completion scope | Reduces overreading “ready”; does not discover missing tests |
| [2](garden-iteration-02.md) | Theme and reduced-motion preferences | Bounded read-only CLI/MCP reporting | One metadata report replaces manual record joining; no performance gain established |
| [3](garden-iteration-03.md) | Delete and undo | Local dashboard and timestamped operation traces | Inspect decisions visually without executing checks or calling providers |
| [4](garden-iteration-04.md) | Stable view sorting | Safe stale-context component diagnostics | Controlled environment mismatch becomes explainable; freshness unchanged |
| [5](garden-iteration-05.md) | Search and combined filters | Bounded start/finish pairing | Completed starts no longer look perpetually running; missing counterparts are not liveness claims |
| [6](garden-iteration-06.md) | Keyboard/dialog focus recovery | Polling task-focus preservation | Real browser BUTTON→BODY failure fixed; no focus stealing elsewhere |

Seed 20260927 and the recorded Fisher–Yates/LCG reproduce this website order. Tool
changes came from observed friction, not random feature selection. Every report
contains both proposals, observations, limitations and next paired proposals.

## What helped, and what did not

Checkpoint genuinely prevented a premature completion in iteration 4. Full gates
found missing script formatting and a context-fingerprint regression after focused
tests had passed. Native completion returned needs_changes. Unsupported context
layouts were repaired without discarding their full freshness identity; the rerun
passed. Original failed artifacts and completion are preserved alongside repaired
ones. This is a demonstrated gate benefit, not a counterfactual claim that a human
would otherwise have shipped the defect.

The baseline browser had a blank board from malformed local storage while declared
syntax/model checks were ready. Checkpoint correctly assessed those obligations,
but they were insufficient. Browser evaluation also found edit-focus loss and the
dialog Tab boundary gap. No current feature authenticates semantic coverage.
The scope notice makes that limit clearer; it does not remove it.

The controlled context replay kept stale evidence unresolved in both versions;
the candidate added changed-component names. History reporting, pairing and focus
fixes improve diagnosis and interaction, not check authority. Unknown/corrupt,
missing, stale, interrupted and failed evidence remain distinct. Suggested actions
never authorize or perform a repair. The earlier real native/CLI discrepancy is
not retroactively root-caused by the synthetic replay.

Jev selected a plausible skill in every recorded loop route, but those skills were
already applicable independently. No useful change in an implementation decision
was demonstrated. Keep routing advisory and review opt-in; do not manufacture calls
to create activity. The $5 key budget is user-reported and externally enforced,
not an application-level spending guarantee.

## Timing, counts and measurement boundaries

These are individual recorded observations on a changing project. They include
process startup and snapshots, not just check execution. They are not paired
randomized performance trials or p95 estimates.

| Website slice | Model tests | Pinned checks, s | Pinned completion, s | Combined, s |
|---|---:|---:|---:|---:|
| Baseline | 3 | 3.481 | 2.797 | 6.278 |
| 1 | 7 | 3.637 | 3.243 | 6.880 |
| 2 | 9 | 3.295 | 2.766 | 6.060 |
| 3 | 11 | 3.808 | 3.121 | 6.929 |
| 4 | 13 | 3.365 | 2.934 | 6.299 |
| 5 | 15 | 3.432 | 3.164 | 6.595 |
| 6 | 17 | 3.418 | 2.808 | 6.227 |

At baseline, equivalent direct unit+syntax commands took 0.394 s versus 6.278 s
for pinned checks+completion: about 5.884 s added workflow time. Including start
and route, the pinned workflow took 9.243 s. Completion adds an evidence operation
not present in a bare direct test command. No causal attribution to Python, MCP,
hashing or Jev is justified by this sample. Later direct unit-only times around
0.31–0.35 s are not equivalent to the full pinned workflow.

Before final document closure, bounded history reads of all 14 loop tasks showed
32 finished repository checks and 14 website checks. The repository had eight
four-check workflows (seven slices plus iteration-4 repair), and eight recorded
completions. Website had seven two-check workflows and eight completions (one extra
baseline coverage experiment). Nominal successful calls: four per task—start,
route, checks, completion—with those extra check/completion calls. Two iteration-4
CLI argument errors reached neither execution nor provider. Final document edits
require another four-check workflow and completion on the existing iteration-6
task; its counts/timing are in the closure manifest. Direct focused tests, browser
commands, and every agent filesystem read are not included in these workflow counts.

Website red→green elapsed envelopes are retained in each report. They include
reasoning/tool latency; some patches were prepared before the red command finished.
Total design/implementation/browser effort was not continuously instrumented and
remains unknown. There is no defensible claim of saved developer time.

Jev: **14 observed physical requests, 5,533 input tokens, 563 output tokens**, each
task reservation 1, no unknown/conflicting usage in these untruncated task windows.
All were Vercel `typesafe-ai/jev` routes; no loop semantic reviews, retries or
fallback. Known call latencies ranged 0.509–6.129 s. Dollars are unknown. The
[history inventory](C:/Users/juanf/AppData/Local/agent-checkpoint/harness/garden-lab/final-audit/history-inventory.json)
is scoped to these tasks, not account billing or prior project experiments.
Candidate smoke tests, probes and dashboard reads made no model requests.

## Friction and limitations

- Two incorrect CLI flags in iteration 4 were agent usage errors; help recovered.
  Its website routing occurred after new tests, before implementation: a retained
  sequencing deviation, not perfect protocol compliance.
- Automation downloads to a redirected Windows AppData destination were canceled;
  normal browser downloads succeeded and were checked on disk. No product patch
  was justified for that automation-specific failure.
- State/trace views are bounded and may be incomplete. Trace writes are best-effort;
  read-only history cannot prove current readiness or process liveness.
- Task navigation still uses opaque IDs. The handoff maps them to iterations.
  Source-role labels are operator declarations, not attestation.
- Working-tree checks are not isolated-snapshot execution. Environment filtering
  is not a sandbox. Evidence bindings/origin labels remain unauthenticated coverage.
- Browser checks are manual/reproducible observations, not cross-browser or full
  assistive-technology certification. Creating new cards is a future feature.
- Native candidate MCP adoption, Claude integration, CI, hooks, public hosting,
  global monitoring and hosted telemetry were neither enabled nor claimed.
- Candidate improvements are installed for isolated validation/read-only viewing;
  active self-supervision still uses 0.1.2 and its five tools.

## Recommended priorities

1. **Evidence authority:** design trusted criterion/check bindings and independent
   outcome evaluation before expanding completion claims. Keep browser verification
   separate and make its coverage explicit.
2. **Measure overhead:** instrument startup/snapshot/check phases in a controlled,
   repeated same-input trial. Consider batching only if freshness, idempotency and
   explicit execution remain intact. Do not adopt a 70% reduction as an achieved fact.
3. **Interaction:** add safe local iteration/task labels and automate the browser
   regression paths. Website next pair: create-new-project validation; tool next
   pair: measured batching/diagnostic navigation, as scoped in iteration 6.
4. **Jev value experiment:** compare mandatory/local routing against Jev on tasks
   with genuinely competing skills and independently judged outcomes. More usage
   alone is not success. Preserve abstention and the existing payload/budget limits.
5. **Adoption:** follow the explicit promotion/recovery procedure only when approved.
   Test native candidate tools after reload before claiming host integration.

The Documentation Writer skill separated this explanation from the operating
how-to and evidence audit. Testing/browser skills shaped the earlier paired work.
