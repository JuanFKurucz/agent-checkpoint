"""Completion wire schema; other tools retain their v1 output contracts for now."""

from typing import Literal

from pydantic import TypeAdapter, ValidationError

from agent_checkpoint.contracts import Completion, Name, Record
from agent_checkpoint.gateway import Decision
from agent_checkpoint.storage import StoreError


class AdvisoryFinding(Decision):
    criterion_id: Name
    authority: Literal["semantic_advisory"]


class AdvisoryReview(Record):
    schema_version: Literal["1"]
    task_id: Name
    contract_revision: int
    snapshot_id: Name
    generation: Name
    findings: tuple[AdvisoryFinding, ...]
    status: Literal["reviewed", "unavailable"]
    reason: str


class CompletionResponse(Completion):
    advisory_findings: tuple[AdvisoryReview, ...]
    assessment_scope: Literal["declared_evidence_only"] = "declared_evidence_only"
    assessment_notice: Literal[
        "Assesses declared evidence, not overall product correctness or semantic coverage."
    ] = "Assesses declared evidence, not overall product correctness or semantic coverage."


class ErrorResponse(Record):
    status: Literal["error"]
    code: Name


def completion_output_schema() -> dict[str, object]:
    schema = TypeAdapter(CompletionResponse | ErrorResponse).json_schema()
    return {"type": "object", **schema}


def validate_completion_output(output: object) -> dict[str, object]:
    try:
        return CompletionResponse.model_validate(output).model_dump(mode="json")
    except ValidationError as exc:
        # Do not expose a malformed stored finding or its raw validation details.
        raise StoreError("INVALID_COMPLETION_OUTPUT") from exc
