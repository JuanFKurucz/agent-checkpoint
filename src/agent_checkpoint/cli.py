"""Explicit CLI integration; stdout is JSON, errors never echo raw input."""

import argparse
import json
import os
import sys
from pathlib import Path
from uuid import uuid4

from agent_checkpoint.config import read_json
from agent_checkpoint.runtime import Runtime
from agent_checkpoint.snapshot import SnapshotError, worktree_identity
from agent_checkpoint.storage import StoreError


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="agent-checkpoint")
    result.add_argument("--root", type=Path, default=Path.cwd())
    result.add_argument("--config", type=Path)
    result.add_argument("--state", type=Path)
    commands = result.add_subparsers(dest="command", required=True)
    doctor = commands.add_parser("doctor")
    doctor.add_argument("--json", action="store_true")
    task = commands.add_parser("task").add_subparsers(dest="action", required=True)
    for action in ("start", "revise"):
        sub = task.add_parser(action)
        sub.add_argument("--contract-file", type=Path, required=True)
        sub.add_argument("--request-file", type=Path, required=action == "start")
        sub.add_argument("--request-id")
        if action == "revise":
            sub.add_argument("task_id")
            sub.add_argument("--expected-revision", type=int, required=True)
    task.add_parser("show").add_argument("task_id")
    check = commands.add_parser("check").add_subparsers(dest="action", required=True)
    run = check.add_parser("run")
    run.add_argument("--task", required=True)
    run.add_argument("--request-id", default=None)
    run.add_argument("--expected-snapshot-id")
    run.add_argument("check_ids", nargs="+")
    for name in ("route", "review", "complete"):
        sub = commands.add_parser(name)
        sub.add_argument("--task", required=True)
        sub.add_argument("--json", action="store_true")
        if name != "complete":
            sub.add_argument("--request-id")
        if name == "complete":
            sub.add_argument("--expected-snapshot-id")
        elif name == "route":
            sub.add_argument("--kind", choices=["skill"], default="skill")
            sub.add_argument("--phase", default="implementation")
            sub.add_argument("--allowed-candidate-ids", nargs="*")
        else:
            sub.add_argument("--criterion-ids", nargs="*")
            sub.add_argument("--evidence-ids", nargs="*", default=[])
    export = commands.add_parser("evidence").add_subparsers(dest="action", required=True)
    export_parser = export.add_parser("export")
    export_parser.add_argument("--task", required=True)
    export_parser.add_argument("--format", choices=["jsonl"], default="jsonl")
    commands.add_parser("mcp").add_argument("--stdio", action="store_true", required=True)
    report = commands.add_parser("report", help="Read historical metadata; never refresh readiness")
    report.add_argument("--task")
    report.add_argument("--limit", type=int, default=100)
    dashboard = commands.add_parser("dashboard", help="Serve a local read-only history viewer")
    dashboard.add_argument("--port", type=int, default=0)
    dashboard.add_argument(
        "--source-role",
        choices=["unknown", "pinned_supervisor", "candidate_fixture"],
        default="unknown",
    )
    dashboard.add_argument("--producer-version")
    return result


def status_code(result: dict[str, object]) -> int:
    status = result.get("status")
    if status in ("unresolved", "pending", "unavailable"):
        return 4
    if status == "needs_changes":
        return 3
    runs = result.get("runs")
    if isinstance(runs, list):
        states = [r.get("status") for r in runs if isinstance(r, dict)]
        if "fail" in states:
            return 3
        if "unknown" in states:
            return 4
    return 0


def dispatch(runtime: Runtime, args: argparse.Namespace) -> dict[str, object] | None:
    if args.command == "doctor":
        return {
            "schema_version": "1",
            "status": "available",
            "worktree_id": runtime.service.worktree_id,
            "policy_digest": runtime.service.policy_digest,
            "checks": list(runtime.config.checks),
            "hooks": "disabled",
            "execution_mode": "working_tree",
            "native_host_integration": "unverified",
            "provider": "jev_gateway_only",
            "remote_enabled": runtime.config.provider.enabled,
            "remote_allowed": runtime.config.provider.remote_allowed,
        }
    if args.command == "task":
        if args.action == "show":
            return runtime.service.task(args.task_id).model_dump(mode="json")
        data = read_json(args.contract_file)
        if args.request_file:
            if args.request_file.name.lower().startswith(".env"):
                raise ValueError("CREDENTIAL_FILE_DENIED")
            with args.request_file.open("r", encoding="utf-8") as handle:
                text = handle.read(16385)
            data["request"] = {"text": text}
        if args.action == "revise":
            previous = runtime.service.task(args.task_id)
            data.setdefault("request", {"text": previous.request})
            data.setdefault("scope", {"exclude": list(previous.scope_exclude)})
            data.update(task_id=args.task_id, expected_contract_revision=args.expected_revision)
        if args.request_id:
            data["request_id"] = args.request_id
        data.setdefault("request_id", str(uuid4()))
        return runtime.call("checkpoint_start_task", data)
    if args.command == "check":
        return runtime.call(
            "checkpoint_run_checks",
            {
                "task_id": args.task,
                "check_ids": args.check_ids,
                "request_id": args.request_id or str(uuid4()),
                "expected_snapshot_id": args.expected_snapshot_id,
            },
        )
    if args.command in ("route", "review", "complete"):
        data = {"task_id": args.task}
        if args.command == "complete":
            data["expected_snapshot_id"] = args.expected_snapshot_id
            return runtime.call("checkpoint_completion", data)
        data["request_id"] = args.request_id or str(uuid4())
        if args.command == "route":
            data.update(
                kind=args.kind, phase=args.phase, allowed_candidate_ids=args.allowed_candidate_ids
            )
        else:
            data.update(criterion_ids=args.criterion_ids, evidence_ids=args.evidence_ids)
        return runtime.call("checkpoint_" + args.command, data)
    if args.command == "evidence":
        runtime.service.task(args.task)
        for kind in ("check", "route", "review", "decision", "completion"):
            for event in runtime.service.store.events(args.task, runtime.service.worktree_id, kind):
                print(json.dumps({"kind": kind, "event": event}, ensure_ascii=True))
        return None
    if args.command == "mcp":
        from agent_checkpoint.mcp_server import serve

        serve(runtime)
        return None
    raise ValueError("UNSUPPORTED_COMMAND")


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        root = args.root.resolve()
        config_path = args.config or root / "checkpoint.json"
        state = args.state or Path(os.environ.get("LOCALAPPDATA", str(Path.home() / ".local"))) / (
            "agent-checkpoint"
        ) / worktree_identity(root)
        if args.command == "dashboard":
            from agent_checkpoint.dashboard import serve_dashboard

            serve_dashboard(
                state,
                worktree_identity(root),
                port=args.port,
                source_role=args.source_role,
                producer_version=args.producer_version,
            )
            return 0
        if args.command == "report":
            # Bypass Runtime/Store construction: never create or migrate state for a report.
            from agent_checkpoint.reporting import read_report

            print(
                json.dumps(
                    read_report(state, worktree_identity(root), args.task, limit=args.limit),
                    ensure_ascii=True,
                )
            )
            return 0
        runtime = Runtime(
            root, config_path, state, transport="mcp" if args.command == "mcp" else "cli"
        )
        output = dispatch(runtime, args)
        if output is not None:
            print(json.dumps(output, ensure_ascii=True))
            return status_code(output)
        return 0
    except (StoreError, SnapshotError) as exc:
        print(
            json.dumps({"status": "error", "code": str(exc)}),
            file=sys.stderr if args.command == "mcp" else sys.stdout,
        )
        return 5
    except (ValueError, OSError):
        print(
            json.dumps({"status": "error", "code": "INVALID_INPUT_OR_CONFIG"}),
            file=sys.stderr if args.command == "mcp" else sys.stdout,
        )
        return 2
    except KeyboardInterrupt:
        print(
            json.dumps({"status": "error", "code": "INTERRUPTED"}),
            file=sys.stderr if args.command == "mcp" else sys.stdout,
        )
        return 5


if __name__ == "__main__":
    raise SystemExit(main())
