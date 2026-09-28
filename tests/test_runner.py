import ctypes
import subprocess
import sys
from ctypes import wintypes
from pathlib import Path

import pytest

from agent_checkpoint.runner import CheckDefinition, check_context, run_check


def test_context_fingerprints_reject_partial_or_extended_layouts():
    from agent_checkpoint.runner import context_fingerprints

    assert context_fingerprints({"external_executable_generation": 1}) is None
    standard = {
        key: "synthetic"
        for key in ("definition", "environment", "runtime", "executable", "launcher")
    }
    assert context_fingerprints(standard) is not None
    assert context_fingerprints({**standard, "unknown_component": "private"}) is None


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    root = tmp_path / "run with spaces"
    root.mkdir()
    subprocess.run(["git", "init", "--quiet", str(root)], check=True)
    (root / "input.txt").write_text("original", encoding="utf-8")
    return root


def test_run_records_success_and_bounded_output(repo: Path) -> None:
    result = run_check(repo, CheckDefinition(argv=(sys.executable, "-c", "print('observed')")))
    assert result.status == "pass"
    assert result.exit_code == 0
    assert result.output.strip() == b"observed"
    assert result.execution_mode == "working_tree"


def test_nonzero_exit_is_a_failure(repo: Path) -> None:
    result = run_check(repo, CheckDefinition(argv=(sys.executable, "-c", "raise SystemExit(7)")))
    assert result.status == "fail"
    assert result.exit_code == 7


def test_mutation_during_execution_is_not_current_pass(repo: Path) -> None:
    code = "from pathlib import Path; Path('input.txt').write_text('changed')"
    result = run_check(repo, CheckDefinition(argv=(sys.executable, "-c", code)))
    assert result.status == "unknown"
    assert result.reason == "INPUT_CHANGED"


def test_edit_revert_is_uncertain_even_with_identical_content(repo: Path) -> None:
    code = (
        "from pathlib import Path; p=Path('input.txt'); "
        "p.write_text('changed'); p.write_text('original')"
    )
    result = run_check(repo, CheckDefinition(argv=(sys.executable, "-c", code)))
    assert result.status == "unknown"


def test_provider_credentials_not_in_child_environment(repo: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("TYPESAFE_API_KEY", "synthetic-do-not-inherit")
    code = "import os; assert 'TYPESAFE_API_KEY' not in os.environ"
    result = run_check(repo, CheckDefinition(argv=(sys.executable, "-c", code)))
    assert result.status == "pass"


def test_output_limit_and_timeout_are_not_success(repo: Path) -> None:
    flood = CheckDefinition(argv=(sys.executable, "-c", "print('x'*100000)"), max_output_bytes=100)
    result = run_check(repo, flood)
    assert result.status == "unknown"
    assert result.reason == "OUTPUT_LIMIT"
    assert len(result.output) <= 100
    timeout = CheckDefinition(
        argv=(sys.executable, "-c", "import time; time.sleep(30)"), timeout_seconds=0.2
    )
    result = run_check(repo, timeout)
    assert result.status == "unknown"
    assert result.reason == "TIMEOUT"


def test_missing_executable_and_escaping_cwd_are_rejected(repo: Path) -> None:
    missing = run_check(repo, CheckDefinition(argv=("missing-checkpoint-executable-12345",)))
    assert missing.status == "unknown"
    assert missing.reason == "EXECUTABLE_UNAVAILABLE"
    with pytest.raises(ValueError, match="CWD_OUTSIDE_WORKSPACE"):
        run_check(repo, CheckDefinition(argv=(sys.executable,), cwd=".."))


@pytest.mark.skipif(sys.platform != "win32", reason="Windows Job Object fixture")
@pytest.mark.parametrize("parent_waits", [False, True])
def test_descendants_die_on_parent_exit_or_timeout(repo: Path, parent_waits: bool) -> None:
    code = (
        "import subprocess,sys,time; "
        "p=subprocess.Popen([sys.executable,'-c','import time; time.sleep(60)']); "
        "print(p.pid,flush=True); " + ("time.sleep(60)" if parent_waits else "")
    )
    result = run_check(repo, CheckDefinition(argv=(sys.executable, "-c", code), timeout_seconds=1))
    pid = int(result.output.strip())
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    handle = kernel.OpenProcess(0x00100000, False, pid)
    if handle:
        try:
            assert kernel.WaitForSingleObject(handle, 1000) == 0
        finally:
            kernel.CloseHandle(handle)
    assert result.reason == ("TIMEOUT" if parent_waits else "")


def test_required_isolation_never_falls_back(repo: Path) -> None:
    result = run_check(
        repo,
        CheckDefinition(
            argv=(sys.executable, "-c", "print('unsafe fallback')"),
            execution_mode="isolated_snapshot",
        ),
    )
    assert result.status == "unknown"
    assert result.reason == "ISOLATION_UNAVAILABLE"
    assert result.output == b""


def test_context_tracks_external_executable_content(tmp_path: Path) -> None:
    executable = tmp_path / "external.exe"
    executable.write_bytes(b"first executable")
    executable.chmod(0o755)
    definition = CheckDefinition(argv=(str(executable),))
    before = check_context(definition)
    executable.write_bytes(b"other executable")
    assert check_context(definition) != before


def test_context_is_rechecked_after_execution(repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    calls = 0

    def changing_context(*args: object) -> dict[str, object]:
        nonlocal calls
        calls += 1
        return {"external_executable_generation": calls}

    monkeypatch.setattr("agent_checkpoint.runner.check_context", changing_context)
    result = run_check(repo, CheckDefinition(argv=(sys.executable, "-c", "pass")))
    assert result.status == "unknown"
    assert result.reason == "INPUT_CHANGED"
