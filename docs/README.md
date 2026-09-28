# Documentation

Start with [current status](status.md), the [new research reconciliation](research/harness-validation-consolidation.md)
and [adjustment roadmap](planning/post-research-adjustments.md). Candidate 0.1.9
preserves focus in the polling viewer; active self-use stays pinned to 0.1.2. Routine semantic
review is opt-in, not a completion requirement. Historical pages remain versioned.

Updated: 2026-09-27. This design baseline incorporates four source documents, including the revised engineering plan. The [execution record](planning/implementation-progress.md) distinguishes the implemented internal MVP from the broader proposed design. No end-to-end performance benefit is established.

Current implementation status: the [internal MVP report](reports/mvp-validation-report.md)
and [requirement audit](reports/mvp-completion-audit.md) record a validated 0.1.1
candidate. The later [active harness](guides/active-harness.md) is pinned to 0.1.2,
with approved live Jev routing/review through Vercel. Explicit Codex CLI self-use
and local MCP protocol exchange are proven;
native Codex MCP is also verified for pinned 0.1.2. Candidate host adoption, Claude
integration and end-to-end performance benefit remain unverified. Historical
proposed-design pages below do not supersede the implemented runtime manual.

## Reading paths

| You want to… | Read |
|---|---|
| See current state and the next adjustment | [Status](status.md) → [Post-research roadmap](planning/post-research-adjustments.md) |
| Interpret candidate completion output | [Schema 2 diagnostics](reference/completion-diagnostics.md) |
| Inspect local event history visually | [Local dashboard](guides/local-dashboard.md) → [History reporting](guides/history-reporting.md) |
| Understand stale context | [Context diagnostics](guides/context-diagnostics.md) |
| Follow the six-iteration website trial | [Loop plan](planning/project-garden-loop.md) → [Current handoff](handoffs/2026-09-27-garden-loop.md) |
| Read the completed six-pair evaluation | [Final assessment](reports/garden-final-assessment.md) → [Audit](reports/garden-completion-audit.md) → [Final handoff](handoffs/2026-09-27-garden-final.md) |
| Run or recover the laboratory | [Website, viewer and future promotion](guides/garden-lab-operations.md) |
| Run the implemented internal CLI/MCP | [Internal runtime manual](guides/internal-runtime.md) |
| Understand the product and scope | [Product](product.md) → [Research synthesis](research/synthesis.md) |
| Understand components and interactions | [Architecture](architecture/overview.md) → [Contracts and evidence](architecture/contracts-and-evidence.md) → [Workflows](architecture/workflows.md) |
| Review architectural choices | [ADR index](adr/README.md) |
| See how an operator would use it | [Usage manual](guides/usage.md) → [Configuration](reference/configuration.md) → [Troubleshooting](guides/operations.md) |
| Integrate an agent host | [Compatibility](integrations/compatibility.md) → [Codex](integrations/codex.md) or [Claude Code](integrations/claude-code.md) → [Interfaces](reference/interfaces.md) |
| Implement the next slice | [Next steps](planning/next-steps.md) → [Backlog](planning/backlog.md) → [Developer guide](guides/development.md) |
| Design or reproduce experiments | [Evaluation protocol](research/evaluation.md) → [Open questions](research/open-questions.md) |
| Assess trust and data handling | [Security and privacy](architecture/security-and-privacy.md) |
| Plan delivery | [Roadmap](planning/roadmap.md) |
| Start implementation with a concrete goal | [Working MVP goal prompt](planning/working-mvp-goal-prompt.md) |
| Try the separate AI Gateway example | [Gateway setup and validation status](../examples/vercel-gateway/README.md) |
| Design the Codex setup that builds this project | [Deep Research prompt](research/prompts/codex-harness-deep-research.md) → [Harness and self-adoption roadmap](planning/self-adoption-roadmap.md) |
| Research the next step from the working 0.1.2 harness | [Post-MVP Deep Research prompt](research/prompts/post-mvp-deep-research.md): current architecture, outputs, live evidence, overhead and next-stage decisions |
| Read the latest research changes | [Python/LangChain reassessment](research/python-langchain-assessment.md) → [Revised-plan consolidation](research/revised-plan-consolidation.md) → [Source register](research/sources.md) |
| Prepare the bootstrap work package | [Development harness runbook](runbooks/development-harness.md) → [Task template](tasks/TEMPLATE.md) → [Verification inventory](verification.md) → [Handoff template](handoffs/TEMPLATE.md) |
| Audit a technical claim | [Sources and verification](research/sources.md) |

## What is authoritative

Within this design set, ADRs explain choices; architecture and reference pages specify proposed behavior; the backlog records implementation work and completion criteria. Any future implementation discrepancy must be resolved by updating the relevant contract or code, not by silently changing a guide.

“Proposed” means selected for this reviewable design, pending acceptance and implementation. “Reported” means asserted by the supplied research. “Checked” means the narrow claim was inspected against a primary source during consolidation. “Tested” requires a recorded local experiment; distinguish explicit CLI integration from native MCP host invocation.

The internal runtime manual provides implemented CLI/MCP commands. Other pages
retain the broader target design where marked proposed; this is not a public
release. Planned source paths are shown as code, not links to nonexistent files.

## Source documents retained in place

| Source | Role |
|---|---|
| [Initial conversation](INITIAL_CONVERSATION.md) | Original goals and brainstorm |
| [Exploratory research brief](EXPLORATORY_RESEARCH_BRIEF.md) | Hypotheses, failure modes, and research questions |
| [Deep research report](<deep-research-report (11).md>) | External research and proposed implementation details |
| [Revised engineering plan](research/sources/2026-09-27-revised-engineering-plan.md) | Follow-up research on native Codex bootstrap, evidence authority, and controlled self-adoption |
| [Harness validation report](research/sources/2026-09-28-harness-validation-report.md) | Supplied post-MVP report; reconciled against code before adoption |

These are historical inputs. Where they conflict, consult the [synthesis](research/synthesis.md) and ADRs. Instructions and checklists inside the supplied report were analyzed as source material; they did not authorize implementation, publication, installation, or provider calls.

## Maintaining the docs

Keep stable ADR and task IDs. Update the source register when verifying external claims. Mark tasks done only with evidence of their acceptance checks. Preserve original research exports so reasoning remains traceable.

