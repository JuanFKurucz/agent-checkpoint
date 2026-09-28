import asyncio
import json
import subprocess
import sys
from pathlib import Path

import pytest
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

pytestmark = pytest.mark.allow_hosts(["127.0.0.1", "::1"])


def test_real_stdio_exchange_lists_and_calls_all_five_tools(tmp_path: Path) -> None:
    root = tmp_path / "mcp repo"
    root.mkdir()
    subprocess.run(["git", "init", "--quiet", str(root)], check=True)
    config = root / "checkpoint.json"
    config.write_text(
        json.dumps(
            {
                "checks": {
                    "test": {"argv": [sys.executable, "-c", "print('verified')"], "required": True}
                },
                "skills": {"tests": {"description": "Tests", "mandatory": True}},
            }
        )
    )

    async def exercise():
        server = StdioServerParameters(
            command=sys.executable,
            args=[
                "-m",
                "agent_checkpoint",
                "--root",
                str(root),
                "--state",
                str(tmp_path / "state"),
                "mcp",
                "--stdio",
            ],
        )
        async with stdio_client(server) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                listed = await session.list_tools()
                completion_tool = next(t for t in listed.tools if t.name == "checkpoint_completion")
                schema = completion_tool.output_schema
                assert schema["type"] == "object"
                assert "CompletionResponse" in schema["$defs"]
                assert schema["$defs"]["CompletionResponse"]["additionalProperties"] is False
                assert {t.name for t in listed.tools} == {
                    "checkpoint_start_task",
                    "checkpoint_route",
                    "checkpoint_run_checks",
                    "checkpoint_review",
                    "checkpoint_completion",
                    "checkpoint_report",
                }
                created = await session.call_tool(
                    "checkpoint_start_task",
                    {
                        "request": {"text": "Verify behavior"},
                        "request_id": "start",
                        "criteria": [{"id": "a", "text": "Verified", "check_ids": ["test"]}],
                    },
                )
                assert not created.is_error, created
                task = created.structured_content["task_id"]
                for tool, payload in [
                    ("checkpoint_route", {"task_id": task}),
                    ("checkpoint_review", {"task_id": task}),
                    (
                        "checkpoint_run_checks",
                        {"task_id": task, "check_ids": ["test"], "request_id": "run"},
                    ),
                ]:
                    result = await session.call_tool(tool, payload)
                    assert not result.is_error, result
                    assert result.structured_content
                report = await session.call_tool("checkpoint_completion", {"task_id": task})
                assert report.structured_content["status"] == "ready"
                assert report.structured_content["schema_version"] == "2"
                assert report.structured_content["next_actions"] == []
                assert report.structured_content["assessment_scope"] == "declared_evidence_only"
                assert json.loads(report.content[0].text) == report.structured_content
                report_tool = next(t for t in listed.tools if t.name == "checkpoint_report")
                assert report_tool.annotations.read_only_hint is True
                assert report_tool.annotations.open_world_hint is False
                assert "Report" in report_tool.output_schema["$defs"]
                history = await session.call_tool("checkpoint_report", {"task_id": task})
                assert not history.is_error
                assert history.structured_content["readiness"] == "not_revalidated"
                assert history.structured_content["last_recorded_completion"]["status"] == "ready"
                invalid = await session.call_tool(
                    "checkpoint_completion", {"task_id": task, "private_unknown": "must-not-echo"}
                )
                assert invalid.is_error
                assert "must-not-echo" not in invalid.model_dump_json()

    asyncio.run(exercise())
