# Revised engineering plan: consolidation notes

Date: 2026-09-27. Scope: documentation only. No runtime, repository instructions, host configuration, provider account, or CI setup was installed or executed.

Source: [preserved revised report](sources/2026-09-27-revised-engineering-plan.md). External checks and their limits are in the [source register](sources.md).

Subsequent user input reopened the language decision: [Python/LangChain assessment](python-langchain-assessment.md). The runtime rows below describe the report's earlier proposal, not a continuing TypeScript requirement. Current ADR-0001 and next steps evaluate Python first.

## Changes incorporated

| Area | Consolidated decision | Canonical document |
|---|---|---|
| Runtime | Node 24 LTS and TypeScript; Node 22 optional; exact patch and dependency pins await tests | [ADR-0001](../adr/0001-runtime-and-adapters.md) |
| Protocol | MCP TypeScript SDK v2, STDIO, target protocol 2026-07-28 | [Architecture](../architecture/overview.md) |
| Jev | Initial versioned evaluation target jev-1.13.0; remote off; no moving alias default | [ADR-0003](../adr/0003-semantic-decisions.md) |
| Authority | Explicit evidence_policy; no required pass based only on Jev | [Contracts](../architecture/contracts-and-evidence.md) |
| Freshness | Separate working_tree from isolated_snapshot and record the guarantee | [Contracts](../architecture/contracts-and-evidence.md) |
| Completion | Reduce existing records; no implicit test or provider call | [Interfaces](../reference/interfaces.md) |
| Hooks | Observe first with zero continuation; separate one-pass mechanical pilot | [Codex](../integrations/codex.md) |
| Data retention | Enterprise ZDR advertised, account terms still unknown | [Privacy](../architecture/security-and-privacy.md) |
| Bootstrap | Native interactive Codex and direct checks; thin automation only when justified | [Runbook](../runbooks/development-harness.md) |
| Self-adoption | Pinned N, candidate N+1, separate state, independently validated promotion | [ADR-0008](../adr/0008-self-adoption.md) |
| Delivery | First package documents schemas and a pure reducer before durable runtime integration | [Next steps](../planning/next-steps.md) |

All ADRs remain proposed. Consolidation is not evidence that implementation milestones or compatibility tests have passed.

## Report inconsistencies resolved

The report reintroduces --agent after the canonical CLI selected --host, and uses different task/revision/result names. Keep the current canonical vocabulary and document the conceptual mapping. No unimplemented aliases are needed.

The report calls completion read-only while showing optional Jev calls in the lifecycle. The core completion operation here consumes stored evidence/findings and may persist an audit report. Explicit review performs remote evaluation. That makes latency, data egress, and failure behavior easier to reason about.

The report's required semantic_advisory criteria need an additional rule: these cannot be the authority for required satisfaction. Registration must preserve the user requirement and require mechanical/manual evidence, not silently change required to false. A model result alone cannot pass or fail that required criterion.

The proposed hook setting advisory plus one continuation conflicts with the existing meaning of advise. Retain observe/advise/enforce semantics: advise never forces continuation; a separately enabled enforce pilot applies only to configured mechanical gaps. Defaults permit zero passes; the first pilot permits one.

Budget defaults were suggestions, not measurements. Adopt six physical provider calls as the initial total cap, retain the existing request timeout, and add the report's total semantic-checkpoint deadline. Per-category limits remain experiment parameters until the budget API is validated.

The report's PostCompact context-injection proposal is not established by the event's existence. Validate each output field and select a supported restoration channel. Early/late bookkeeping cannot depend on an already-connected MCP server.

The report treats March 24, 2026 as Node 20's EOL date, but the inspected table labels that column Last updated. Preserve only the verified EOL status; do not repeat that exact lifecycle date.

Its new routing and latency gates differ from the earlier draft. Keep both proposals traceable and require one frozen protocol before final evaluation. Do not replace thresholds after looking at results.

## What remains unverified

Exact installed Codex/app/CLI/SDK parity; actual Jev requests and account retention; MCP client compatibility; SQLite binding; Windows cancellation of descendant processes; vendor and third-party performance results; statistical sufficiency of the proposed sample sizes; and the product's net quality/cost/latency effect.

Native Windows is the target environment, but environmental guarantees must come from tested capabilities. Neither environment filtering nor a copied workspace alone proves process isolation.

## First work package after documentation

HARNESS-02 and TASK-03/04: concise active repository instructions, task/handoff templates, a scaffold in the language selected by TASK-01's Python-first comparison, validated domain schemas, a pure deterministic readiness reducer, and actual direct verification commands. The templates and runbook are now documented; installing instructions and implementing commands are still open work.

TASK-07 remains the later durable completion service that loads scoped evidence, computes freshness, and records reports. Early reducer fixtures do not complete that task. TASK-09/10 introduce Jev only after deterministic behavior is useful and independently checked.

