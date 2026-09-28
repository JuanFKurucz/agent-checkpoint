import subprocess
from pathlib import Path

import pytest

from agent_checkpoint.snapshot import capture


def test_secret_files_are_never_opened_and_metadata_changes_invalidate(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    root.mkdir()
    subprocess.run(["git", "init", "--quiet", str(root)], check=True)
    secret = root / ".env.local"
    secret.write_text("SYNTHETIC_PLACEHOLDER=one")
    original = Path.open

    def guarded(path, *args, **kwargs):
        if path == secret:
            raise AssertionError("Secret contents must never be read by snapshot capture")
        return original(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", guarded)
    first = capture(root)
    with original(secret, "w") as handle:
        handle.write("SYNTHETIC_PLACEHOLDER=changed")
    second = capture(root)
    assert first.id != second.id
    assert ".env.local" in first.files
    assert "SYNTHETIC_PLACEHOLDER" not in str(first)


def test_tracked_secret_file_is_rejected_without_reading(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    subprocess.run(["git", "init", "--quiet", str(root)], check=True)
    (root / ".env").write_text("SYNTHETIC_PLACEHOLDER=one")
    subprocess.run(["git", "-C", str(root), "add", ".env"], check=True)
    with pytest.raises(RuntimeError, match="TRACKED_CREDENTIAL_FILE"):
        capture(root)
