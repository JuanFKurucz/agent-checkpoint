# Research synthesis

The post-MVP report is now [reconciled against the implementation](harness-validation-consolidation.md).
That update and [current status](../status.md) supersede implementation-status
assumptions in this historical design synthesis.

Status: consolidated through the revised engineering report and the user's Python/LangChain follow-up, with limited primary-source checks on 2026-09-27. See the [revision notes](revised-plan-consolidation.md) and [Python reassessment](python-langchain-assessment.md).

## Central conclusion

The strongest supported product direction is a reusable task-and-evidence runtime. Jev is a plausible way to answer small semantic questions within it. Neither the supplied report nor this repository establishes that Jev improves coding-agent success, latency, or total cost.

The brainstorm identified routing and quality checks. The exploratory brief made those testable hypotheses. The deep report contributes a more concrete provider shape, durable storage, adapter boundaries, and evaluation protocol. It also introduces implementation assumptions that need compatibility tests.

## Resolutions and corrections

| Issue | Source tension | Consolidated direction |
|---|---|---|
| Runtime structure | Earlier TypeScript-only proposal omitted existing Python integrations | One package; evaluate Python first, LangChain adapter versus direct SDK; TypeScript remains an alternative |
| Runtime version | SDK minimum interpreted as product runtime target | Select and pin the tested runtime after TASK-01; Node 24 is the TypeScript alternative, not a Python requirement |
| State location | Original repository tasks folder; report user-data database | Commit config/policies; keep mutable SQLite and blobs outside checkout |
| Provider abstention | Earlier brief asks whether native unknown exists | Explicit none candidate and application-owned unknown; no assumed native abstention |
| Confidence | Example generic confidence field | Preserve provider-native optional fields; calibrate by question type |
| Task activation | Explicit configuration but report sequence implies prompt auto-start | Prompt hooks resolve an already registered task; new task activation remains explicit |
| Semantics versus enforcement | Required semantic judgment could become self-approval | Explicit mechanical/manual evidence_policy for required criteria; model findings remain optional advice |
| Completion mode input | Example MCP input lets caller choose mode | Effective mode comes from trusted configuration; caller cannot weaken gates |
| Snapshot input | Example caller supplies current snapshot | Runtime computes and checks current snapshot; supplied ID is only an optimistic precondition |
| Model identity | Pinned model requirement versus null/moving aliases | Initial jev-1.13.0 evaluation pin; record requested/returned identity and reject substitution |
| MCP generation | SDK v2 confirmed; host examples may differ | Target v2/2026-07-28, then pin a tested SDK/host tuple; identity never depends on transport sessions |
| Catalog cardinality | Report cites a limit of 255 | Prefilter to a much smaller budget; verify limit before any dependency on it |
| Task scope | Report suggests automatic subagent recommendations | Recommendation only, subject to host/user authority; initial slice focuses on skills |
| CI evidence | Artifacts described as sanitized and trusted | Verify producer, commit, policy, run identity, and artifact integrity; sanitization alone is insufficient |

These choices are recorded as [proposed ADRs](../adr/README.md), not claims of stakeholder ratification.

## Gaps that remain after the report

A hash of workspace inputs detects many stale results but cannot prove that a live file tree remained unchanged during a test. Concurrent edit-and-revert events, ignored inputs, symlinks, submodules, dependencies, and generated files need explicit treatment. The design uses conservative invalidation, mutation tracking, and independent CI; it does not turn a local fingerprint into a security attestation.

Moving evidence outside the repository reduces accidental edits but does not protect against a process running as the same OS user. Likewise, removing credentials from a child environment is not a filesystem sandbox.

The proposed provider interface in the report allows callers to request arbitrary generic return types. Implementation should instead use a discriminated request/result union validated at runtime. A typed SDK alone cannot guarantee that the application used the right rubric or mapped the answer correctly.

The reports' completion examples need required flags, criterion origins, evidence authority, contract revisions, provenance, and separate advisory findings to make aggregation unambiguous. Those fields are defined in the [contracts](../architecture/contracts-and-evidence.md). The latest report's alternate field names are reconciled in the canonical interface reference rather than treated as a parallel API.

## Evidence interpretation

The source register now includes selected Node, model, enterprise-ZDR availability, MCP and Codex hook checks. Account-specific privacy terms, exact installed-host behavior, pricing, provider cardinality and benchmark results are not validated product facts. A report calling something verified is not sufficient to call it tested here.

The external source checks do not validate report snippets as compilable code. No dependencies were installed, no private repository data was sent to Jev, and no coding-agent trials were run.

## Research outcome options

1. Evidence tracking helps and Jev helps further: build both, with selective provider use.
2. Evidence tracking helps but Jev adds no value: ship deterministic workflows and retain a replaceable provider interface.
3. Routing improves but completion does not: narrow the first use case.
4. Quality improves at added cost: position a quality mode with measured trade-offs.
5. No meaningful system-level improvement: stop the intervention and preserve the negative results.

The [evaluation protocol](evaluation.md) distinguishes these outcomes before investment in broad hook integration.

