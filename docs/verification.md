# Direct verification inventory

Status: internal MVP 0.1.1 verified on Windows/CPython 3.13.11. See the
[requirement audit](reports/mvp-completion-audit.md) and
[operating report](reports/mvp-validation-report.md) for scope and exact artifacts.

Direct verification remains runnable without a running Agent Checkpoint service,
active database, Jev credentials, MCP connection, or hooks. Run from the repository
root after `uv sync --locked --extra jev`; all exact dependencies are in uv.lock.

| Direct command | Observed result on 2026-09-27 |
|---|---|
| `uv run --locked --extra jev ruff check src tests scripts` | Pass |
| `uv run --locked --extra jev ruff format --check src tests scripts` | Pass, 27 files |
| `uv run --locked --extra jev mypy` | Pass, 13 source files |
| `uv run --locked --extra jev pytest -q` | Current source: 89 passed in 127.00 s; frozen extracted source: 89 passed in 137.92 s |
| `uv build --no-sources` | Wheel and source distribution built |

Tests create disposable repositories and state; sockets are disabled by default.
Build artifacts contain the CLI and five-tool MCP runtime. Independently installed
N has wheel SHA-256
`83114bf8ca716c0183d31667fa9e3c6b4184e9c50ea6dffbdce72e8d40087637` and was used
unchanged for shadow plus two real follow-up tasks. Current source contains those
follow-up fixes. Candidate 0.1.1 was selected and rolled back only in a disposable
promotion drill; active N stayed unchanged. The clean candidate passed all 18
workflow trials and an installed all-five-tool MCP exchange. See the
[report](reports/mvp-validation-report.md) for identities and limitations.

Separate gateway example: `npm run typecheck` in examples/vercel-gateway passes.
After local key entry, `npm start` exited 0 and returned nonempty GPT-5.5 text
(Lanternleaf Day, 2026-09-27, 6.60-second observed command wall time). The initial
missing-key attempt is retained as a failed preflight, not counted as generation.
The user then restricted model usage to Jev through Vercel Gateway. The example was
changed to `experimental_evaluate` with an explicit Gateway provider. `npm run
typecheck` passed and one synthetic `npm start` returned testing, 350 input / 38
output tokens, 692 ms evaluation time, exit 0. Requested/reported alias was
typesafe-ai/jev; an exact weights/version pin is unverified. No more GPT calls are
authorized. [Sanitized smoke record](reports/gateway-smoke-2026-09-27.json).

The Python gateway adapter's 14 offline tests pass; its live compatibility remains
unverified. Seven concurrency fixtures pass. The new CLI lifecycle and real MCP
stdio exchange pass, and installed CLI self-use is recorded. A corrupt-state
promotion/rollback drill and 24 direct recovery tests passed. See the machine-readable
[promotion record](reports/promotion-drill-2026-09-27.json).

| Surface | Current state | Future registration requirement |
|---|---|---|
| Documentation | Local links, fences, JSON examples and consistency can be inspected directly; no committed validator command | Record the exact repeatable command before advertising it as a repository script |
| Types/package/build for selected language | Clean wheel installed; source/archive/installed code matches | Broader distribution remains unverified |
| Unit/schema tests | Authority/readiness, scope, revision, concurrency, CLI/MCP and gateway fixtures pass | Broader proposed policy surfaces remain future work |
| Runner/storage integration | Working-tree runner, SQLite/blobs, copied-state recovery pass | Runtime isolated_snapshot mode remains unavailable |
| Host adapter contracts | CLI self-use and installed MCP exchange pass; native Codex config parses | Native MCP invocation remains unverified |
| CI/release verification | Unavailable | Trusted definitions, candidate identity, independently produced evidence |

For each future entry record command/argv, working directory, purpose, required inputs/environment profile, expected output/exit meaning, validation date, and evidence location. Do not store credentials or pre-populate passing results.

The first implementation package should validate scripts directly before adding them to active agent instructions. A failed product runtime must not remove access to these commands.

