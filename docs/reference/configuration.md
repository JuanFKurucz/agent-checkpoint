# Configuration reference

Status: the internal runtime implements a strict JSON subset described in the
[runtime manual](../guides/internal-runtime.md), with checkpoint.json as this
repository's reviewed configuration. The broader YAML below is still design
material, not accepted configuration. Values are prototype defaults, not guarantees.

Current user constraint (2026-09-27) supersedes provider examples below: only Jev
through Vercel AI Gateway is authorized. The implemented internal GatewayPolicy
fixes base_url to https://ai-gateway.vercel.sh/typesafe, model to typesafe-ai/jev,
and api_key_env to AI_GATEWAY_API_KEY. Direct TypeSafe access and other models are
rejected, not fallback choices. This gateway alias is not an exact model-version
pin; Decision.identity_verified remains false. Remote use still needs explicit
data-scope/spend approval. The implemented JSON wiring is tested; the broader YAML
design below remains unimplemented.

## Illustrative repository config

```yaml
schemaVersion: 1
project:
  taskActivation: explicit
mode: advise
provider:
  kind: jev
  enabled: false
  apiKeyEnv: AI_GATEWAY_API_KEY
  model: typesafe-ai/jev
  timeoutMs: 2500
  maxCallsPerTask: 6
  checkpointDeadlineMs: 5000
  maxInputBytesPerCall: 65536
  maxSpendUsdPerTask: null
privacy:
  remoteEvaluation:
    allowed: false
    allowedEvidenceKinds: [task_summary, policy_excerpt, diff_fragment, check_summary]
  storeProviderPayloads: false
runtime:
  state:
    kind: sqlite
  evidence:
    maxInlineBytes: 32768
checks:
  typecheck:
    argv: [npm, run, typecheck]
    timeoutSeconds: 120
    required: true
  test:
    argv: [npm, run, "test:ci"]
    timeoutSeconds: 240
    required: true
evidence:
  freshness:
    strategy: whole-relevant-workspace
  executionMode: working_tree
  promotionExecutionMode: isolated_snapshot
completion:
  unknown: unresolved
  semanticBlocking: false
  automaticRemediation: false
  maxAutomaticRemediationPasses: 0
routing:
  skills:
    enabled: true
    maxCandidates: 40
  subagents:
    enabled: false
  model:
    enabled: false
hosts:
  codex:
    mcp: true
    hooks: false
  claudeCode:
    mcp: true
    hooks: false
```

This example assumes a target repository already defines those npm scripts. It does not configure this documentation-only repository to run them. Do not execute unknown repository scripts merely because their names match.

## Semantics and validation

| Setting | Meaning |
|---|---|
| mode | observe records; advise reports; enforce may act on explicitly configured mechanical gaps |
| provider.enabled and remoteEvaluation.allowed | Both must be true for a remote request; local mocks do not send data |
| provider.model | Current user-authorized transport fixes typesafe-ai/jev through Vercel. Record requested/returned identity and reject mismatches. This alias does not verify jev-1.13.0 or another exact version; keep exact-version reproducibility explicitly unverified |
| maxCallsPerTask | Includes physical retries and all child/session activity attributed to the task |
| timeoutMs | Total provider-operation deadline, including retries; also bounded by host event deadline |
| checkpointDeadlineMs | Total semantic review/routing checkpoint wall-clock budget; does not shorten an independently configured test timeout |
| maxSpendUsdPerTask | null means no dollar cap is claimed; call/input caps still apply. Enabled remote operation requires explicit budget acknowledgement or a positive cap with verified pricing |
| maxInputBytesPerCall | Serialized payload bytes, not token count |
| maxCandidates | Total Choice options including none; mandatory skills are handled before optional routing |
| automaticRemediation | Separate opt-in; false means a cap alone does not enable continuations |
| maxAutomaticRemediationPasses | 0 during observation; first pilot requires explicit enablement, enforce mode for configured mechanical gaps, and a cap of 1. Higher values need a later evaluated policy change |
| evidence.executionMode | working_tree for interactive checks; record pre/post state and uncertainty without claiming isolation |
| evidence.promotionExecutionMode | isolated_snapshot for critical promotion; unavailable isolation must not silently fall back |
| semanticBlocking | Must remain false in v1; reject true rather than silently ignoring it |
| runtime.state | OS user-data location by default; explicit override must pass path/isolation checks |
| hooks | Desired capability only; effective capability depends on installed version, trust, and doctor results |

No agent request can lower requiredChecks or mode for its task. User-level organization constraints can tighten repository settings. Conflicts produce explicit errors; environment variables supply named credentials, not a blanket configuration override.

The revised report proposes per-category call caps (two routing, two semantic review). Keep these as pilot parameters until the provider budget interface is validated; this v1 example uses the overall six-physical-call cap. The 2500 ms request deadline and 5000 ms checkpoint deadline are experiment defaults, not latency guarantees. Count SDK retries against both time and call budgets; verify SDK cancellation/retry controls rather than layering another blind retry loop.

Each check will also declare cwd, inputs, and envAllow alongside argv and timeoutSeconds. The runner resolves and hashes the full definition. A trusted platform environment profile supplies necessary OS/process variables; the check allowlist adds only approved values and never implicitly inherits provider credentials. Declare relevant ignored inputs explicitly and fail uncertain freshness when declarations are incomplete.

## Policy example

```yaml
schemaVersion: 1
id: testing.invalid-input
appliesWhen:
  changedPaths: ["src/api/**", "src/routes/**"]
mechanical:
  requiredChecks: [typecheck, test]
semantic:
  enabled: true
  blocking: false
  criterion: Changed validation has automated invalid-input coverage.
  evidence:
    include: [changed_diff, nearest_test_diff, "check:test"]
```

Path applicability can select a policy, but absence of a file in the diff does not prove no cross-cutting impact. Required checks established by the contract remain required even if a router recommends otherwise.

## Configuration ownership

Commit configuration and reviewed policy. Store mutable task state, budgets, logs, and provider payload metadata outside the checkout. Installation records its edits and the installed runtime version. Updating a check, policy, contract, runtime, or relevant environment invalidates affected evidence.

Unknown schema versions, missing required policies, duplicate check IDs, empty argv, invalid budgets, and unresolvable executable paths must fail validation. Schema and secret values must not be printed together in doctor output.

