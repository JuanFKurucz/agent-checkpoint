# Usage manual

Status: proposed workflow for a future release. **The commands below cannot run from this repository today.** For work you can start now, use [next steps](../planning/next-steps.md).

## Before installation

Choose a disposable repository for the first demonstration. Identify its existing checks, required conventions, and one small implementation request. Pick the host and exact supported version after a compatibility record exists. Begin with local mock decisions and remote evaluation disabled.

## Target installation workflow

1. Install a published or locally built, pinned runtime once the package exists.
2. Run the preview command and review its proposed configuration and executable hooks.
3. Apply the selected integration without overwriting existing entries.
4. Complete any host-native trust step.
5. Run doctor and a local mock-provider smoke test.
6. Enable remote evaluation only after reviewing the intended data bundle and budget.

Proposed commands:

```text
agent-checkpoint init --host codex --dry-run
agent-checkpoint init --host codex --apply
agent-checkpoint doctor
```

For Claude Code, use --host claude-code. Selecting a host does not imply native hooks are implemented. See [compatibility](../integrations/compatibility.md).

## Register the work

Create a task request and contract that identify what must be true when work finishes. Separate user requirements, repository rules, and agent assumptions. Declare required checks and scope exclusions.

```text
agent-checkpoint task start --request-file task.md --contract-file contract.json
agent-checkpoint task show task_demo
```

Use the returned task ID in place of task_demo. Review the normalized criteria before implementation. If a requirement is unclear, resolve it rather than declaring it not_applicable.

## Route and implement

```text
agent-checkpoint route --task task_demo --kind skill
```

Load any mandatory skills plus applicable optional recommendations through the host. A none result is legitimate. An unavailable provider is a different result and should be shown as unavailable. The agent implements through its normal authorized workflow.

## Gather evidence and inspect completion

```text
agent-checkpoint check run --task task_demo typecheck test
agent-checkpoint review --task task_demo
agent-checkpoint complete --task task_demo --json
```

Only configured IDs are executable. Review may report provider disabled while retaining valid mechanical evidence. Completion does not run omitted checks automatically.

| Report | Operator action |
|---|---|
| ready | Inspect evidence and scope; continue normal review/release process |
| needs_changes | Fix the listed required failure, then gather new evidence |
| unresolved | Supply missing evidence, clarify criteria, or report the limitation |
| advisory finding | Investigate if useful; it does not by itself grant blocking authority |

Example: typecheck and tests pass, but there is no evidence that invalid-input behavior is covered. The report remains unresolved for that criterion. Add or identify the relevant test and rerun when inputs change.

## Optional automation

After observe-only trials, enable only the supported mechanical continuation behavior you intend. Automatic remediation defaults off with zero allowed passes. The first enabled pilot permits one pass across the task, not one per session or subagent.

A cap being exhausted leaves the task incomplete. Stopping the host and declaring the task ready are different operations.

## Export and uninstall

```text
agent-checkpoint evidence export --task task_demo --format jsonl
agent-checkpoint uninstall --host codex --dry-run
```

Exports carry provenance and redaction metadata. They do not constitute independent CI proof. Uninstall previews only toolkit-owned integration edits; evidence retention/deletion is a separate explicit operation. Never remove an entire host configuration file merely because Checkpoint added one entry.

The [operations manual](operations.md) covers failures, updates, and recovery.

