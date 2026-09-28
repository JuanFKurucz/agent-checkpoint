# Sources and verification register

Checked: 2026-09-27. This register separates supplied research from direct verification and executable compatibility evidence.

## Local sources

| ID | Source | How it is used |
|---|---|---|
| SRC-01 | [Initial conversation](../INITIAL_CONVERSATION.md) | Original intent and proposed integrations |
| SRC-02 | [Exploratory brief](../EXPLORATORY_RESEARCH_BRIEF.md) | Hypotheses, metrics, uncertainties |
| SRC-03 | [Deep research report](<../deep-research-report (11).md>) | Detailed architecture, reported findings, source URLs |
| SRC-04 | [Revised engineering plan](sources/2026-09-27-revised-engineering-plan.md) | Supplied 2026-09-27 research response; retained with original citation tokens as a historical input |
| SRC-05 | [Harness validation report](sources/2026-09-28-harness-validation-report.md) | Supplied date 2026-09-28; consolidated locally 2026-09-27; citation placeholders retained, not independently resolved |

Latest [reconciliation](harness-validation-consolidation.md) and [current status](../status.md)
supersede historical "untested" statements where later local evidence exists.
SRC-05's dates, newest host/protocol claims, prices and retention assertions are
not adopted as verified facts. Do not copy its proposed schema into active config.

The source exports contain citation tokens whose original retrieval targets are unavailable in the files. SRC-03 contains a URL index; SRC-04 mostly uses unrecoverable citation tokens. Their recommendations are inputs to the design, not instructions to execute. The [revision notes](revised-plan-consolidation.md) record accepted changes, reconciled conflicts, and unresolved claims.

## Limited checks completed during consolidation

| ID | Primary source | Checked claim | Remaining limitation |
|---|---|---|---|
| EXT-01 | [Official TypeSafe JavaScript SDK](https://github.com/typesafe-ai/typesafe-sdk-js) | Repository identifies the official SDK; README shows Node 20+, package name, typed choice helper, and systemOne client | No package installed, exact release pinned, or live API tested |
| EXT-02 | [MCP TypeScript v2 documentation](https://ts.sdk.modelcontextprotocol.io/v2/) | Documentation exists for v2, split server/client packages, serving, migration, and legacy clients | Host compatibility and exact imports untested |
| EXT-03 | [MCP 2026-07-28 release](https://blog.modelcontextprotocol.io/posts/2026-07-28/) | Release page identifies that protocol generation and its stateless direction | Does not establish which protocol a particular installed host supports |
| EXT-12 | [Node release table](https://nodejs.org/en/about/previous-releases) | Lists Node 24/22 as LTS and Node 20 as EOL; supports proposed Node 24 baseline | The table's March 24 date for Node 20 is Last updated, not evidence of its precise EOL date |
| EXT-13 | [TypeSafe models](https://docs.typesafe.ai/models) | Lists jev-1.13.0 and moving aliases; returned model identifies the version | Account access and actual request were not tested |
| EXT-14 | [TypeSafe legal overview](https://docs.typesafe.ai/legal) | Advertises enterprise ZDR | No entitlement or terms for this account established |
| EXT-15 | [Current Codex hooks](https://learn.chatgpt.com/docs/hooks) | Checked existing-MCP lifecycle constraints, continuation, incomplete tool coverage, and disable setting | No local hook execution; the older developers.openai.com/docs/hooks URL returned 404 |
| EXT-16 | [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode) | Official destination for programmatic-run investigation | Exact event/version behavior still needs HARNESS-01 fixture verification |
| EXT-17 | [Windows sandbox](https://learn.chatgpt.com/docs/windows/windows-sandbox) | Current official Windows guidance located | Local sandbox/descendant-process behavior untested |
| EXT-24 | [MCP 2025-11-25 tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools) | Checked 2026-09-27: outputSchema describes structured results and supplied schemas require conforming output | Supports candidate completion validation; no new protocol/host compatibility claim |

These checks support selecting an ecosystem for a prototype. They do not establish performance gains or production readiness.

## Python and LangChain follow-up

Checked 2026-09-27 after the user's additional references. See the [runtime reassessment](python-langchain-assessment.md); earlier Node/TypeScript sources remain evidence for an alternative, not a required stack.

| ID | Primary source | Checked scope | Remaining limitation |
|---|---|---|---|
| EXT-18 | [Harness with Jev](https://www.langchain.com/blog/building-a-harness-with-jev) | Python integration and experimental middleware examples | Does not establish access to native coding-host internals |
| EXT-19 | [TypeSafe integration reference](https://docs.langchain.com/oss/python/integrations/providers/typesafe) | Classifier request/result contract | Exact installed release, retries and tracing behavior untested |
| EXT-20 | [Jev and LangGraph](https://www.langchain.com/blog/building-prod-with-jev-and-langgraph) | Decision-workflow example with linked code | Reported performance not reproduced or transferable by assumption |
| EXT-21 | [Decision model evaluator](https://docs.langchain.com/langsmith/decision-model-evaluator) | LangSmith UI evaluator creation and Jev support | Not a local-runtime SDK replacement; account/data approval pending |
| EXT-22 | [TypeSafe Python SDK](https://github.com/typesafe-ai/typesafe-sdk-python) | Direct official Python client exists | Package pin, cancellation and live account access untested |
| EXT-23 | [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) | Python server/client implementation, v2 documentation | Installed-host exchange and packaging untested |

## Reported claims requiring follow-up

| ID | Topic and primary source to inspect | Claim to verify | Backlog |
|---|---|---|---|
| EXT-04 | [System One API](https://api.typesafe.ai/docs) | Noul, Choice, Score shapes; model discovery; limits; errors and retry behavior | TASK-01, TASK-09 |
| EXT-05 | [TypeSafe evaluations](https://evals.typesafe.ai/) and [introduction](https://typesafe.ai/blog/introducing-system-one-models-and-jev) | Benchmark conditions, pricing basis, latency distribution; no transfer assumption to coding tasks | TASK-01, TASK-10 |
| EXT-06 | [Privacy](https://typesafe.ai/legal/privacy-policy), [DPA](https://typesafe.ai/legal/data-processing), [customer agreement](https://typesafe.ai/legal/mca) | Account-specific retention, training use, telemetry and approval conditions; see enterprise availability in EXT-14 | TASK-02 |
| EXT-07 | [Codex hooks](https://learn.chatgpt.com/docs/hooks) | Remaining exact schemas/deadlines, output-field permissions, installed-surface parity; selected constraints checked in EXT-15 | TASK-01, TASK-13 |
| EXT-08 | [Plugin packaging](https://developers.openai.com/plugins/build/plugins) and [MCP server guidance](https://developers.openai.com/plugins/build/mcp-server) | Current manifests, installation, hooks and trust | TASK-16 |
| EXT-09 | [Claude Code MCP](https://docs.anthropic.com/en/docs/claude-code/mcp) | STDIO, configuration scopes, project approval; follow official navigation for hook reference | TASK-12, TASK-17 |
| EXT-10 | [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use) and [pull_request_target](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target) | Appropriate independent CI pattern and credential boundaries | TASK-15 |
| EXT-11 | [LangChain agent evaluations](https://www.langchain.com/resources/agent-evals) | Evaluation guidance; recover exact Jev experiment URL separately | TASK-01, TASK-10 |

Current prices are deliberately omitted from operating defaults. The report's price figure is a dated vendor claim, not a billing guarantee. No zero-retention or self-hosted Jev capability is assumed.

MCP v2's page now explicitly identifies the stable release line and 2026-07-28 protocol. This supports the proposed SDK generation, not an exact dependency pin or a tested Codex/Claude tuple. SDK retry/cancellation details and vendor/third-party benchmark numbers in SRC-04 remain reported until their specific primary artifacts are verified.

## Recording a completed verification

For each claim record the final URL after redirects, date, source section, package/host/model versions, exact interpretation, and link to the saved test result if applicable. Use statuses reported, checked, tested, contradicted, or unavailable. A failed fetch is unavailable, not contradicted. Record unresolved disagreements instead of selecting the more convenient source.

