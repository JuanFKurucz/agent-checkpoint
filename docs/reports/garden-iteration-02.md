# Iteration 2 — appearance preferences and read-only reports

Status: verified; 134 tests in 135.97 s, native lint/format/types pass and completion
ready. Installed six-tool MCP exchange passed in 8.036267 s; 15 runtime files matched
source. External garden-lab/candidate-iteration-2/validation.json contains final
evidence and artifact hashes. The installed candidate report read real pinned website
history in 0.808714 s without credentials or provider calls. Not promoted.

## Paired work

Website: system/daylight/after-dusk preference with safe independent persistence;
system setting responds live to browser color-scheme changes. Reduced-motion disables
transitions. Recovery/card behavior remains intact. Two new cases first failed for
missing preference exports; all nine model tests then passed.

Tool: metadata-only CLI/MCP history reporting. In iteration 1, diagnosis required
manually joining calls and raw records, and a completion result could be overread.
The report now gathers scoped history without executing anything. It deduplicates
Jev usage and exposes unknown/truncated/corrupt data. It does not improve check coverage
or freshness, and it is not a new completion authority.

## Verification and observed usefulness

Reporting tests first failed at import because no report capability existed.
Fourteen projection/security/bounds tests plus runtime nonexecution/CLI recovery
checks and actual MCP exchange pass: focused suite 38 tests in 38.44 s.
Read-only tests compare logical database dumps; forbidden-call sentinels guard
checks, completion, event writes, provider calls and config verification. Missing
state stays missing. Foreign tasks are not returned; corrupted records are flagged.

Candidate CLI read of real pinned website history returned two route/decision events
as **one** observed Jev request, task reservation 1, 388 input/41 output tokens and
unknown dollars. End-to-end `uv run ... report` elapsed 1.646799 s in one observation
(before candidate version bump). It supplied task list and decision history in one
call. No general latency/cost or coding-quality improvement is established.

Browser verified dark selection survives reload, system changes live dark→light,
reduced-motion yields transitionDuration=0s, and mobile has no horizontal overflow.
Desktop and mobile screenshots retained outside checkout. This is visual/manual
verification, not a complete accessibility or automated browser regression suite.

## Identities and measurements

Repository task 6f7bb5a3b75f7e24c0fd0afc2bd801a0. Website task
809c7c3777cdec26924d292efe0e1759. Website check IDs:
e6b92900-1ef0-4ca3-9f8c-c0480b8fd3bd (unit),
4f0010c5-9ec3-4664-b70f-a72aade8526d (syntax).
Pinned website checks 3.294648 s, completion 2.765620 s: ready for declared evidence.
Direct nine-test command 0.311551 s. Website red→green implementation envelope
~31.0 s including reasoning/tool latency; browser validation measured separately only
as individual observations, not one continuous timed phase.

Jev repository route e9b29dd3-f246-4b4d-8163-7efbf3fe7305: documentation,
406/39 tokens, 1.091926 s, confidence 0.33. Website route
890bda74-394d-4581-98e2-79cd615d0d43: frontend-design, 388/41 tokens,
0.689792 s, confidence 0.53. One physical call per task, no retry/review/fallback;
all billing unknown. Skills already applied independently; no additional routing
decision value established. Report reads made zero new provider requests.

Candidate becomes 0.1.5, six tools. Active 0.1.2 remains five tools and unchanged.
The observability skill guided bounded metadata and honest metrics; testing skill
guided isolated negative fixtures; frontend/browser skills guided visual validation.

## Next paired proposal

Website iteration 3: deletion with undo (fixed shuffled order).
Tool: local visual dashboard and timestamped candidate operation traces, using the
new report boundary. Show polling/last-good freshness and a decision map with Mermaid
source; defend loopback API access, prevent raw payload exports, retain unknown legacy
timestamps and avoid automatic checks. Report-only interaction cannot replace visual
or missing functional tests; verify those independently.
