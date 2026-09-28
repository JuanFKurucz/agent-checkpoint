"""Controlled installed-runtime replay; synthetic state only, no provider requests."""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from agent_checkpoint import __version__
from agent_checkpoint.runtime import Runtime


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Choose a fresh evidence path")
    base = Path(tempfile.mkdtemp(prefix="checkpoint-context-probe-"))
    root = base / "repo"
    root.mkdir()
    subprocess.run(["git", "init", "--quiet", str(root)], check=True, capture_output=True)
    (root / "check.py").write_text("assert True\n", encoding="utf-8")
    config = root / "checkpoint.json"
    config.write_text(
        json.dumps({"checks": {"unit": {"argv": [sys.executable, "check.py"], "required": True}}}),
        encoding="utf-8",
    )
    record = {
        "version": __version__,
        "fixture": str(base),
        "python": sys.executable,
        "provider_requests": 0,
        "status": "incomplete",
    }
    original_lang = os.environ.get("LANG")
    started = time.perf_counter()
    try:
        os.environ["LANG"] = "synthetic-context-a"
        runtime = Runtime(root, config, base / "state")
        task = runtime.call(
            "checkpoint_start_task",
            {
                "request_id": "start",
                "request": {"text": "Synthetic context diagnostic replay"},
                "criteria": [{"id": "a", "text": "Unit verification", "check_ids": ["unit"]}],
            },
        )["task_id"]
        record["task_id"] = task
        runtime.call(
            "checkpoint_run_checks",
            {
                "task_id": task,
                "check_ids": ["unit"],
                "request_id": "check",
            },
        )
        baseline = runtime.call("checkpoint_completion", {"task_id": task})
        assert baseline["status"] == "ready"
        os.environ["LANG"] = "synthetic-context-b"
        changed = runtime.call("checkpoint_completion", {"task_id": task})
        assert changed["status"] == "unresolved"
        assert changed["next_actions"][0]["reason_code"] == "EVIDENCE_STALE"
        record["baseline"] = baseline
        record["changed"] = changed
        record["check_events"] = len(
            runtime.service.store.events(task, runtime.service.worktree_id, "check")
        )
        assert record["check_events"] == 2  # start/finish; complete did not rerun.
        record["status"] = "pass"
    finally:
        if original_lang is None:
            os.environ.pop("LANG", None)
        else:
            os.environ["LANG"] = original_lang
        record["seconds"] = time.perf_counter() - started
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: record[k] for k in ("version", "status", "seconds", "fixture")}))


if __name__ == "__main__":
    main()
