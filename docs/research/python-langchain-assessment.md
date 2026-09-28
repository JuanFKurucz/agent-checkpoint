# Python, LangChain, and Jev: runtime reassessment

Date: 2026-09-27. Status: source-checked design proposal; no dependencies installed or provider calls made. This updates the earlier TypeScript-only direction in [ADR-0001](../adr/0001-runtime-and-adapters.md).

## What the sources establish

The [LangChain harness article](https://www.langchain.com/blog/building-a-harness-with-jev) demonstrates Python Jev integration through `langchain-typesafe`, including classifier use and experimental agent middleware. This is existing integration code we can evaluate, not a reason to implement a TypeScript adapter from scratch.

The [integration reference](https://docs.langchain.com/oss/python/integrations/providers/typesafe) exposes `TypeSafeClassifier` as a Runnable. Current invocations carry both state and questions; earlier examples used a different shape. Results include typed answers, returned model, usage, and provider request ID. Pin and test a specific release rather than copying an undated snippet.

There is also an [official direct Python SDK](https://github.com/typesafe-ai/typesafe-sdk-python), packaged as `typesafe-sdk`. Python therefore does not require LangChain just to call Jev. The [official Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk) documents v2 and the 2026-07-28 protocol; this establishes an alternative adapter ecosystem, not tested compatibility with our installed hosts.

The [LangGraph article](https://www.langchain.com/blog/building-prod-with-jev-and-langgraph) and its [linked Python example](https://gist.github.com/sydney-runkle/a632ba4ea0b2b72501dfa4b6ab2a7d8a) illustrate decision nodes, deterministic routing, and human escalation. The reported classification speedup is specific to that example, not evidence of coding-task savings here.

The [LangSmith evaluator guide](https://docs.langchain.com/langsmith/decision-model-evaluator) is a separate product surface: decision evaluators are created through the UI, not through LangSmith SDK creation APIs at the time checked. It supports Jev with a supplied TypeSafe key. This is an optional evaluation workflow, not our local runtime or completion authority.

## Proposed boundary

| Layer | Python-first candidate | Still our responsibility |
|---|---|---|
| Core | Typed Python domain models and pure reducer | Task identity, authority, freshness, idempotency, budgets |
| Jev adapter | Compare langchain-typesafe with direct typesafe-sdk | Validate answers, enforce model pin, abstain, account for actual calls |
| Host surface | Official Python MCP SDK plus CLI/hook adapters | Host contracts, cancellation, stdout hygiene, capability checks |
| Workflow | Ordinary service calls initially | Durable task/evidence lifecycle |
| Optional orchestration | LangGraph if a concrete workflow needs it | Idempotent side effects and no conflicting state authority |
| Optional evaluation | LangSmith or local evaluation runner | Independent labels, leakage controls, provider/telemetry approval |

This is a proposed engineering boundary, not a claim that the libraries already implement Agent Checkpoint. LangGraph checkpoints are execution state; our evidence records have different authority and freshness semantics. Native Codex and Claude Code remain the coding hosts. LangChain middleware examples do not establish control over their internal loops or permissions.

## Bounded comparison before TASK-03

Extend TASK-01 with one synthetic fixture and a compact decision record, not a parallel implementation of the product:

1. Record candidate runtime/package versions, license/dependency footprint, installation and cold-start behavior on Windows. Compare Python first; retain Node 24 as the fallback baseline.
2. Exercise the same mocked Choice/Noul/Score inputs, malformed outputs, explicit none/unknown handling, and model identity mapping through each candidate provider adapter.
3. Verify async behavior, cancellation, retry ownership, request deadlines, physical-call accounting, and usage availability. A background request continuing after caller timeout is not successful cancellation.
4. Run a minimal MCP STDIO exchange and CLI invocation without provider credentials. Record negotiated protocol and host/version limits; do not assume the two languages' SDK APIs are interchangeable.
5. Inspect tracing/callback defaults and prove the offline fixture sends no data. LangSmith export requires a separate destination/data approval; permission to call TypeSafe does not authorize another recipient.
6. If separately authorized, run a synthetic pinned-model smoke test. Otherwise record live access as unverified; it need not block the deterministic scaffold.

Choose the smallest integration that meets the contract. Prefer the LangChain adapter when its composition and instrumentation save meaningful work without compromising budgets, startup, or privacy; prefer the direct SDK if those abstractions add no value. Neither choice requires LangGraph or a hosted service.

## Roadmap consequences

TASK-01 selects and records the runtime/adapter direction. TASK-03 then creates one scaffold in that language. TASK-04 implements the same evidence contracts and pure reducer. TASK-09 uses the chosen Jev adapter, and TASK-10 may evaluate optional LangSmith support under a separate data boundary. All remain open.

No changes are needed to the five public MCP tools, readiness states, semantic-advisory restriction, native-bootstrap approach, or pinned N/N+1 promotion model. Update effort estimates after the spike; existing integrations do not by themselves prove lower end-to-end cost or latency.
