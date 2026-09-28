# Interaction workflows

Status: proposed sequences. Host event names are integration candidates until the compatibility spike passes.

## Explicit task through MCP or CLI

```mermaid
sequenceDiagram
    participant U as Developer
    participant H as Coding host
    participant A as Adapter
    participant C as Checkpoint core
    participant S as Local store
    participant J as Decision provider
    participant R as Check runner
    U->>H: Implementation request
    H->>A: start_task with explicit criteria
    A->>C: Validate task and scope
    C->>S: Persist contract revision
    C-->>H: Task ID
    H->>C: route for task and phase
    C->>C: Preserve mandatory resources and filter candidates
    opt Remote evaluation enabled and budget available
        C->>J: Bounded choice including none
        J-->>C: Typed result
    end
    C-->>H: Allowed recommendation or abstention
    H->>H: Implement using native tools
    H->>C: run_checks using approved IDs
    C->>R: Execute and capture input identity
    R-->>C: Exit status and evidence
    C->>S: Persist run and freshness
    H->>C: completion for task
    C->>C: Revalidate current snapshot and aggregate
    C-->>H: Ready, needs_changes, or unresolved
    H-->>U: Result with evidence and remaining gaps
```

Completion does not implicitly run checks, install dependencies, or edit code. Suggested next actions are constrained identifiers and templates, not provider-generated shell commands.

## Native stop adapter

```mermaid
flowchart TD
    E["Stop event"] --> I{"Registered task and verified capability?"}
    I -->|No| N["Return without completion enforcement"]
    I -->|Yes| D{"Duplicate event?"}
    D -->|Yes| R["Return recorded response"]
    D -->|No| C["Compute current completion report"]
    C --> M{"Mode allows continuation for this mechanical gap?"}
    M -->|No| P["Publish report and let host stop"]
    M -->|Yes| B{"Budget remains and action is actionable?"}
    B -->|No| P
    B -->|Yes| T["Atomically reserve a pass and event response"]
    T --> H["Translate to verified host continuation payload"]
```

Missing credentials, ambiguous user requirements, unsupported capabilities, and semantic uncertainty are not repaired by repeatedly asking the agent to continue. Report them. A provider outage does not spend remediation passes. Observation permits zero continuations; an explicitly enabled mechanical pilot permits at most one across the task.

## Evidence lifecycle

```mermaid
stateDiagram-v2
    [*] --> Running
    Running --> Current: Successful observed run and stable inputs
    Running --> Failed: Nonzero exit
    Running --> Unknown: Missing observation or uncertain inputs
    Running --> Interrupted: Cancellation or process loss
    Current --> Stale: Relevant mutation or revision change
    Failed --> Stale: Inputs change
    Stale --> Running: Explicit new run
    Unknown --> Running: Explicit new run
    Interrupted --> Running: Explicit new run
```

Old records remain for audit. Re-running creates a new record; it never edits a historical failure into a pass.

## Independent CI

```mermaid
flowchart LR
    COMMIT["Exact candidate commit"] --> RUN["Unprivileged isolated checks"]
    TRUST["Trusted policy revision"] --> RUN
    RUN --> ART["Bounded artifacts and producer metadata"]
    ART --> VERIFY["Validate origin, commit, digests, and schemas"]
    TRUST --> VERIFY
    VERIFY --> RESULT["Independent deterministic report"]
    VERIFY --> OPT["Optional separate semantic evaluator"]
    OPT --> ADVICE["Advisory findings"]
```

CI must establish its own task/commit context and rerun required verification. Importing a local ready report is not independent verification. An exported local artifact is comparison data until its provenance is established.

