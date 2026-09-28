# Initial publication and review plan

Approved 2026-09-28. This is an import of existing work, not four newly completed
product milestones. No feature PR is automatically merged or candidate promoted.

## Branch ownership

| Branch | Base | Owned paths |
|---|---|---|
| `main` | Initial commit | README.md, .gitignore |
| `codex/runtime-foundation` | main | src/, tests/, pyproject.toml, uv.lock, .python-version, checkpoint.example.json, scripts/measure_scenarios.py |
| `codex/architecture-docs` | runtime-foundation | docs root/index/status/product/research inputs; architecture/, adr/, research/, reference/, planning/, tasks/ |
| `codex/harness-integration` | architecture-docs | AGENTS.md, examples/, docs/guides/, docs/integrations/, docs/runbooks/ |
| `codex/validation-evidence` | harness-integration | Remaining Python verification scripts, docs/reports/, docs/handoffs/, docs/verification.md |

The complete checkout is the validation branch. Cross-links in earlier documentation
PRs can refer forward to later PRs; do not mistake their absence for deleted work.
Reporting/dashboard code stays with the runtime because the CLI, MCP and runtime
already depend on its shared types. The measurement helper is a dependency of a
runtime regression test and therefore belongs in the first PR.

## Review sequence and acceptance

1. **Runtime:** inspect contract authority, snapshot bindings, distinct result
   states, no implicit execution from completion, bounded provider behavior,
   loopback dashboard protections, package contents and offline tests.
2. **Architecture:** distinguish accepted ADRs from hypotheses and historical
   research; review privacy, unfinished authority design and the roadmap.
3. **Harness:** inspect pinned-N/candidate-N+1 separation, direct recovery,
   placeholder installation paths, disabled-by-default example provider, and
   explicit credential/payload approval. Confirm fresh-clone instructions do not
   claim the author's host installation exists on another machine.
4. **Validation:** review historical evidence against the stated version, fixture
   and limitations; inspect reproducible scripts and final publication handoff.
   Do not infer agent performance gains from passing tests or provider latency.

Run the README's lint/format/types/tests/build commands on the runtime branch and
the assembled tip. Record exact commits tested; untracked local files are not
proof of a branch's contents. The developer suite requires Git, Python 3.13, uv and
Node. Dependencies must be installed before the offline configured checks run.

For merging, work from PR 1 to PR 4. Prefer merge commits for this initial stack.
After each predecessor reaches main, retarget the next PR to main and review its
diff again. Squash/rebase merges need explicit stack reconciliation first. Do not
delete an upstream branch while a successor still targets it. No force push,
automatic merge, release or package publication is part of this task.

## Private/local boundary

The actual `.codex/config.toml`, `checkpoint.json`, credential files and two local
launchers remain ignored and untouched. Public templates contain no credentials
and do not replace the active installation. Local SQLite state, build outputs,
virtual environments and dependency directories are excluded. Historical docs
retain local evidence paths as provenance, not portable execution instructions.

The separate Project Garden website is outside this repository and is not silently
copied or published. Its reports are included; a redistributable fixture and CI
are future work. No hosted tracing or new model path is enabled by publication.

## Follow-up backlog

- [ ] Review and merge the four PRs in order.
- [ ] Establish independent CI and portable browser fixtures.
- [ ] Resolve authenticated evidence authority and coverage semantics.
- [ ] Measure full task overhead and quality on comparable baselines.
- [ ] Validate candidate promotion and rollback in isolation before host adoption.
- [ ] Verify Claude integration and native hooks as separate compatibility work.
