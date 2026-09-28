"""Conservative input identity, including ignored inputs and transient-edit metadata.

Working-tree snapshots detect ordinary mutation; they are not process isolation.
No private file contents or environment values are persisted in this manifest.
"""

import hashlib
import os
import stat
import subprocess
from dataclasses import dataclass
from pathlib import Path

from agent_checkpoint.storage import digest

# Generated tool/output paths, not arbitrary Git ignore rules. Explicitly tracked
# files under these paths are an error so required inputs cannot vanish silently.
EXCLUDED = frozenset(
    {
        ".git",
        "node_modules",
        ".venv",
        "__pycache__",
        ".pytest_cache",
        ".ruff_cache",
        ".mypy_cache",
        "dist",
        "build",
        "htmlcov",
        ".coverage",
    }
)


class SnapshotError(RuntimeError):
    pass


def stamp(value: os.stat_result) -> tuple[int, int, int, int]:
    return value.st_size, value.st_mtime_ns, value.st_ctime_ns, value.st_ino


def git(root: Path, *args: str, allow_failure: bool = False) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise SnapshotError("GIT_UNAVAILABLE") from exc
    if result.returncode:
        if allow_failure:
            return ""
        raise SnapshotError("INVALID_GIT_WORKTREE")
    return result.stdout.decode("utf-8", errors="strict").strip()


def worktree_identity(root: Path) -> str:
    root = root.resolve()
    top = Path(git(root, "rev-parse", "--show-toplevel")).resolve()
    if root != top:
        raise SnapshotError("ROOT_MUST_BE_WORKTREE")
    common = Path(git(root, "rev-parse", "--path-format=absolute", "--git-common-dir")).resolve()
    return digest(
        {"root": os.path.normcase(str(root)), "git_common": os.path.normcase(str(common))}
    )


@dataclass(frozen=True)
class Snapshot:
    id: str
    worktree_id: str
    base_commit: str
    files: dict[str, str]
    generation: str
    opaque_inputs: tuple[str, ...] = ()


def credential_name(name: str) -> bool:
    return name.casefold() == ".env" or name.casefold().startswith(".env.")


def capture(
    root: Path,
    *,
    context: object = None,
    max_file_bytes: int = 16_777_216,
    max_files: int = 20_000,
) -> Snapshot:
    root = root.resolve()
    identity = worktree_identity(root)
    base = git(root, "rev-parse", "--verify", "HEAD", allow_failure=True) or "UNBORN"
    tracked = git(root, "ls-files", "--stage", "-z")
    for entry in tracked.split("\0"):
        if not entry:
            continue
        mode, _, rest = entry.split(" ", 2)
        name = rest.split("\t", 1)[1]
        if credential_name(Path(name).name):
            raise SnapshotError("TRACKED_CREDENTIAL_FILE")
        if mode == "160000":
            raise SnapshotError("SUBMODULE_INPUT_UNSUPPORTED")
        if any(part in EXCLUDED for part in Path(name).parts):
            raise SnapshotError("TRACKED_INPUT_EXCLUDED")
    files: dict[str, str] = {}
    metadata: dict[str, tuple[int, int, int, int]] = {}
    opaque: list[str] = []

    def scan(directory: Path) -> None:
        try:
            entries = sorted(directory.iterdir())
        except OSError as exc:
            raise SnapshotError("INPUT_UNAVAILABLE") from exc
        for child in entries:
            if child.name in EXCLUDED or child.name.endswith(".egg-info"):
                continue
            try:
                before = child.lstat()
                if stat.S_ISLNK(before.st_mode) or (
                    getattr(before, "st_file_attributes", 0) & 0x400
                ):
                    raise SnapshotError("LINK_INPUT_UNSUPPORTED")
                if child.is_dir():
                    scan(child)
                    continue
                if not stat.S_ISREG(before.st_mode):
                    raise SnapshotError("SPECIAL_INPUT_UNSUPPORTED")
                if len(files) >= max_files:
                    raise SnapshotError("TOO_MANY_INPUTS")
                if credential_name(child.name):
                    # Do not open credential files, even for hashing. Metadata
                    # detects ordinary changes but is explicitly not content proof.
                    name = child.relative_to(root).as_posix()
                    metadata[name] = stamp(before)
                    files[name] = digest({"opaque_credential_metadata": stamp(before)})
                    opaque.append(name)
                    continue
                with child.open("rb") as handle:
                    content = handle.read(max_file_bytes + 1)
                after = child.stat()
            except OSError as exc:
                raise SnapshotError("INPUT_UNAVAILABLE") from exc
            if len(content) > max_file_bytes:
                raise SnapshotError("INPUT_TOO_LARGE")
            if stamp(before) != stamp(after):
                raise SnapshotError("INPUT_CHANGED_DURING_SNAPSHOT")
            name = child.relative_to(root).as_posix()
            files[name] = digest(
                {"sha256": hashlib.sha256(content).hexdigest(), "mode": stat.S_IMODE(after.st_mode)}
            )
            metadata[name] = stamp(after)

    scan(root)
    index = Path(git(root, "rev-parse", "--path-format=absolute", "--git-path", "index"))
    try:
        index_hash = (
            hashlib.sha256(index.read_bytes()).hexdigest() if index.exists() else "NO_INDEX"
        )
    except OSError as exc:
        raise SnapshotError("INDEX_UNAVAILABLE") from exc
    return Snapshot(
        id=digest(
            {
                "version": 2,
                "worktree": identity,
                "base": base,
                "index": index_hash,
                "files": files,
                "context": context,
            }
        ),
        worktree_id=identity,
        base_commit=base,
        files=files,
        generation=digest(metadata),
        opaque_inputs=tuple(opaque),
    )
