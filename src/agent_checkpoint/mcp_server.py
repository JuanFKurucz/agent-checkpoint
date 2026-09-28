"""Flat-schema MCP tools backed by the same validated runtime as the CLI."""

import asyncio
import json

import anyio
import mcp_types as types
from mcp.server import Server, ServerRequestContext
from mcp.server.stdio import stdio_server

from agent_checkpoint import __version__
from agent_checkpoint.outputs import completion_output_schema, validate_completion_output
from agent_checkpoint.reporting import Report, report_output_schema
from agent_checkpoint.runtime import INPUTS, Runtime
from agent_checkpoint.snapshot import SnapshotError
from agent_checkpoint.storage import StoreError

DESCRIPTIONS = {
    "checkpoint_start_task": "Register or additively revise an immutable task contract.",
    "checkpoint_route": "Select optional skills; mandatory repository skills cannot be removed.",
    "checkpoint_run_checks": "Execute configured check IDs and record snapshot-bound evidence.",
    "checkpoint_review": "Record advisory review; disabled providers return unavailable.",
    "checkpoint_report": (
        "Read bounded historical metadata, not current readiness. "
        "Never execute checks, call a provider or append evidence."
    ),
    "checkpoint_completion": (
        "Assess declared evidence, not overall product correctness. "
        "Never execute checks or call a provider."
    ),
}


def build_server(runtime: Runtime) -> Server[None]:
    runtime.transport = "mcp"

    async def list_tools(
        ctx: ServerRequestContext[None], params: types.PaginatedRequestParams | None
    ) -> types.ListToolsResult:
        return types.ListToolsResult(
            tools=[
                types.Tool(
                    name=name,
                    description=DESCRIPTIONS[name],
                    input_schema=schema.model_json_schema(),
                    output_schema=completion_output_schema()
                    if name == "checkpoint_completion"
                    else report_output_schema()
                    if name == "checkpoint_report"
                    else {"type": "object"},
                    annotations=types.ToolAnnotations(
                        read_only_hint=name == "checkpoint_report",
                        destructive_hint=False,
                        open_world_hint=name
                        in {"checkpoint_review", "checkpoint_route", "checkpoint_run_checks"},
                    ),
                )
                for name, schema in INPUTS.items()
            ]
        )

    async def call_tool(
        ctx: ServerRequestContext[None], params: types.CallToolRequestParams
    ) -> types.CallToolResult:
        error = False
        try:
            # Blocking approved checks must not stall the protocol receive loop.
            output = await anyio.to_thread.run_sync(
                runtime.call, params.name, dict(params.arguments or {})
            )
            if params.name == "checkpoint_completion":
                output = validate_completion_output(output)
            elif params.name == "checkpoint_report":
                output = Report.model_validate(output).model_dump(mode="json")
        except (StoreError, SnapshotError) as exc:
            output = {"status": "error", "code": str(exc)}
            error = True
        except (ValueError, OSError):
            output = {"status": "error", "code": "INVALID_INPUT_OR_CONFIG"}
            error = True
        except Exception:
            output = {"status": "error", "code": "RUNTIME_UNAVAILABLE"}
            error = True
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=json.dumps(output, ensure_ascii=True))],
            structured_content=output,
            is_error=error,
        )

    return Server(
        name="agent-checkpoint",
        version=__version__,
        on_list_tools=list_tools,
        on_call_tool=call_tool,
    )


def serve(runtime: Runtime) -> None:
    async def run() -> None:
        server = build_server(runtime)
        async with stdio_server() as (read, write):
            await server.run(read, write, server.create_initialization_options())

    asyncio.run(run())
