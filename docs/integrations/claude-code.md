# Claude Code integration design

Status: proposed. The supplied research establishes a direction for explicit MCP and leaves native hook verification open.

## Initial workflow

Register the pinned local runtime through the host's supported MCP configuration mechanism after verifying the current schema. Use explicit task, routing, checks, review, and completion calls. Reuse the core task/evidence contracts and readiness interpretation.

The source report identifies project .mcp.json and user approval as relevant. This is a reported integration detail, not a tested configuration snippet. Installation should inspect existing entries, preview a merge, and preserve host approvals.

## Native adapter research

Before adding hooks, verify:

1. Event names, JSON payloads, deadlines, and exit/output semantics.
2. Context injection and tool-result visibility.
3. Stop and subagent continuation behavior.
4. Session identity across resume and compaction.
5. Plugin packaging, configuration scope/precedence, and trust.
6. Duplicate/concurrent event behavior and cancellation.

Record primary references and fixtures in the compatibility record. Do not mechanically reuse Codex hook response JSON.

## Portability acceptance

Run the same registered task through CLI, Codex MCP, and Claude MCP. Require equivalent domain results for identical contracts/evidence; allow host-specific presentation and transport metadata.

A successful explicit MCP demo supports the claim “usable through MCP.” Automatic checkpoints require separate native-adapter tests. If a host lacks a capability, the manual workflow remains valid and doctor reports the limitation.

