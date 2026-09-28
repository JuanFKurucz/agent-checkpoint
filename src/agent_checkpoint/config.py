"""Explicit launcher-owned configuration. No arbitrary overrides on tool requests."""

import json
from pathlib import Path
from typing import Literal, Self

from pydantic import ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel

from agent_checkpoint.contracts import Name, Record, Text
from agent_checkpoint.gateway import GatewayPolicy
from agent_checkpoint.runner import CheckDefinition, check_environment


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def read_json(path: Path, limit: int = 262144) -> dict[str, object]:
    if path.name.lower() == ".env" or path.name.lower().startswith(".env."):
        raise ValueError("CREDENTIAL_FILE_DENIED")
    with path.open("rb") as stream:
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise ValueError("INPUT_TOO_LARGE")
    value = json.loads(data, object_pairs_hook=_unique_object)
    if not isinstance(value, dict):
        raise ValueError("JSON_OBJECT_REQUIRED")
    return value


class ConfigRecord(Record):
    model_config = ConfigDict(extra="forbid", frozen=True, alias_generator=to_camel)


class ConfigCheck(ConfigRecord):
    argv: tuple[Name, ...] = Field(min_length=1)
    cwd: Name = "."
    timeout_seconds: float = Field(default=120, gt=0, le=3600, allow_inf_nan=False)
    max_output_bytes: int = Field(default=32768, ge=1, le=1048576, strict=True)
    env_allow: tuple[Name, ...] = ()
    execution_mode: Literal["working_tree", "isolated_snapshot"] = "working_tree"
    required: bool = Field(default=False, strict=True)

    def definition(self) -> CheckDefinition:
        result = CheckDefinition.model_validate(self.model_dump(exclude={"required"}))
        check_environment(result)
        return result


class Skill(ConfigRecord):
    description: Text
    mandatory: bool = Field(default=False, strict=True)
    keywords: tuple[Name, ...] = ()


class ProviderConfig(ConfigRecord):
    kind: Literal["jev"] = "jev"
    enabled: bool = Field(default=False, strict=True)
    remote_allowed: bool = Field(default=False, strict=True)
    base_url: Literal["https://ai-gateway.vercel.sh/typesafe"] = (
        "https://ai-gateway.vercel.sh/typesafe"
    )
    model: Literal["typesafe-ai/jev"] = "typesafe-ai/jev"
    api_key_env: Literal["AI_GATEWAY_API_KEY"] = "AI_GATEWAY_API_KEY"
    max_calls_per_task: int = Field(default=6, ge=1, le=6, strict=True)
    max_input_bytes: int = Field(default=65536, ge=1, le=65536, strict=True)
    timeout_seconds: float = Field(default=2.5, gt=0, le=30, allow_inf_nan=False)
    approved_input_digests: tuple[str, ...] = ()
    approved_payload_kinds: tuple[Literal["single_route", "criterion_evidence"], ...] = ()
    spend_acknowledged: bool = Field(default=False, strict=True)

    @model_validator(mode="after")
    def explicit_approval(self) -> Self:
        if self.enabled and self.remote_allowed and not self.spend_acknowledged:
            raise ValueError("SPEND_ACKNOWLEDGEMENT_REQUIRED")
        return self

    def policy(self) -> GatewayPolicy:
        return GatewayPolicy.model_validate(
            self.model_dump(
                exclude={
                    "kind",
                    "approved_input_digests",
                    "approved_payload_kinds",
                    "spend_acknowledged",
                }
            )
        )


class Configuration(ConfigRecord):
    schema_version: Literal[1] = 1
    mode: Literal["observe", "advise"] = "advise"
    checks: dict[Name, ConfigCheck]
    skills: dict[Name, Skill] = Field(default_factory=dict, max_length=39)
    provider: ProviderConfig = Field(default_factory=ProviderConfig)

    @model_validator(mode="after")
    def reserved(self) -> Self:
        if "none" in self.skills:
            raise ValueError("RESERVED_SKILL_ID")
        return self
