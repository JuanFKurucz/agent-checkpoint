# Agent Checkpoint development

Use Python 3.13 and the checked-in uv.lock. Read docs/planning/implementation-progress.md
and the latest handoff before resuming the active MVP goal. Preserve existing user work.

## Direct checks (implemented)

- `uv sync --locked --extra jev`
- `uv run --locked --extra jev ruff check src tests`
- `uv run --locked --extra jev ruff format --check src tests`
- `uv run --locked --extra jev mypy`
- `uv run --locked --extra jev pytest -q`
- `uv build --no-sources`

## Active Checkpoint harness (this repository)

For substantive implementation tasks, use the `checkpoint` MCP tools when available.
Until this session loads them, use `& ./scripts/checkpoint.ps1 <command>`; it selects
the same separately installed 0.1.2 build and outside-checkout harness state.
Do not use the editable candidate runtime as its own active supervisor.

1. Register the user request and substantive criteria before edits with
   checkpoint_start_task (CLI: task start). Put CLI request/contract files under
   C:/Users/juanf/AppData/Local/agent-checkpoint/harness/0.1.2/requests, not this checkout.
2. Call checkpoint_route (CLI: route) for the skill shortlist. Mandatory instructions
   and explicitly requested skills always apply, regardless of routing advice.
3. Implement, then call checkpoint_run_checks (CLI: check run) with lint format types
   tests. Inspect failures and fix the actual gap; use new request IDs for reruns.
4. Call checkpoint_completion (CLI: complete --json) before claiming implementation
   complete. If inputs change after checks, rerun; never weaken requirements to pass.
5. checkpoint_review (CLI: review) is now opt-in for a specific evidence experiment,
   not a routine completion step. Check-status summaries alone do not establish
   semantic coverage. Keep routing advisory; do not disable Jev globally. For an
   explicit review experiment, pass relevant finished run IDs and retain abstention.
   The user approved live Jev task-routing and
   criterion-evidence payloads on 2026-09-27: task text, skill descriptions, criterion
   text and check IDs/status summaries. Keep task text concise and free of secrets
   or pasted source. Never upload raw source files or check-output blobs implicitly.
   Six physical Gateway requests total per task, 16 KiB input limit, 10-second
   deadline, no retries. Failures stay unavailable; no alternate model or endpoint.
   Record task IDs and Jev usage/results in the handoff. Advice never decides a
   required pass/fail. The user reports a $5 Gateway key budget; billing remains
   externally enforced/unverified, not a claimed application-level dollar cap.

Read-only questions need not create tasks or trigger the full suite. A broken runtime
does not block direct verification: disclose the failure, preserve state, and use the
commands above. Do not silently relabel unresolved evidence ready. Do not recursively
invoke Checkpoint from tests or check definitions. Native hooks remain unimplemented.

Start with docs/status.md for current state. Candidate 0.1.9 preserves dashboard
focus while polling and includes bounded history pairing; pinned 0.1.2 still emits schema 1 and
exposes five tools until a separately validated promotion. Typed next_actions never
grant permission or execute repairs. History reports never establish current readiness.

Project MCP configuration is .codex/config.toml; restart/reload the Codex MCP connection
after changes. See docs/guides/active-harness.md for installation identity and recovery.

Tests deny sockets by default and use temporary repositories/state. No credentials
are needed. Dependency installation may need network; runtime verification does not.
Node.js is a development-only prerequisite for the offline dashboard DOM regression
run by pytest. It is not required by the installed Python runtime.

## Invariants

- Required evidence is mechanical/manual; Jev advice cannot create a required pass.
- Keep failed, missing, stale, interrupted and unavailable results distinct.
- Complete never runs checks or calls a provider implicitly.
- Validate task/worktree/revision/snapshot associations at every service boundary.
- Preserve immutable revisions; never silently weaken criteria or required checks.
- State lives outside the evaluated checkout. Environment filtering is not a sandbox.
- Never imply working-tree checks provide isolated-snapshot guarantees.
- Provider calls are approved only for the two payload kinds above; hosted telemetry
  remains disabled. Runtime credential loading is allowed; never inspect or print keys.
- The only authorized live model is Jev through Vercel AI Gateway. Use
  typesafe-ai/jev and AI_GATEWAY_API_KEY; no direct TypeSafe endpoint, alternate
  gateway, generative-model fallback or further GPT-5.5 calls. The earlier GPT
  smoke result is historical evidence only. Never inspect .env.local contents.
- Use installed pinned N for self-use, not a live rebuilt hook from candidate N+1.
- Keep direct checks and manual recovery usable when the product is broken.

No publication, Git push, global host edits, background agents, or recurring jobs
without separate user authorization. Mark tasks complete only with observed evidence.
