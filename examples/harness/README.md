# Portable harness configuration

This is a template, not the active author's installation. It does not install a
runtime, grant provider approval, promote the candidate or connect a host.

1. Install dependencies with the locked Python 3.13 environment and run the direct
   checks in the root README. Build and independently validate a noneditable wheel
   installation outside the repository before adopting it as a supervisor.
2. If no local `checkpoint.json` exists, copy the root `checkpoint.example.json`
   there. Review commands, timeouts and required checks. The template is offline.
   Never overwrite an existing host's configuration as an installation shortcut.
3. Select separate absolute paths for repository, pinned interpreter and external
   state. Keep candidate experiments away from active state. Use a matching root
   and state for subsequent CLI/MCP requests; evidence from a different identity
   is not interchangeable.
4. Adapt `codex.config.example.toml` into a local `.codex/config.toml`, preserving
   other MCP entries. Replace every placeholder, verify the executable identifies
   the intended installed package, then explicitly enable the connection. Reload
   the host and verify its tool list. The five-tool allowlist is the pinned baseline;
   candidate report support requires a separately validated adoption decision.
5. Test the offline doctor/task/check/completion flow. A host config file alone
   does not establish a successful native connection. Keep direct checks available
   if the pinned runtime is broken or the connection fails.

Equivalent CLI shape (replace all four values):

```powershell
& PINNED_PYTHON -I -m agent_checkpoint --root REPO --config CONFIG --state EXTERNAL_STATE doctor --json
```

The repository's ignored `scripts/checkpoint.ps1` and `scripts/checkpoint-launch.mjs`
belong to the author's local 0.1.2 installation and are intentionally not distributed.
The local AGENTS.md workflow documents that installation; fresh clones should use
the explicit installed-interpreter command after validation, or direct checks.

## Optional remote advice

The template deliberately does not forward a credential. Jev is only permitted
through Vercel AI Gateway with `AI_GATEWAY_API_KEY`, explicit spend approval and
approved payload scope. A local credential bootstrap may load the key at runtime
without inspecting or logging it. Do not copy the author's approval to a different
user/account. Never commit credentials or enable debug HTTP logging.

Keep six physical requests per task, 16 KiB input and a ten-second deadline, no
retries or alternate model/endpoint. Advice cannot satisfy required checks. Hosted
telemetry is not configured. See the operating guides for identity and recovery
limitations; most historical command examples refer to the original Windows host.
