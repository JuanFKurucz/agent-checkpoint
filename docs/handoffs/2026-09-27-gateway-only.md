# Gateway-only increment handoff

Goal remains active and incomplete. This turn made concrete progress, not a blocker.
The user explicitly requires **only Jev through Vercel AI Gateway**. This supersedes
earlier direct-TypeSafe and GPT-example plans. Never inspect `.env.local`, copy the
chat credential, or print/log/commit a credential. The file is confirmed Git-ignored.

## What changed

- `gateway.py`: optional Python SDK adapter with fixed Vercel URL and Jev model;
  rejects other models/endpoints/key-env names, ignores TypeSafe endpoint/model env
  overrides, disables redirects/proxy inheritance and SDK retries, bounds input and
  total deadline, reserves physical calls atomically, protects duplicate requests,
  sanitizes failures and records no raw provider input/output payloads.
- Remote use is disabled by default. The policy's opt-in is internal; CLI/MCP
  callers must not be allowed to authorize their own remote data scope or spend.
- Semantic Choice supports route and criterion-evidence variants. It supplies no
  required mechanical/manual authority. Exact model pin remains unverified because
  the gateway exposes an alias. Mismatched response identity fails unavailable.
- Check events have started/finished phases; latest start wins over late finish;
  any still-started run keeps evidence unknown. Malformed transitions fail closed.
- Completion uses atomic revision/evidence-high-water comparison on publication.
- TypeScript setup example now calls only Jev via explicit Gateway evaluation.
  Its live synthetic request succeeded: see the sanitized JSON report in reports.
  The older GPT test is historical evidence only, not an authorized future model.

## Remaining before goal completion

Trusted repository configuration, CLI, all five MCP tools, local routing and review
service wiring still need implementation. Python gateway adapter has offline tests
but no live request yet. Native-host integration and clean installed runtime are
not tested. Do not represent the TypeScript smoke as Python-runtime compatibility.

Continue the foundation handoff's roadmap: executable/dependency identity, explicit
interrupted-run recovery, revision API, config, CLI/MCP, isolated promotion support,
independently installed build N, shadow then two genuine follow-up self-use tasks,
three baseline/intervention scenarios, promotion/rollback/manual escape, final MVP
report. No goal/task acceptance gate is satisfied merely by this smoke test.

Before self-use on the actual checkout, ensure snapshotting does not read secret
file contents; the existing whole-workspace snapshot implementation includes ignored
inputs. Tests currently run only on disposable synthetic repositories. Define and
test a conservative credential-file exclusion/metadata policy first.

Other review targets: explicit response-size limit; service trust boundary for
approval and mandatory skill rules; data-scope and spend acknowledgement wiring;
no authenticated manual attestation yet; no upgrade migration from old phase-less
check events (prototype state must not be silently promoted as valid evidence).
Direct test commands remain available when the product is broken.

## Verification

Targeted new suite: 18 offline tests passed. Windows asyncio needs loopback-only
socket access for its internal socketpair; gateway tests allow 127.0.0.1/::1 only,
use MockTransport, and keep external sockets blocked. Ruff and mypy pass; build
produces a wheel/sdist. See `../verification.md` for the final complete-suite result.
No Git commit/push, global host edit, private-data upload or background job was made.

The Backend Testing skill drove red-before-green regression fixtures. The AI SDK
skill drove installed-source API verification, live model-catalog lookup and tsc.
