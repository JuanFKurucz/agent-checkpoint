"""Exercise the candidate MCP tools with the Python that launches this script (-I).

Use a noneditable installed Python. No real repository or provider data is used.
"""

import argparse
import asyncio
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def exercise(base, record):
    root = base / "mcp repo with spaces"
    root.mkdir()
    subprocess.run(["git", "init", "--quiet", str(root)], check=True, capture_output=True)
    (root / "checkpoint.json").write_text(
        json.dumps(
            {
                "checks": {
                    "test": {
                        "argv": [sys.executable, "-I", "-c", "assert 2 == 2"],
                        "required": True,
                    }
                },
                "skills": {"safety": {"description": "Synthetic invariant", "mandatory": True}},
            }
        ),
        encoding="utf-8",
    )
    server = StdioServerParameters(
        command=sys.executable,
        args=[
            "-I",
            "-m",
            "agent_checkpoint",
            "--root",
            str(root),
            "--state",
            str(base / "state"),
            "mcp",
            "--stdio",
        ],
    )
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            initialized = await session.initialize()
            record["initialize"] = initialized.model_dump(mode="json")
            tools = await session.list_tools()
            names = [tool.name for tool in tools.tools]
            assert {
                "checkpoint_start_task",
                "checkpoint_route",
                "checkpoint_review",
                "checkpoint_run_checks",
                "checkpoint_completion",
            } <= set(names)
            record["listed_tools"] = names

            async def call(name, data):
                result = await session.call_tool(name, data)
                assert not result.is_error
                record["calls"].append({"name": name, "result": result.structured_content})
                return result.structured_content

            task = await call(
                "checkpoint_start_task",
                {
                    "request": {"text": "Verify synthetic behavior"},
                    "request_id": "start",
                    "criteria": [{"id": "a", "text": "Verified", "check_ids": ["test"]}],
                },
            )
            payload = {"task_id": task["task_id"]}
            missing = await call("checkpoint_completion", payload)
            assert missing["status"] == "unresolved"
            route = await call("checkpoint_route", {**payload, "request_id": "route"})
            assert route["mandatory"] == ["safety"]
            review = await call("checkpoint_review", {**payload, "request_id": "review"})
            assert review["status"] == "unavailable" and review["reason"] == "PROVIDER_DISABLED"
            check = await call(
                "checkpoint_run_checks",
                {
                    **payload,
                    "request_id": "check",
                    "check_ids": ["test"],
                },
            )
            assert check["runs"][0]["status"] == "pass"
            ready = await call("checkpoint_completion", payload)
            assert ready["status"] == "ready"
            if "checkpoint_report" in names:
                history = await call("checkpoint_report", payload)
                assert history["readiness"] == "not_revalidated"
                assert history["last_recorded_completion"]["status"] == "ready"
            invalid = await session.call_tool(
                "checkpoint_completion", {**payload, "unknown": "reject"}
            )
            assert invalid.is_error
            record["invalid_request_rejected"] = True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Choose a new output path")
    base = Path(tempfile.mkdtemp(prefix="checkpoint-installed-mcp-"))
    record = {
        "python": sys.executable,
        "fixture": str(base),
        "status": "incomplete",
        "calls": [],
        "native_host_test": False,
        "provider_requests": 0,
    }
    start = time.perf_counter()
    try:
        asyncio.run(exercise(base, record))
        record["status"] = "pass"
    finally:
        record["seconds"] = time.perf_counter() - start
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print("Installed MCP exchange passed; native host integration remains unverified.")


if __name__ == "__main__":
    main()
