from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from agent_checkpoint.contracts import Contract, Criterion
from agent_checkpoint.service import CheckEvent, latest_checks
from agent_checkpoint.storage import Store, StoreError


def test_late_older_result_cannot_overwrite_newer_failure() -> None:
    older = CheckEvent(run_id="old", check_id="test", contract_revision=1)
    newer = CheckEvent(run_id="new", check_id="test", contract_revision=1)
    failed = newer.model_copy(update={"phase": "finished", "status": "fail"})
    passed = older.model_copy(update={"phase": "finished", "status": "pass"})
    events = [older, newer, failed, passed]
    assert latest_checks(events)["test"].status == "fail"


def test_unfinished_run_prevents_ready_even_after_a_newer_success() -> None:
    older = CheckEvent(run_id="old", check_id="test", contract_revision=1)
    newer = CheckEvent(run_id="new", check_id="test", contract_revision=1)
    passed = newer.model_copy(update={"phase": "finished", "status": "pass"})
    assert latest_checks([older, newer, passed])["test"].status == "unknown"


def test_orphan_finish_does_not_count_as_observed_run() -> None:
    finish = CheckEvent(
        run_id="orphan", check_id="test", contract_revision=1, phase="finished", status="pass"
    )
    with pytest.raises(StoreError, match="RUN_WITHOUT_START"):
        latest_checks([finish])


def test_request_reservation_is_atomic(tmp_path: Path) -> None:
    store = Store(tmp_path / "state")

    def claim(_: int) -> object:
        return store.claim_request("scope", "request", {"check": "test"})

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(claim, range(16)))
    assert results.count(None) == 1
    assert results.count({"status": "pending"}) == 15


def test_call_budget_survives_restart_and_concurrent_attempts(tmp_path: Path) -> None:
    store = Store(tmp_path / "state")
    store.save_contract(
        Contract(
            task_id="t",
            worktree_id="w",
            request="Do work",
            criteria=(Criterion(id="a", text="Check behavior"),),
        ),
        "start",
    )

    def reserve(_: int) -> str:
        try:
            Store(tmp_path / "state").reserve_call("t", "w", 3)
            return "reserved"
        except StoreError as exc:
            return str(exc)

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(reserve, range(8)))
    assert results.count("reserved") == 3
    assert results.count("BUDGET_EXHAUSTED") == 5


@pytest.mark.parametrize("change", ["revision", "event"])
def test_report_publication_rejects_changed_inputs(tmp_path: Path, change: str) -> None:
    store = Store(tmp_path / "state")
    contract = Contract(
        task_id="t",
        worktree_id="w",
        request="Do work",
        criteria=(Criterion(id="a", text="Check behavior"),),
    )
    store.save_contract(contract, "start")
    guard = store.report_guard("t", "w")
    if change == "revision":
        store.save_contract(contract.model_copy(update={"contract_revision": 2}), "revise", 1)
    else:
        store.append_event("t", "w", "check", {"status": "unknown"})
    with pytest.raises(StoreError, match="REPORT_INPUTS_CHANGED"):
        store.publish_report("t", "w", guard, {"status": "ready"})
    assert store.events("t", "w", "completion") == []
