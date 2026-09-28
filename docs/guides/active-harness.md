# Active repository harness

Enabled by user request on 2026-09-27, after the internal-MVP validation. This is
explicit advisory adoption, not a native hook or a custom replacement coding agent.

Current verification: pinned 0.1.2 native MCP start/route/check/completion have now
run successfully throughout the [Garden trial](../reports/garden-final-assessment.md).
Later "still requires loading" statements below retain the original setup snapshot.
Candidate 0.1.9's six-tool standalone smoke is not native adoption. See the
[current promotion/recovery procedure](garden-lab-operations.md).

Post-research policy adjustment: routing remains advisory; criterion review is
opt-in for a specific experiment, not a default completion step. All five tools and
the existing approved payload kinds remain available. Candidate 0.1.3's
[typed diagnostics](../reference/completion-diagnostics.md) are not installed in
this still-pinned 0.1.2 supervisor. No active artifact or credential was changed.

## What is configured

- Project-local Codex MCP: `.codex/config.toml`, all five Checkpoint tools, 30-second
  startup and 600-second tool deadlines. Startup is optional so broken Checkpoint
  cannot prevent Codex from opening the repository. Host approvals are not relaxed.
- Pinned noneditable runtime: `C:/Users/juanf/AppData/Local/agent-checkpoint/harness/build-0.1.2/venv/Scripts/python.exe`.
  A pinned Node bootstrap in that build directory consumes the local Gateway
  credential silently and starts Python; it is not a second product runtime.
- Wheel SHA-256: `d95902e4d5639e7d2e6e11c77a99a9eee7335b11f589b15f900934dbf8ae44d8`.
- New harness state: `C:/Users/juanf/AppData/Local/agent-checkpoint/harness/0.1.2/state`.
  Prior N/self-use state remains preserved; no schema migration or destructive reset.
- CLI fallback: `& ./scripts/checkpoint.ps1 doctor --json` from the repository.
  The same root, reviewed checkpoint.json and state are used by CLI and MCP.
- AGENTS.md requires explicit task registration, routing, approved checks and
  completion reporting for substantive implementation tasks. This is procedural
  integration, not automatic stop enforcement. Direct verification stays available.

Lint/format now include scripts; all checks allow only the nonsecret UV_CACHE_DIR
in addition to the runner's OS variables. This is a reviewed policy change: old
contracts keep their old policy digest and are not reused as current evidence.
The MCP configuration explicitly forwards the launcher's nonsecret OS/cache
allowlist. MCP's default Windows environment omits variables such as WINDIR and TMP;
without explicit forwarding, the same files can correctly produce stale evidence
when switching to CLI. Environment identity checks remain enforced.

## Activating the native tool connection

Codex loads project MCP configuration only for trusted projects. Restart the MCP
connection/app or open a new Codex session for this repository, then inspect `/mcp`.
The current running conversation may still need the explicit CLI fallback; a parsed
configuration or standalone client exchange is not proof of native tool invocation.
The OpenAI Docs skill guided the project scope and timeout settings using the
[official MCP documentation](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).
No global config or project trust setting was changed by the agent.

## Remote and unsupported features

Only Jev through Vercel Gateway is permitted. The user explicitly approved the
implemented task-routing and criterion-review payloads and spending on 2026-09-27.
checkpoint.json now enables both `single_route` and `criterion_evidence` through
`approvedPayloadKinds`; exact approvedInputDigests remain an alternative for narrower
policies. This approval is launcher-owned, not writable through MCP arguments.

Routing sends task text and optional skill descriptions. Review sends criterion
text and selected check IDs/status summaries, not raw outputs or source files.
Keep task text short and sanitized; don't paste source or secrets into task records.
Six physical requests total per task, 16 KiB requests, 10-second deadline, no retries.
The user reports a $5 Gateway key budget; the application does not attest or enforce
an aggregate dollar cap. Provider failures remain explicit and have no model fallback.

The pinned bootstrap loads .env.local at runtime, forwards only AI_GATEWAY_API_KEY
and allowlisted OS/cache variables, and never prints credentials. Agent tools must
not inspect that file or log keys. Check subprocesses do not inherit the credential.
No hosted telemetry, alternate models, native hooks or automatic continuation were
enabled. Claude Code configuration is unchanged by this Codex integration.

The first real Python Gateway routing call succeeded for this integration task:
backend-testing selected, 384 input / 40 output tokens, 1.048 seconds, one physical
request, zero retries; billed cost unknown. The live probe report and the configured
MCP/CLI validation report are retained outside the checkout under
`C:/Users/juanf/AppData/Local/agent-checkpoint/harness/`. Native Codex tool invocation
still requires the connection to load; a standalone client is not native-host proof.

## Recovery

Set only `mcp_servers.checkpoint.enabled = false` in the project config and restart
the connection to disable native MCP. Omit CLI wrapper calls and run the direct
AGENTS.md commands if the runtime is unhealthy. Preserve harness state and task IDs
for diagnosis. Never delete state, waive checks, or turn an unknown result into pass.
Do not rebuild the pinned installation in place: independently validate a new build
and explicitly update both launchers, preserving compatible state/rollback artifacts.
