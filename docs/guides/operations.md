# Operations and troubleshooting

Status: target runbook for a future implementation.

## Diagnose from the report

| Symptom | Likely cause | Safe next action |
|---|---|---|
| Provider disabled | Default privacy setting | Use deterministic workflow or review opt-in requirements |
| Provider timeout | Deadline, outage, throttling | Keep mechanical results; retry only within explicit remaining budget |
| Evidence stale after tests | Inputs changed during/after run | Inspect mutation reason, then run current checks |
| Tests green but task unresolved | Coverage or another criterion lacks evidence | Read criterion-specific reason; do not weaken criterion |
| Task belongs to another worktree | Incorrect session mapping or ID | Select the correct task; do not copy its evidence |
| Hook never runs | Unsupported host version, registration, or trust | Doctor; use explicit MCP/CLI until fixed |
| Repeated continuation | Event dedupe/budget defect | Disable automatic remediation, retain logs, investigate |
| SQLite busy | Concurrent writer or interrupted operation | Bounded retry; inspect process ownership; do not erase DB |
| Missing/corrupt blob | Interrupted write, deletion, or corruption | Mark referenced evidence unavailable and rerun |
| Changed policy | New governing definitions | Review revision and collect new evidence |
| Check times out | Hung process or insufficient bounded budget | Cancel process tree; record interruption, then diagnose check |
| Output truncated | Configured output cap | Preserve truncation flag; do not infer omitted results |

## Doctor's target checks

Report runtime and host versions, policy/schema validity, exact command availability, state-directory permissions, database migration state, provider enabled/disabled, desired/effective host capabilities, and isolation support. Credential presence can be shown as a boolean; never print the secret.

A green connectivity test is not evidence that a host hook has the claimed event coverage. Doctor should link a tested compatibility tuple or show unknown.

## Updates

Preview integration diffs, back up toolkit-owned edits, pin the new runtime, and run migration/contract checks. If a migration fails, preserve the original store and fail visibly. Do not silently open a new empty store and report that no tasks exist.

Recheck policies and installed skill content after updates. Provider/model/rubric changes invalidate decision caches. Evidence reuse across runtime changes requires an explicitly compatible identity rule.

## Retention and recovery

Before field trials, specify retention limits and how referenced versus orphan blobs are collected. Backups need a consistent SQLite snapshot plus referenced blobs. Exports are not a full backup unless they include every required field and artifact.

Restore to a separate location first and verify integrity. Mark pending runs interrupted after a crash. Resume task identity and budgets without resetting them.

## Escalation report

When filing a defect, include sanitized runtime/host versions, task/worktree identifiers, contract revision, reason codes, run IDs, whether inputs changed, and a minimal reproduction. Never attach raw private code or provider payloads by default.

