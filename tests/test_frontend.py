"""Offline JS regression; Node is a development-only test prerequisite."""

import shutil
import subprocess
from pathlib import Path


def test_dashboard_focus_regression():
    node = shutil.which("node")
    assert node, "Node.js is required for the dashboard interaction regression"
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [
            node,
            str(root / "tests/dashboard_focus.cjs"),
            str(root / "src/agent_checkpoint/web/app.js"),
        ],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
