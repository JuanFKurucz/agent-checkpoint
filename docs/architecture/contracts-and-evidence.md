# Contracts, evidence, and readiness

Status: proposed v1 domain model. These definitions govern every interface.

## Identity and records

| Record | Required identity and content |
|---|---|
| Repository | repo_id, canonical root, Git identity; remote URL alone is insufficient |
| Worktree | worktree_id, repo_id, canonical worktree path |
| TaskContract | task_id, worktree_id, request reference/text, revision, scope, criteria, required checks, policy digests |
| Criterion | stable id, text, origin, required flag, evidence_policy, evidence requirement, satisfaction rule |
| SessionBinding | host, session_id, optional turn/agent id, task_id |
| Snapshot | id, scope manifest, input digests, contract revision, environment identity, mutation generation |
| CheckRun | run id, task id, execution_mode, before/after snapshot, check-definition digest, status, exit code, timing, output references |
| Evidence | id, task/worktree, snapshot, kind, provenance, source run, digest |
| Decision | id, input fingerprint, task/revision, rubric, requested/returned model, native result, disposition, usage |
| CompletionReport | id, current snapshot, contract revision, criterion states, required-check states, advisory findings, next actions |
| ContinuationReservation | task id, event id, pass number, status, timestamps |

A repository can have multiple worktrees, each with multiple tasks and host sessions. Queries must check the full identity association; knowledge of an evidence ID does not authorize its use in another task.

## Contract changes

Origins are user, repository, and agent_proposed. The task service records the original request and criteria, so the agent cannot pass simply by omitting difficult requirements. A proposed criterion is visible as an inference.

Revisions are append-only. A change must supply expected revision, reason, and authorized actor. User/repository requirements cannot be silently removed or weakened. Conflicting requirements yield unresolved status and a request for clarification. The toolkit cannot create authority beyond the user's and host's actual instructions.

Initial tasks require at least one substantive criterion. An empty contract cannot be ready. Cancellation is a task lifecycle state, not a passing criterion. Planning or conversational turns have no implementation contract unless explicitly registered.

## Criterion status and readiness

### Evidence authority

Each criterion declares `evidence_policy` independently of its origin and satisfaction rule. Internal naming follows the selected language; the wire contract uses snake_case.

| Evidence policy | What can establish satisfaction | MVP constraint |
|---|---|---|
| mechanical | Current recorded execution or another approved deterministic observation | Required checks remain authoritative |
| manual | An authorized, identified reviewer attestation bound to the criterion and snapshot | Cannot waive a separately required mechanical check |
| semantic_advisory | A bounded model finding for investigation | Optional only; cannot be the authority for a required pass |
| informational | Context with no completion authority | Optional only |

Reject any required criterion whose evidence_policy is semantic_advisory or informational. Do not silently downgrade a user's requirement. Clarify its satisfaction rule or record it as a required manual/mechanical criterion with unknown evidence. Optional semantic findings can reference that required criterion without deciding its state.

For example, a model can suggest that a test covers malformed input. An approved behavioral test or authorized review must establish the required coverage criterion. The model's positive answer alone never promotes it to pass. A model's negative answer likewise cannot independently overturn an authoritative result; it is a visible finding to investigate.

| Criterion state | Meaning |
|---|---|
| pass | Its declared satisfaction rule has current supporting evidence |
| fail | Current evidence contradicts it or its required mechanical check fails |
| unknown | Evidence is missing, stale, inconclusive, inaccessible, or outside the trusted provenance class |
| not_applicable | A recorded applicability rule or authorized revision excludes it |

A green command supports “the check passed.” It does not alone support “this test exercises the requested behavior.” Evidence sufficiency must be judged against the criterion's declared rule.

Readiness uses this precedence:

1. Invalid identity, contract, or policy prevents evaluation and returns an error or unresolved report.
2. A failed required check or failed required criterion yields needs_changes.
3. Otherwise any required unknown yields unresolved.
4. Otherwise all required criteria must pass or have justified not_applicable, and all required checks must pass, to yield ready.

If failures and unknowns coexist, needs_changes wins while both are listed. Optional findings stay visible but do not change readiness. Never average criterion scores.

Semantic classification remains in advisory findings. Required readiness is reduced from authoritative mechanical/manual evidence; Jev alone cannot promote or fail a required criterion. A ready report means the recorded contract is supported under the configured evidence rules; it is not proof of global correctness or release approval.

## Readiness versus action

Readiness reports and host control are separate. Observe records; advise displays; enforce may request continuation for explicitly configured mechanical failures. Semantic findings never trigger blocking in the MVP. Missing required manual evidence remains unknown even if the semantic finding is positive; it does not trigger a mechanical continuation.

A user can read an unresolved report and decide how to proceed. The interface must not relabel it ready to allow the host to stop.

## Provenance

| Provenance | Permitted interpretation |
|---|---|
| agent_claimed | A claim requiring verification |
| host_observed | An observation with precisely documented host coverage |
| checkpoint_runner | Execution recorded by this runtime |
| ci_verified | Independently produced CI evidence with validated producer and commit |
| human_attested | Named reviewer judgment tied to criterion and snapshot |

Provenance describes origin, not universal trust. Each criterion declares acceptable sources. A user confirmation cannot waive a required mechanical check by masquerading as an execution result.

## Snapshot design

Hash a versioned canonical manifest, not an ambiguous concatenated string. Include base commit (or an explicit unborn-HEAD marker), staged/unstaged content identity, relevant untracked files, deletion/rename/mode changes, contract revision, policy and check digests, dependency lockfiles, runtime/tool identities, and other declared inputs.

The scope includes configuration and scripts that define checks. Exclusions must be explicit and reviewed. Git-ignored files may still affect execution; relevant ignored configuration needs identity without recording secret values. Missing or unbounded inputs produce unknown freshness. Unknown symlink, submodule, or external dependency behavior must not silently disappear from the manifest.

Initially invalidate all required evidence after any relevant mutation. Reuse is allowed only inside the same authorized task/worktree and matching revision, snapshot, check definition, and environment.

## Running against a live workspace

Record `execution_mode` separately from freshness. `working_tree` is the interactive mode: input hashes and mutation observations detect ordinary changes but do not prove isolation. `isolated_snapshot` runs against explicitly materialized, controlled inputs and separate output/state, and is required for critical promotion/release checks. Copying files alone is not sufficient if concurrent writers can still modify the check inputs.

An isolated run must identify the materialized manifest, including intended uncommitted changes when evaluating a local candidate; a clean base-commit checkout is not evidence for a different dirty workspace. Reuse still requires exact task, policy, check, and relevant environment identity. If a required execution mode is unavailable, report unknown instead of silently falling back.

1. Capture the manifest and mutation generation before execution.
2. Record the resolved executable, argv, environment profile identity, and check-definition digest.
3. Run with deadline, cancellation, bounded output, and explicit check identity.
4. Capture the manifest and mutation generation after execution.
5. If relevant inputs changed or mutation observation was incomplete, mark the run stale or unknown even when exit code is zero.
6. Recheck current identity before using results in a completion report.

Before/after equality alone misses edit-and-revert races. A watcher is advisory and can lose events. The prototype must test mutation generations and uncertainty handling; stronger release verification should use a stable checkout or isolated materialized snapshot in CI.

## Durable concurrency

Use transactions and expected-revision checks to prevent lost updates. Duplicate mutating requests return the original result only if the idempotency key and payload fingerprint match. Different payloads with the same key are conflicts.

Interrupted runs retain cancelled/interrupted states. No response, missing exit code, or partial output is success. Separate processes reserve continuation passes atomically, and duplicate host stop events cannot consume or create multiple passes.

Detailed wire examples are in [interfaces](../reference/interfaces.md).

