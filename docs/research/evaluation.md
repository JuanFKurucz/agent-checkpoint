# Evaluation protocol

Status: proposed protocol. No measurements have been run. Freeze the protocol and thresholds before evaluating held-out data.

## Questions and conditions

Test the usefulness of the evidence runtime separately from Jev.

| Condition | Intervention |
|---|---|
| A: baseline | Normal coding host |
| B: deterministic | Task contracts, approved checks, evidence freshness |
| C: heuristic | B plus inexpensive resource selection |
| D: self-judge | B plus equivalent bounded decisions from the coding model |
| E: Jev | B plus Jev on the same decision boundaries |

Use A versus B to measure runtime value, and E versus B/C/D to measure incremental Jev value. Prompt additions, retries, check effort, and observation overhead must be recorded in every condition.

## Datasets

| Dataset | Pilot | Expansion target | Negative cases |
|---|---:|---:|---|
| Skill routing | 100 | 300+ | No applicable skill, overlapping names, misleading descriptions, required skill |
| Criterion evidence | 150 | 500+ | Stale run, wrong test, fabricated success, omitted requirement |
| Subagent routing, deferred | 100 | 300+ | Unnecessary delegation, tightly dependent steps |
| Policy conformance, deferred | 100 | 300+ | Ambiguous rule, missing context, adversarial comment |
| Whole tasks | 30 | 100+ | Incomplete feature, no-op, unclear request, changed policy |

Counts are planning targets, not statistical sufficiency guarantees. Label routing with independent reviewers and retain disagreements; completion uses hidden tests plus adjudication for non-mechanical requirements.

Split by repository/task family before tuning to prevent near-duplicate leakage. Keep hidden tests and final labels inaccessible to providers and agents. Version datasets, catalogs, task definitions, and rubrics. Do not regenerate labels with the system being evaluated.

## Experimental procedure

1. Define the task and environment, baseline host settings, budgets, and success criteria.
2. Freeze development, calibration, and held-out splits.
3. Run decision replays to eliminate poor rubrics and estimate cost.
4. Run paired live tasks from the same base commit with clean, isolated state.
5. Randomize condition order and repeat trials for stochastic agent behavior.
6. Control cold/warm cache conditions and never leak state from one condition to another.
7. Judge outcomes independently, blind to intervention where practical.
8. Report task-level outcomes, uncertainty, and failure categories before aggregate claims.

Record OS, hardware, network conditions, package/host/model versions, requested and actual provider models, policy/catalog digests, pricing schedule date, retry counts, truncation, and cancellations.

## Metrics and denominators

False-ready rate = ready tasks with at least one unsatisfied required criterion / all tasks declared ready. If none are declared ready, the rate is undefined; report coverage instead of zero.

Also report false-ready count / all attempted tasks so a system cannot appear safer merely by refusing every completion. Report false-block rate and abstention coverage.

Total experiment cost includes coding model, subagent, provider, infrastructure, and failed/retried attempts. Cost per accepted task = total cost of all attempts in the condition / independently accepted tasks. If no tasks are accepted, it is undefined/infinite, not free.

Avoid double-counting subagent costs already included in host usage. When subscription pricing obscures marginal dollar cost, report tokens/usage separately and label any tariff-based estimate. Never claim a lower bill from token reduction alone.

Wall time runs from accepted input to independently accepted result or terminal failure. Report failed-task duration and timeouts as well as latency among accepted tasks; disclose censoring. Parallel work uses elapsed time, not sum of call durations.

| Dimension | Measurements |
|---|---|
| Task quality | Hidden-test success and independent acceptance |
| Completion | False-ready, unmet-criterion recall, unresolved coverage, false-block |
| Routing | Precision, recall, unnecessary choices, selective risk at coverage |
| Calibration | Brier score where applicable; reliability bins and uncertainty |
| Cost | Whole-condition spend and cost per accepted task |
| Latency | Task wall time and checkpoint p50/p95/p99 |
| Human work | Review/intervention minutes |
| Reliability | Outages, stale evidence, duplicate continuations, exhausted budgets |

Use paired task-level intervals; bootstrap by task/repository cluster rather than pretending repeated trials are independent. Report uncertainty for binary outcomes and routing precision. A small pilot cannot establish rare-event safety or tail latency reliably.

## Draft gates from the report

| Gate | Proposed target | Interpretation |
|---|---|---|
| False-ready | At least 30% relative reduction | Also report absolute change; if baseline is zero, use an absolute criterion |
| Correctness | At most 2 percentage points regression | Require a non-inferiority analysis, not just similar point estimates |
| Autonomous routing precision | At least 95% on held-out domain | Pre-register coverage and uncertainty requirement; unrelated to semantic blocking |
| Remediation limit reached | Under 1% of eligible tasks | Requires sufficient sample size |
| Stale/missing evidence silently passes | Zero observed invariant violations | Mandatory engineering invariant; finite tests do not prove universal absence |
| Required pass based solely on semantic advice | Zero observed violations | Required mechanical/manual authority must be satisfied independently |
| Cross-task evidence reuse | Zero observed violations | Mandatory identity invariant |
| Cost saving claim | Total cost per accepted task decreases | Include failures and retries |
| Latency saving claim | End-to-end distribution improves | Include p95 and quality context |

These targets are recommendations to ratify during TASK-10, not achieved results or automatic release authorization. The team must also precommit absolute budget limits and the minimum useful effect. If evidence is inconclusive, expand or narrow the study; do not tune the gate after viewing held-out results.

### Revised report's additional candidates

The [revised report](sources/2026-09-27-revised-engineering-plan.md) proposes at least 20% relative and five percentage points absolute routing-error reduction against the strongest simple baseline, provider p95 at or below two seconds, and end-to-end false-ready non-inferiority to deterministic mode plus a measured benefit in success, rework, human effort, or cost.

These are unratified alternatives/additions, not measured results or silent replacements for the earlier table. A five-point improvement is impossible if baseline error is below five points; decide the applicable gate and sample size before final data are seen. Freeze the chosen protocol once. Routing improvements do not establish completion accuracy.

Stage the comparisons: offline provider decisions, then whole-task intervention, then incremental hook observation/continuation. Hook observation must not inject recommendations into the active agent. Internal development tasks remain tuning or observational data, not the held-out release set.

## Decision artifacts

Save a protocol, split manifest, sanitized decision outputs, per-task results, pricing/usage assumptions, analysis, and a go/no-go note. Outcomes may be ship deterministic-only, continue Jev research, enable a specific advisory policy, or stop a failed intervention.

Semantic blocking remains out of v1 regardless of routing precision. The [roadmap](../planning/roadmap.md) controls promotion.

