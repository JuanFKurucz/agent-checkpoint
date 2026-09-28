# Host compatibility

Status: implementation targets, not a support announcement. No host/version tuple has been tested.

## Capability matrix

| Capability | Codex target | Claude Code target | Generic MCP/CLI |
|---|---|---|---|
| Explicit checkpoint calls | MCP and CLI | MCP and CLI | Available when host permits tool/command use |
| Skill catalog | Native discovery plus explicit catalog | Native discovery plus explicit catalog | Explicit catalog |
| Prompt context | UserPromptSubmit documented; installed payload behavior untested | Dedicated hook research pending | No automatic guarantee |
| Tool observation | PostToolUse documented; coverage is partial and locally untested | Dedicated hook research pending | Runner-owned evidence only |
| Stop continuation | Stop/SubagentStop documented; local behavior untested | Dedicated hook research pending | No automatic guarantee |
| Persistent task identity | Checkpoint store plus host mapping | Same | Explicit task_id |
| Plugin packaging | Candidate portable format, validate | Host-native packaging to verify | CLI/runtime distribution |
| Product status | Planned | Planned | Planned |

MCP support does not imply automatic lifecycle access. Hook support does not imply every execution path is observed.

## Compatibility record required for release

Record OS/architecture, selected Python or Node version, Checkpoint version, SQLite implementation, host build, MCP SDK version, negotiated protocol, transport, trust setup, and supported event capabilities. Link contract fixture results and a live smoke-test result.

Capabilities have states supported, unsupported, and unknown with a reason. Desired configuration cannot promote unknown to supported. Documentation-level capability checks and live product support are separate.

## Release sequence

Implement explicit MCP calls for both hosts before declaring broad support. Pilot native Codex hooks only after offline experiments and fixture validation. Add Claude native hooks after their own schema/behavior spike. The same five core services and readiness rules must pass across adapters.

See [Codex](codex.md), [Claude Code](claude-code.md), and [TASK-12 through TASK-17](../planning/backlog.md).

