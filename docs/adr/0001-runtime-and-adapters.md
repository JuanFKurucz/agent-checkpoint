# ADR-0001: One runtime with thin adapters; Python-first evaluation

Status: Accepted for the internal MVP. Date: 2026-09-27.

## Implemented selection

The runtime is one Python package, tested on CPython 3.13.11, with shared services
behind CLI and MCP 2.2.0 adapters. The optional provider uses typesafe-sdk 0.7.2
configured exclusively for Vercel AI Gateway (`typesafe-ai/jev`). The plain SDK
provides async decisions, explicit retry control and an injectable transport without
requiring LangChain runnable/middleware/tracing dependencies. This is a complexity
choice, not a measured performance comparison with langchain-typesafe. LangChain
remains a valid future integration; neither LangGraph nor hosted LangSmith is enabled.

Locked dependencies, offline transport tests, real stdio exchanges and separately
installed CLI self-use validate the selected internal stack. Live Python Jev and
native host MCP invocation remain unverified. The user-requested TypeScript smoke
example is separate setup evidence, not a parallel product implementation.
See the [operating report](../reports/mvp-validation-report.md) for exact evidence.

The following context records the original decision process; its pre-implementation
language is historical, not current delivery status.

## Context

The sources alternate between one package, a monorepo, and an MCP-centered product. Core behavior must remain testable without an agent host. See the [research synthesis](../research/synthesis.md).

## Decision

Use one versioned package with internal core modules. MCP, CLI, hooks, and CI call shared services. Start with STDIO and CLI. Reopen the language choice before scaffolding: Python is the preferred candidate to evaluate, with TypeScript/Node 24 retained as the alternative, not a requirement.

The user's Python/LangChain sources correct the earlier assumption that Python was only an analysis companion. Evaluate `langchain-typesafe` against the direct `typesafe-sdk` Python client; keep both behind the same provider boundary. An official Python MCP SDK also exists, so MCP does not require a TypeScript runtime. See the [Python integration assessment](../research/python-langchain-assessment.md) for sources and the TASK-01 decision gate.

Do not adopt LangGraph or hosted LangSmith by implication. Deterministic core behavior remains independent of framework orchestration, provider calls, and telemetry. Pin the chosen Python/runtime, SDK, and dependency versions only after testing; no package or host tuple is validated yet.

## Alternatives

A multi-package monorepo adds release coordination before independent consumers exist. An MCP-centric core couples domain tests to transport. Python with the direct SDK minimizes framework coupling; Python with LangChain reuses its decision integration; TypeScript retains the earlier ecosystem choice. A mixed Python/Node runtime would add packaging and process boundaries without demonstrated need.

## Consequences

Shared domain schemas and a single release reduce duplication. Python packaging, cold-start overhead, SQLite behavior, subprocess cancellation, and MCP compatibility must be measured on Windows. Framework reuse can reduce integration work but does not supply our evidence authority, freshness, or promotion rules. Existing TypeScript paths in historical research are not implementation commitments.

## Revisit conditions

Select TypeScript instead if the bounded compatibility comparison shows a concrete Python blocker or a material delivery/operational disadvantage. Add LangGraph only for a demonstrated resumable workflow requirement, not merely because it supports Jev. Split packages when separate release ownership or consumers justify it; add HTTP only with demonstrated demand.

## Delivery and validation

[Backlog](../planning/backlog.md): TASK-03, TASK-11, TASK-12. Completion requires their stated acceptance evidence. Related decisions: [ADR index](README.md).

