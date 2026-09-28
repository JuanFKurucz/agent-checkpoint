# Open questions and decision register

Status: unresolved unless explicitly stated. Owner roles identify needed expertise, not assigned people.

| ID | Priority | Question | Resolution artifact | Role | Task |
|---|---|---|---|---|---|
| Q-01 | P0 | Does Jev add value beyond rules and self-judgment? | Held-out and whole-task comparison | Evaluation lead | TASK-10, TASK-18 |
| Q-02 | P0 | Which provider terms permit the intended repository data? | Approved data classes and retention assumptions | Maintainer/data owner | TASK-02 |
| Q-03 | P0 | Which exact SDK/host/protocol tuple works? | Compatibility fixture and live smoke records | Integration engineer | TASK-01, TASK-12 |
| Q-04 | P0 | Can freshness survive concurrent edits and ignored inputs? | Adversarial fixture results and overhead | Runtime engineer | TASK-06 |
| Q-05 | P0 | How are criteria omissions and unauthorized revisions detected? | Origin/revision tests and independent review protocol | Core engineer | TASK-04, TASK-10 |
| Q-06 | P1 | Which SQLite binding packages cleanly across platforms? | Packaging, transaction, migration results | Runtime engineer | TASK-03, TASK-05 |
| Q-07 | P1 | How does Codex identity survive restart/compaction? | Session/task mapping and repeated-event tests | Codex integrator | TASK-13 |
| Q-08 | P1 | What are Claude's current hook contracts? | Primary references, payload fixtures, live demo | Claude integrator | TASK-17 |
| Q-09 | P1 | What default latency/call/spend budget is useful? | Pilot budget sensitivity analysis | Evaluation lead | TASK-09, TASK-10 |
| Q-10 | P1 | What local retention and deletion policy is appropriate? | Retention spec and recovery test | Runtime maintainer | TASK-05, TASK-16 |
| Q-11 | P1 | What runner isolation is available on each OS? | Capability results and strict-mode behavior | Runtime/security engineer | TASK-06 |
| Q-12 | P2 | Do context/check/model/subagent interventions help? | Separate ablation for each | Agent researcher | TASK-20 |
| Q-13 | P2 | Does architecture scoring improve real review decisions? | Human-adjudicated rubric experiment | Reviewer/researcher | TASK-20 |
| Q-14 | P2 | Is shared remote state necessary? | Concrete multi-user requirements and ADR | Maintainer | TASK-20 |

## Resolved for the proposed baseline

Abstention is application-owned. Initial package count is one. Mutable evidence lives outside the repository. Required unknown remains unresolved, and semantic advice cannot independently pass or fail a required criterion. Native continuation is separate from report status. The MCP process is not task identity. These are [design choices](../adr/README.md), not empirical findings.

The earlier Node/TypeScript-only proposal is reopened by the [Python integration assessment](python-langchain-assessment.md): evaluate Python first, including LangChain versus direct SDK and Python MCP compatibility. Exact runtime/dependency pins and a tested host tuple remain open; `jev-1.13.0` remains the initial evaluation model. Working-tree and isolated-snapshot evidence are distinct; promotion requires the latter. Hook rollout starts with zero automatic passes, followed by an opt-in one-pass mechanical pilot. Enterprise zero-data-retention availability does not settle Q-02: our account terms and permitted data classes still require approval.

## Questions to take back to researchers

Prioritize failure prevalence and economic impact: which real tasks waste enough time for a checkpoint to help? Ask for anonymized traces with original requirements, catalogs, tool results, final changes, and later corrections. A confident but wrong route is less informative than knowing what rework it caused.

For Jev, recover exact response semantics, model version controls, concurrency/retries, payload limits, and data-handling terms. For hosts, request current documented hook contracts and repeatable fixtures. For evaluators, agree on label ambiguity, leakage controls, and thresholds before final runs.

Close questions with artifacts and dates. Avoid replacing an open question with an unsupported default disguised as a fact.

