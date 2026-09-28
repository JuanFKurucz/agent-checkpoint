"""Approved argv execution with bounded capture and process-tree lifetime.

The launcher waits for parent setup before executing repository code. On Windows
it is assigned to a kill-on-close Job Object first; descendants cannot outlive
the check. This is lifetime control, not filesystem or network sandboxing.
"""

import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from pydantic import Field

from agent_checkpoint.contracts import ContextFingerprints, Record
from agent_checkpoint.snapshot import Snapshot, SnapshotError, capture, credential_name, stamp
from agent_checkpoint.storage import digest

_LAUNCH = (
    "import json,subprocess,sys; c=json.loads(sys.stdin.readline()); "
    "raise SystemExit(subprocess.call(c['argv'], cwd=c['cwd'], stdin=subprocess.DEVNULL))"
)
_OS_ENV = ("SYSTEMROOT", "WINDIR", "COMSPEC", "TEMP", "TMP", "PATH", "PATHEXT", "LANG")


class CheckDefinition(Record):
    argv: tuple[str, ...] = Field(min_length=1)
    cwd: str = "."
    timeout_seconds: float = Field(default=120, gt=0, le=3600)
    max_output_bytes: int = Field(default=32768, ge=1, le=1_048_576)
    env_allow: tuple[str, ...] = ()
    execution_mode: Literal["working_tree", "isolated_snapshot"] = "working_tree"


@dataclass(frozen=True)
class CheckResult:
    status: Literal["pass", "fail", "unknown"]
    exit_code: int | None
    output: bytes
    reason: str
    before: Snapshot
    after: Snapshot | None
    definition_digest: str
    duration_seconds: float
    execution_mode: str
    context_fingerprints: ContextFingerprints | None = None


def check_environment(definition: CheckDefinition) -> dict[str, str]:
    if any(
        re.search("KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL", k, re.I) for k in definition.env_allow
    ):
        raise ValueError("SECRET_ENVIRONMENT_DENIED")
    allowed = {k.upper() for k in (*_OS_ENV, *definition.env_allow)}
    result = {k: v for k, v in os.environ.items() if k.upper() in allowed}
    result.update(PYTHONDONTWRITEBYTECODE="1", PYTHONUNBUFFERED="1")
    return result


class ProcessTree:
    def __init__(self, process: subprocess.Popen[bytes]) -> None:
        self.process = process
        self.close_job: Callable[[], None] = lambda: None
        if sys.platform == "win32":
            import win32api  # type: ignore[import-untyped]
            import win32job  # type: ignore[import-untyped]

            job = win32job.CreateJobObject(None, "")
            try:
                info = win32job.QueryInformationJobObject(
                    job, win32job.JobObjectExtendedLimitInformation
                )
                info["BasicLimitInformation"]["LimitFlags"] = (
                    win32job.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
                )
                win32job.SetInformationJobObject(
                    job, win32job.JobObjectExtendedLimitInformation, info
                )
                handle = win32api.OpenProcess(0x0100 | 0x0001 | 0x0400, False, process.pid)
                try:
                    win32job.AssignProcessToJobObject(job, handle)
                finally:
                    win32api.CloseHandle(handle)
            except BaseException:
                win32api.CloseHandle(job)
                process.kill()
                process.wait()
                raise
            self.close_job = lambda: win32api.CloseHandle(job)

    def close(self) -> None:
        if sys.platform == "win32":
            self.close_job()
        else:
            try:
                os.killpg(self.process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        self.process.wait(timeout=10)


def resolve_executable(definition: CheckDefinition, root: Path) -> str | None:
    command = definition.argv[0]
    # Relative executable paths are relative to the check, not the host process.
    if "/" in command or "\\" in command:
        command = str((root / definition.cwd / command).resolve())
    return shutil.which(command, path=check_environment(definition).get("PATH"))


def executable_identity(executable: str | None) -> dict[str, object] | None:
    if executable is None:
        return None
    path = Path(executable).resolve()
    if credential_name(path.name):
        raise SnapshotError("CREDENTIAL_EXECUTABLE_DENIED")
    try:
        before = path.stat()
        limit = 256 * 1024 * 1024
        if not path.is_file() or before.st_size > limit:
            raise SnapshotError("EXECUTABLE_IDENTITY_UNAVAILABLE")
        content = hashlib.sha256()
        size = 0
        with path.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                size += len(chunk)
                if size > limit:
                    raise SnapshotError("EXECUTABLE_IDENTITY_UNAVAILABLE")
                content.update(chunk)
        if stamp(before) != stamp(path.stat()):
            raise SnapshotError("EXECUTABLE_CHANGED_DURING_SNAPSHOT")
        return {"path": str(path), "sha256": content.hexdigest(), "generation": stamp(before)}
    except OSError as exc:
        raise SnapshotError("EXECUTABLE_IDENTITY_UNAVAILABLE") from exc


def check_context(definition: CheckDefinition, root: Path | None = None) -> dict[str, object]:
    return {
        "definition": digest(definition.model_dump()),
        "environment": digest(check_environment(definition)),
        "runtime": sys.version,
        "executable": executable_identity(resolve_executable(definition, root or Path.cwd())),
        "launcher": executable_identity(sys.executable),
    }


def context_fingerprints(context: dict[str, object]) -> ContextFingerprints | None:
    """Fixed component digests only; never retain paths or environment values."""
    # Unknown/partial context layouts cannot support a complete comparison. The
    # snapshot still uses the entire context and determines freshness unchanged.
    if set(context) != set(ContextFingerprints.model_fields):
        return None
    return ContextFingerprints.model_validate(
        {key: digest(context[key]) for key in ContextFingerprints.model_fields}
    )


def run_check(root: Path, definition: CheckDefinition) -> CheckResult:
    started = time.monotonic()
    root = root.resolve()
    cwd = (root / definition.cwd).resolve()
    if not cwd.is_relative_to(root):
        raise ValueError("CWD_OUTSIDE_WORKSPACE")
    env = check_environment(definition)
    definition_hash = digest(definition.model_dump())
    context = check_context(definition, root)
    before = capture(root, context=context)

    def result(
        status: Literal["pass", "fail", "unknown"],
        reason: str,
        code: int | None = None,
        output: bytes = b"",
        after: Snapshot | None = None,
    ) -> CheckResult:
        return CheckResult(
            status,
            code,
            output,
            reason,
            before,
            after,
            definition_hash,
            time.monotonic() - started,
            definition.execution_mode,
            context_fingerprints(context),
        )

    if definition.execution_mode != "working_tree":
        # Explicit until a controlled materialization implementation is validated.
        return result("unknown", "ISOLATION_UNAVAILABLE")
    executable = resolve_executable(definition, root)
    if executable is None:
        return result("unknown", "EXECUTABLE_UNAVAILABLE")
    if Path(executable).suffix.lower() in (".bat", ".cmd"):
        return result("unknown", "SHELL_WRAPPER_UNSUPPORTED")
    argv = [str(Path(executable).resolve()), *definition.argv[1:]]
    output = bytearray()
    overflow = threading.Event()
    process: subprocess.Popen[bytes] | None = None
    tree: ProcessTree | None = None
    reader: threading.Thread | None = None
    reason = ""
    code: int | None = None
    try:
        process = subprocess.Popen(
            [sys.executable, "-I", "-c", _LAUNCH],
            cwd=cwd,
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            start_new_session=os.name != "nt",
        )
        tree = ProcessTree(process)
        assert process.stdout is not None and process.stdin is not None
        pipe = process.stdout

        def drain() -> None:
            while chunk := pipe.read(4096):
                room = definition.max_output_bytes - len(output)
                output.extend(chunk[:room])
                if len(chunk) > room:
                    overflow.set()

        reader = threading.Thread(target=drain, daemon=True)
        reader.start()
        process.stdin.write((json.dumps({"argv": argv, "cwd": str(cwd)}) + "\n").encode())
        process.stdin.close()
        deadline = time.monotonic() + definition.timeout_seconds
        while process.poll() is None:
            if overflow.wait(min(0.01, max(0, deadline - time.monotonic()))):
                reason = "OUTPUT_LIMIT"
                break
            if time.monotonic() >= deadline:
                reason = "TIMEOUT"
                break
        code = process.poll()
    except (OSError, subprocess.SubprocessError):
        reason = "EXECUTION_UNAVAILABLE"
    finally:
        if tree is not None:
            tree.close()
        elif process is not None and process.poll() is None:
            process.kill()
            process.wait()
        if reader is not None:
            reader.join(timeout=5)
            if reader.is_alive():
                reason = "OUTPUT_CAPTURE_INCOMPLETE"
        if process is not None:
            if process.stdout is not None:
                process.stdout.close()
            if process.stdin is not None and not process.stdin.closed:
                process.stdin.close()
    if overflow.is_set():
        reason = "OUTPUT_LIMIT"
    try:
        after = capture(root, context=check_context(definition, root))
    except SnapshotError:
        return result("unknown", "SNAPSHOT_UNAVAILABLE", code, bytes(output))
    if not reason and (before.id != after.id or before.generation != after.generation):
        reason = "INPUT_CHANGED"
    if reason or code is None:
        return result("unknown", reason or "INTERRUPTED", code, bytes(output), after)
    return result("pass" if code == 0 else "fail", "", code, bytes(output), after)
