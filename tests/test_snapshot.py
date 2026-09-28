import subprocess
from pathlib import Path

import pytest

from agent_checkpoint.snapshot import SnapshotError, capture, worktree_identity


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo with spaces"
    root.mkdir()
    subprocess.run(["git", "init", "--quiet", str(root)], check=True)
    (root / "code.py").write_text("original", encoding="utf-8")
    return root


def test_snapshot_handles_unborn_head_and_untracked_inputs(repo: Path) -> None:
    first = capture(repo)
    assert first.base_commit == "UNBORN"
    assert "code.py" in first.files
    assert capture(repo).id == first.id
    (repo / "code.py").write_text("changed", encoding="utf-8")
    assert capture(repo).id != first.id


def test_snapshot_tracks_deletion_and_relevant_ignored_files(repo: Path) -> None:
    (repo / ".gitignore").write_text("settings.ini\n", encoding="utf-8")
    (repo / "settings.ini").write_text("A=1", encoding="utf-8")
    first = capture(repo)
    assert "settings.ini" in first.files
    (repo / "settings.ini").unlink()
    assert capture(repo).id != first.id


def test_edit_and_revert_changes_observation_metadata(repo: Path) -> None:
    first = capture(repo)
    (repo / "code.py").write_text("mutated", encoding="utf-8")
    (repo / "code.py").write_text("original", encoding="utf-8")
    second = capture(repo)
    assert second.files["code.py"] == first.files["code.py"]
    assert second.generation != first.generation


def test_policy_and_environment_participate_in_identity(repo: Path) -> None:
    first = capture(repo, context={"policy": "v1", "runtime": "a"})
    assert capture(repo, context={"policy": "v2", "runtime": "a"}).id != first.id
    assert capture(repo, context={"policy": "v1", "runtime": "b"}).id != first.id


def test_metadata_and_output_directories_are_not_inputs(repo: Path) -> None:
    first = capture(repo)
    (repo / ".pytest_cache").mkdir()
    (repo / ".pytest_cache" / "cache").write_text("generated", encoding="utf-8")
    assert capture(repo).id == first.id


def test_worktrees_have_distinct_identity(repo: Path, tmp_path: Path) -> None:
    other = tmp_path / "other"
    other.mkdir()
    subprocess.run(["git", "init", "--quiet", str(other)], check=True)
    assert worktree_identity(repo) != worktree_identity(other)


def test_scope_limits_are_errors_not_silent_omissions(repo: Path) -> None:
    with pytest.raises(SnapshotError, match="INPUT_TOO_LARGE"):
        capture(repo, max_file_bytes=2)
