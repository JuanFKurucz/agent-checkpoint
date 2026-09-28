"""Credential-free, matched CLI workflow measurements; no model or agent simulation.

Run with a separately installed runtime using --python. All baseline repetitions
finish before any Checkpoint condition. Fixtures are retained outside the checkout.
The same acceptance argv is used in both conditions. This is not a causal coding
performance experiment: fixed order, tiny synthetic tasks, no independent agents.
"""

import argparse
import hashlib
import json
import os
import statistics
import subprocess
import tempfile
import time
from pathlib import Path

SCENARIOS = ("passing", "failure_repair", "stale_repair")
VERIFY = "from pathlib import Path\nassert Path('value.txt').read_text() == '2'\n"


def invoke(argv, cwd, attempts, expected):
    env = {
        k: v
        for k, v in os.environ.items()
        if k.upper() in {"PATH", "PATHEXT", "SYSTEMROOT", "WINDIR", "TEMP", "TMP", "LANG"}
    }
    start = time.perf_counter()
    result = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=60)
    record = {
        "argv": [str(arg) for arg in argv],
        "exit_code": result.returncode,
        "seconds": time.perf_counter() - start,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "expected_exit": expected,
    }
    attempts.append(record)
    if result.returncode != expected:
        raise RuntimeError(f"Unexpected exit {result.returncode}; expected {expected}")
    return result.stdout


def trial(python, base, condition, scenario, repetition):
    directory = base / f"{condition}-{scenario}-{repetition}"
    root = directory / "repo with spaces"
    root.mkdir(parents=True)
    subprocess.run(["git", "init", "--quiet", str(root)], check=True, capture_output=True)
    check = [str(python), "-I", "verify.py"]
    config = {
        "schemaVersion": 1,
        "checks": {"acceptance": {"argv": check, "required": True}},
    }
    (root / "checkpoint.json").write_text(json.dumps(config), encoding="utf-8")
    (root / "verify.py").write_text(VERIFY, encoding="utf-8")
    (root / "value.txt").write_text("1" if scenario == "failure_repair" else "2")
    request = directory / "request.txt"
    request.write_text("Make the synthetic value equal two.", encoding="utf-8")
    contract = directory / "contract.json"
    contract.write_text(
        json.dumps(
            {"criteria": [{"id": "value", "text": "Value is two", "check_ids": ["acceptance"]}]}
        ),
        encoding="utf-8",
    )
    record = {
        "condition": condition,
        "scenario": scenario,
        "repetition": repetition,
        "fixture": str(directory),
        "acceptance_argv": check,
        "verify_sha256": hashlib.sha256(VERIFY.encode()).hexdigest(),
        "attempts": [],
        "provider_requests": 0,
        "provider_retries": 0,
        "tokens": None,
        "billed_usd": None,
        "outcome": "incomplete",
    }
    attempts = record["attempts"]
    command = [
        str(python),
        "-I",
        "-m",
        "agent_checkpoint",
        "--root",
        str(root),
        "--state",
        str(directory / "state"),
    ]
    start = time.perf_counter()
    try:
        task = None
        if condition == "checkpoint":
            task = json.loads(
                invoke(
                    [
                        *command,
                        "task",
                        "start",
                        "--request-file",
                        str(request),
                        "--contract-file",
                        str(contract),
                        "--request-id",
                        "start",
                    ],
                    root,
                    attempts,
                    0,
                )
            )["task_id"]

        def report(status):
            if task:
                code = {"ready": 0, "needs_changes": 3, "unresolved": 4}[status]
                data = json.loads(
                    invoke([*command, "complete", "--task", task], root, attempts, code)
                )
                if data["status"] != status:
                    raise RuntimeError("Unexpected completion status")

        def run(number, passing):
            if task:
                invoke(
                    [
                        *command,
                        "check",
                        "run",
                        "--task",
                        task,
                        "--request-id",
                        f"check-{number}",
                        "acceptance",
                    ],
                    root,
                    attempts,
                    0 if passing else 3,
                )
            else:
                invoke(check, root, attempts, 0 if passing else 1)
            report("ready" if passing else "needs_changes")

        report("unresolved")
        run(1, scenario != "failure_repair")
        if scenario == "stale_repair":
            (root / "value.txt").write_text("1")
            report("unresolved")
            run(2, False)
        if scenario != "passing":
            (root / "value.txt").write_text("2")
            run(3 if scenario == "stale_repair" else 2, True)
        record["outcome"] = "pass"
    except Exception as exc:
        record["outcome"] = "error"
        record["error_type"] = type(exc).__name__
    record["workflow_seconds"] = time.perf_counter() - start
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repetitions", type=int, default=3)
    args = parser.parse_args()
    if not args.python.is_file() or not 1 <= args.repetitions <= 20:
        parser.error("Existing installed Python and 1..20 repetitions required")
    if args.output.exists():
        parser.error("Output exists; choose a new report path to preserve all attempts")
    base = Path(tempfile.mkdtemp(prefix="checkpoint-comparison-"))
    results = []
    data = {
        "schema_version": 1,
        "kind": "descriptive_fixed_order_workflow_microbenchmark",
        "fixture_root": str(base),
        "python": str(args.python.resolve()),
        "repetitions_per_condition_per_scenario": args.repetitions,
        "setup_time_included": False,
        "baseline_first": True,
        "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    for condition in ("baseline", "checkpoint"):
        for scenario in SCENARIOS:
            for repetition in range(1, args.repetitions + 1):
                record = trial(args.python.resolve(), base, condition, scenario, repetition)
                results.append(record)
                args.output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
                print(condition, scenario, repetition, record["outcome"], flush=True)
    data["summary"] = {}
    for scenario in SCENARIOS:
        medians = {
            condition: statistics.median(
                r["workflow_seconds"]
                for r in results
                if r["condition"] == condition and r["scenario"] == scenario
            )
            for condition in ("baseline", "checkpoint")
        }
        data["summary"][scenario] = {
            **medians,
            "overhead_seconds": medians["checkpoint"] - medians["baseline"],
        }
    args.output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return 0 if all(r["outcome"] == "pass" for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
