"""Read-only report comparison over synthetic completed, unmatched and duplicate starts."""

import argparse
import json
import subprocess
import tempfile
import time
from pathlib import Path

from agent_checkpoint import __version__
from agent_checkpoint.contracts import Contract, Criterion
from agent_checkpoint.reporting import read_report
from agent_checkpoint.snapshot import worktree_identity
from agent_checkpoint.storage import Store


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Choose a fresh output path")
    base = Path(tempfile.mkdtemp(prefix="checkpoint-pairing-probe-"))
    root = base / "repo"
    root.mkdir()
    subprocess.run(["git", "init", "--quiet", str(root)], check=True, capture_output=True)
    identity = worktree_identity(root)
    store = Store(base / "state")
    store.save_contract(
        Contract(
            task_id="pairing-probe",
            worktree_id=identity,
            request="Synthetic history, no real executions",
            criteria=(Criterion(id="a", text="Fixture only"),),
        ),
        "start",
    )
    for run, phases in [
        ("completed", ["started", "finished"]),
        ("unmatched", ["started"]),
        ("duplicate", ["started", "started", "finished"]),
    ]:
        for phase in phases:
            store.append_event(
                "pairing-probe",
                identity,
                "check",
                {
                    "run_id": run,
                    "check_id": "synthetic",
                    "contract_revision": 1,
                    "phase": phase,
                    "status": "unknown" if phase == "started" else "pass",
                    "reason": "INTERRUPTED_OR_RUNNING" if phase == "started" else "",
                    "duration_seconds": 0,
                },
            )
    with store.connection() as db:
        before = list(db.iterdump())
    started = time.perf_counter()
    report = read_report(store.state, identity, "pairing-probe")
    seconds = time.perf_counter() - started
    with store.connection() as db:
        assert before == list(db.iterdump())
    assert report["readiness"] == "not_revalidated"
    record = {
        "version": __version__,
        "fixture": str(base),
        "report": report,
        "read_seconds": seconds,
        "database_unchanged": True,
        "provider_requests": 0,
        "real_check_executions": 0,
        "status": "pass",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: record[k] for k in ("version", "fixture", "read_seconds", "status")}))


if __name__ == "__main__":
    main()
