import runpy
import sys
from pathlib import Path

import pytest


@pytest.mark.parametrize("scenario", ["passing", "failure_repair", "stale_repair"])
def test_measurement_conditions_have_equal_acceptance_checks(tmp_path: Path, scenario: str) -> None:
    script = Path(__file__).resolve().parents[1] / "scripts" / "measure_scenarios.py"
    trial = runpy.run_path(str(script))["trial"]
    baseline = trial(Path(sys.executable), tmp_path, "baseline", scenario, 1)
    checkpoint = trial(Path(sys.executable), tmp_path, "checkpoint", scenario, 1)
    assert baseline["outcome"] == checkpoint["outcome"] == "pass"
    assert baseline["acceptance_argv"] == checkpoint["acceptance_argv"]
    assert baseline["verify_sha256"] == checkpoint["verify_sha256"]
    expected_checks = {"passing": 1, "failure_repair": 2, "stale_repair": 3}[scenario]
    assert len(baseline["attempts"]) == expected_checks
    assert sum("check" in a["argv"] for a in checkpoint["attempts"]) == expected_checks
    assert baseline["provider_requests"] == checkpoint["provider_requests"] == 0
