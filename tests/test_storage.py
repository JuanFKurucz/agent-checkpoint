from pathlib import Path

import pytest

from agent_checkpoint.contracts import Contract, Criterion
from agent_checkpoint.storage import Store, StoreError


def contract() -> Contract:
    return Contract(
        task_id="t",
        worktree_id="w",
        request="Implement validation",
        criteria=(Criterion(id="a", text="Reject invalid input", check_ids=("behavior",)),),
    )


def test_duplicate_start_is_idempotent_and_survives_restart(tmp_path: Path) -> None:
    store = Store(tmp_path / "state")
    first = store.save_contract(contract(), "request1")
    again = Store(tmp_path / "state").save_contract(contract(), "request1")
    assert first == again
    assert store.get_contract("t", "w") == contract()


def test_duplicate_request_with_different_payload_is_conflict(tmp_path: Path) -> None:
    store = Store(tmp_path / "state")
    store.save_contract(contract(), "request1")
    with pytest.raises(StoreError, match="IDEMPOTENCY_CONFLICT"):
        store.save_contract(contract().model_copy(update={"request": "Different"}), "request1")


def test_task_binding_is_checked(tmp_path: Path) -> None:
    store = Store(tmp_path / "state")
    store.save_contract(contract(), "request1")
    with pytest.raises(StoreError, match="TASK_SCOPE_MISMATCH"):
        store.get_contract("t", "wrong")


def test_revision_preserves_history_and_rejects_weakening(tmp_path: Path) -> None:
    store = Store(tmp_path / "state")
    c = contract()
    store.save_contract(c, "r1")
    c2 = c.model_copy(update={"contract_revision": 2, "required_check_ids": ("test",)})
    store.save_contract(c2, "r2", expected_revision=1)
    assert store.get_contract("t", "w").contract_revision == 2
    assert store.get_contract("t", "w", revision=1) == c
    with pytest.raises(StoreError, match="REVISION_CONFLICT"):
        store.save_contract(c2, "r3", expected_revision=1)
    with pytest.raises(StoreError, match="CONTRACT_WEAKENING"):
        store.save_contract(
            c.model_copy(update={"contract_revision": 3}), "r4", expected_revision=2
        )


def test_blobs_are_digest_verified_and_bounded(tmp_path: Path) -> None:
    store = Store(tmp_path / "state", max_blob_bytes=8)
    digest = store.put_blob(b"test")
    assert store.get_blob(digest) == b"test"
    (store.blobs / digest).write_bytes(b"fake")
    with pytest.raises(StoreError, match="BLOB_CORRUPT"):
        store.get_blob(digest)
    with pytest.raises(StoreError, match="BLOB_TOO_LARGE"):
        store.put_blob(b"123456789")
    with pytest.raises(StoreError, match="INVALID_BLOB_ID"):
        store.get_blob("../../private")


def test_corrupt_database_is_not_replaced(tmp_path: Path) -> None:
    state = tmp_path / "state"
    state.mkdir()
    (state / "checkpoint.sqlite3").write_bytes(b"bad database")
    with pytest.raises(StoreError, match="STORAGE_UNAVAILABLE"):
        Store(state)
    assert (state / "checkpoint.sqlite3").read_bytes() == b"bad database"
