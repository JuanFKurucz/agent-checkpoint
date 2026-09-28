# Security, privacy, and trust

Status: proposed controls for this product. Current host and provider terms still require the checks in the [source register](../research/sources.md).

## Authority boundaries

The user and host authorize execution. Repository policy contributes requirements within that authority. Mechanical observations describe actual check outcomes. Semantic results are advisory evidence classifications. Candidate descriptions, code comments, diffs, and model answers do not gain execution authority by appearing in a decision payload.

Remote calls default off for all repositories. Enabling Jev requires provider enablement and an explicit repository data policy. Raw request/response payload persistence is off by default. Opt-in does not imply zero retention at the provider.

## Threats and concrete responses

| Threat | Response | Residual limitation |
|---|---|---|
| Agent fabricates test success | Separate claimed and observed provenance | Same-user local state is not tamper-proof |
| Change weakens its own checks | Pin definitions; detect policy changes; use trusted CI policy | Maintainers still review intended policy changes |
| Secrets leave in diff or output | Evidence-kind allowlist, size caps, secret scanning, deny on suspected secret | Redaction alone cannot prove absence of sensitive content |
| Repository text injects instructions | Separate trusted rubric from untrusted evidence; validate outputs | Semantic model may still misclassify |
| Unsafe check command | Approved IDs, argv execution, environment allowlist, time/output limits | Test scripts execute repository code |
| Duplicate hooks create loops | Durable event deduplication and atomic task budget | Host delivery semantics need testing |
| Another worktree's result is reused | Full identity and snapshot binding | Filesystem identity must be canonicalized carefully |
| Provider outage | Bounded deadline, abstention/unknown, no pass fallback | Advisory result unavailable; independent required evidence may still be unresolved |
| Tampered CI artifact | Check run/commit/producer/digests and schema | Artifact sanitization is not authentication |

## Runner isolation

Keep provider credentials out of test environments. An environment allowlist must include only declared execution needs. Resolve executables deliberately; command arguments from a provider are never accepted. Use a trusted platform-specific launcher for Windows command wrappers if direct invocation cannot support them safely, and test quoting with spaces and metacharacters.

Environment filtering is not a sandbox. Repository code may still read user files or access the network if the execution environment permits it. Doctor must report whether isolation is present. Repositories requiring isolation must refuse to run if that requirement cannot be met. Independent CI should use an unprivileged clean environment.

Kill the process tree on timeout/cancellation where supported, bound log capture, distinguish truncation from complete output, and prevent arbitrary paths escaping the configured workspace through check configuration.

## Privacy and retention

Construct only the evidence needed for the specific question. Approved metadata is still potentially sensitive. Do not send full environments, entire transcripts, or entire repositories.

Persist operational metadata and redacted bounded artifacts. Before field trials, define local retention duration, deletion behavior, backups, access permissions, and blob garbage collection. Exports must declare omitted/redacted fields; an incomplete export cannot silently become stronger evidence.

No local/self-hosted Jev product is assumed. “Local provider” means mocks, deterministic heuristics, or a separately validated local model. Provider terms, retention, and organizational data approval are open items, not resolved legal conclusions.

TypeSafe's current [legal overview](https://docs.typesafe.ai/legal) advertises enterprise ZDR. This corrects the older report's categorical availability concern; it does not establish that this account has that arrangement. Verify applicable terms and permitted data before enabling private-content evaluation. No account access or legal entitlement was tested during consolidation.

## CI boundary

Do not execute untrusted repository code in a secret-bearing semantic evaluator. A trusted workflow selects the policy revision, verifies artifact origin and candidate commit, and reruns deterministic checks. Checkpoint reports cannot waive branch protection or host approval.

The CI task includes review of official platform guidance before selecting an event or privilege model; see [TASK-15](../planning/backlog.md).

