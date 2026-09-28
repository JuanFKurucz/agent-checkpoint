"""Independent local promotion/rollback drill; never changes the active launcher.

Uses only the standard library and direct commands, not Checkpoint readiness, as
the promotion gate. Keeps extracted source, copied state and every command result.
The local pointer belongs to the drill only: this is not an installed host hook.
"""

import argparse
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import tarfile
import time
import zipfile
from pathlib import Path


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def copy_state(source, destination):
    destination.mkdir()
    with sqlite3.connect((source / "checkpoint.sqlite3").as_uri() + "?mode=ro", uri=True) as src:
        with sqlite3.connect(destination / "checkpoint.sqlite3") as dst:
            src.backup(dst)
            assert dst.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
            events = dst.execute("SELECT payload FROM events").fetchall()
            tasks = dst.execute(
                "SELECT DISTINCT task_id FROM contracts ORDER BY task_id"
            ).fetchall()
    blobs = destination / "blobs"
    blobs.mkdir()
    # Copy exactly the output blobs referenced by the consistent SQLite snapshot.
    ids = {json.loads(row[0]).get("output_digest") for row in events} - {None, ""}
    for blob_id in ids:
        if len(blob_id) != 64 or any(c not in "0123456789abcdef" for c in blob_id):
            raise ValueError("Invalid blob identity")
        path = source / "blobs" / blob_id
        if path.is_symlink() or path.stat().st_size > 1048576 or sha(path) != blob_id:
            raise ValueError("Invalid source blob")
        shutil.copyfile(path, blobs / blob_id)
        assert sha(blobs / blob_id) == blob_id
    return {"tasks": [row[0] for row in tasks], "events": len(events), "blobs": len(ids)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("candidate", "baseline", "active-state", "root", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--wheel-sha256", required=True)
    parser.add_argument("--source-sha256", required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        parser.error("Use a new output directory; prior evidence is never overwritten")
    if output.is_relative_to(args.active_state.resolve()) or output.is_relative_to(
        args.root.resolve()
    ):
        parser.error("Drill output must be outside active state and evaluated checkout")
    output.mkdir(parents=True)
    records = []
    report = {
        "schema_version": 1,
        "status": "incomplete",
        "commands": records,
        "active_state_modified": False,
        "real_launcher_modified": False,
        "promotion_gate": "independent direct checks and installed-file hashes",
        "candidate_ready_used_as_gate": False,
    }
    report_path = output / "report.json"

    def save():
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    def run(argv, cwd, expected=0):
        start = time.perf_counter()
        env = {
            k: v
            for k, v in os.environ.items()
            if k.upper()
            in {
                "PATH",
                "PATHEXT",
                "SYSTEMROOT",
                "WINDIR",
                "TEMP",
                "TMP",
                "LOCALAPPDATA",
                "APPDATA",
                "USERPROFILE",
                "LANG",
                "UV_CACHE_DIR",
            }
        }
        result = subprocess.run(
            [str(a) for a in argv], cwd=cwd, env=env, capture_output=True, text=True, timeout=600
        )
        records.append(
            {
                "argv": [str(a) for a in argv],
                "cwd": str(cwd),
                "exit_code": result.returncode,
                "expected_exit": expected,
                "seconds": time.perf_counter() - start,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        )
        save()
        print(Path(str(argv[0])).name, "exit", result.returncode, flush=True)
        if result.returncode != expected:
            raise RuntimeError("Independent command gate failed")
        return result.stdout

    try:
        wheels = list(args.candidate.glob("*.whl"))
        archives = list(args.candidate.glob("*.tar.gz"))
        assert len(wheels) == len(archives) == 1
        wheel, archive = wheels[0], archives[0]
        assert sha(wheel) == args.wheel_sha256
        assert sha(archive) == args.source_sha256
        report.update(wheel_sha256=sha(wheel), source_sha256=sha(archive))
        extracted = output / "source"
        extracted.mkdir()
        with tarfile.open(archive) as package:
            for entry in package.getmembers():
                target = (extracted / entry.name).resolve()
                if not target.is_relative_to(extracted) or not (entry.isfile() or entry.isdir()):
                    raise ValueError("Unsafe archive entry")
                if any(part == ".env" or part.startswith(".env.") for part in target.parts):
                    raise ValueError("Credential archive entry denied")
            package.extractall(extracted, filter="data")
        roots = list(extracted.iterdir())
        assert len(roots) == 1 and roots[0].is_dir()
        source = roots[0]
        report["isolated_source"] = str(source)
        run(["git", "init", "--quiet", source], output)
        run(["uv", "sync", "--locked", "--offline", "--extra", "jev"], source)
        direct = ["uv", "run", "--locked", "--offline", "--extra", "jev"]
        for check in (
            ["ruff", "check", "src", "tests", "scripts"],
            ["ruff", "format", "--check", "src", "tests", "scripts"],
            ["mypy"],
            ["pytest", "-q"],
        ):
            run([*direct, *check], source)
        candidate_python = args.candidate / "venv" / "Scripts" / "python.exe"
        baseline_python = args.baseline / "venv" / "Scripts" / "python.exe"
        purelib = Path(
            run(
                [
                    candidate_python,
                    "-I",
                    "-c",
                    "import sysconfig; print(sysconfig.get_path('purelib'))",
                ],
                output,
            ).strip()
        )
        installed_files = 0
        with zipfile.ZipFile(wheel) as package:
            for name in package.namelist():
                if name.startswith("agent_checkpoint/") and name.endswith(".py"):
                    assert (purelib / name).read_bytes() == package.read(name)
                    installed_files += 1
        report["installed_python_files_verified"] = installed_files
        backup = output / "backup-state"
        report["state_backup"] = copy_state(args.active_state.resolve(), backup)
        candidate_state = output / "candidate-state"
        copy_state(backup, candidate_state)
        task_id = report["state_backup"]["tasks"][0]
        pointer = output / "launcher.json"

        def select(python, state):
            temp = output / "launcher.next.json"
            temp.write_text(
                json.dumps(
                    {
                        "python": str(python) if python else None,
                        "state": str(state) if state else None,
                    }
                ),
                encoding="utf-8",
            )
            os.replace(temp, pointer)

        def show(expected=0):
            launch = json.loads(pointer.read_text())
            return run(
                [
                    launch["python"],
                    "-I",
                    "-m",
                    "agent_checkpoint",
                    "--root",
                    args.root,
                    "--state",
                    launch["state"],
                    "task",
                    "show",
                    task_id,
                ],
                output,
                expected,
            )

        select(baseline_python, backup)
        baseline_contract = json.loads(show())
        # This switch occurs only AFTER independent direct checks and wheel verification.
        select(candidate_python, candidate_state)
        assert json.loads(show()) == baseline_contract
        report["promotion"] = "candidate selected; copied contract preserved"
        broken = output / "broken-state"
        broken.mkdir()
        (broken / "checkpoint.sqlite3").write_bytes(b"synthetic corrupt database")
        select(candidate_python, broken)
        failure = json.loads(show(expected=5))
        report["failure_injection"] = failure
        # Manual escape does not depend on Checkpoint starting or accepting a verdict.
        select(None, None)
        assert json.loads(pointer.read_text())["python"] is None
        run([*direct, "pytest", "-q", "tests/test_contracts.py", "tests/test_service.py"], source)
        report["manual_disable"] = "drill launcher disabled; direct command passed"
        restored = output / "rollback-state"
        copy_state(backup, restored)
        select(baseline_python, restored)
        assert json.loads(show()) == baseline_contract
        report["rollback"] = "baseline artifact and backup-derived state restored"
        report["status"] = "pass"
    except Exception as exc:
        report["status"] = "failed"
        report["error_type"] = type(exc).__name__
        raise
    finally:
        save()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
