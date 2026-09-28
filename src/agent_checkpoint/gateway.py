"""Optional Jev decision transport. Vercel only; never a generative-model fallback."""

import asyncio
import logging
import math
import os
from time import monotonic
from typing import TYPE_CHECKING, Final, Literal, Self
from uuid import uuid4

from pydantic import Field, model_validator

from agent_checkpoint.contracts import Name, Record, Text
from agent_checkpoint.storage import Store, StoreError, canonical, digest

if TYPE_CHECKING:
    import httpx2

GATEWAY_URL: Final = "https://ai-gateway.vercel.sh/typesafe"
GATEWAY_MODEL: Final = "typesafe-ai/jev"


class GatewayPolicy(Record):
    base_url: Literal["https://ai-gateway.vercel.sh/typesafe"] = GATEWAY_URL
    model: Literal["typesafe-ai/jev"] = GATEWAY_MODEL
    api_key_env: Literal["AI_GATEWAY_API_KEY"] = "AI_GATEWAY_API_KEY"
    enabled: bool = Field(default=False, strict=True)
    remote_allowed: bool = Field(default=False, strict=True)
    max_calls_per_task: int = Field(default=6, ge=1, le=6, strict=True)
    max_input_bytes: int = Field(default=65536, ge=1, le=65536, strict=True)
    timeout_seconds: float = Field(default=2.5, gt=0, le=30, allow_inf_nan=False)


class SelectionRequest(Record):
    kind: Literal["single_route", "criterion_evidence"] = "single_route"
    state: Text
    instructions: Text
    candidates: dict[Name, Text] = Field(min_length=2, max_length=40)
    rubric_version: Name = "1"

    @model_validator(mode="after")
    def abstention(self) -> Self:
        required = "none" if self.kind == "single_route" else "insufficient"
        if required not in self.candidates:
            raise ValueError("MISSING_ABSTENTION_CHOICE")
        if self.kind == "criterion_evidence" and set(self.candidates) != {
            "supported",
            "contradicted",
            "insufficient",
        }:
            raise ValueError("INVALID_REVIEW_CHOICES")
        return self


class Decision(Record):
    schema_version: Literal["1"] = "1"
    decision_id: str = Field(default_factory=lambda: str(uuid4()))
    status: Literal["selected", "none", "unavailable"]
    selected: str | None = None
    reason: str = ""
    requested_model: str = GATEWAY_MODEL
    returned_model: str | None = None
    identity_verified: Literal[False] = False
    identity_note: str = "Gateway alias does not attest an exact Jev weights/version pin"
    physical_requests: int = 0
    input_tokens: int | None = None
    output_tokens: int | None = None
    billed_usd: None = None
    confidence: float | None = None
    duration_seconds: float = 0


class GatewayJev:
    """Internal adapter: callers must first approve exact data scope and spend.

    No file discovery, credential logging, fallback endpoints or retries. The
    optional test transport is a Python construction seam, not a wire parameter.
    Both task budget and request replay protection are durable across restarts.
    """

    def __init__(
        self,
        store: Store,
        policy: GatewayPolicy,
        *,
        transport: "httpx2.AsyncBaseTransport | None" = None,
    ) -> None:
        self.store = store
        self.policy = policy
        self.transport = transport

    async def select(
        self, task_id: str, worktree_id: str, request_id: str, request: SelectionRequest
    ) -> Decision:
        contract = self.store.get_contract(task_id, worktree_id)
        if not self.policy.enabled or not self.policy.remote_allowed:
            return Decision(status="unavailable", reason="PROVIDER_DISABLED")
        body = {
            "model": GATEWAY_MODEL,
            "state": request.state,
            "questions": {
                "selection": {
                    "type": "choice",
                    "instructions": request.instructions,
                    "criteria": request.candidates,
                }
            },
        }
        if len(canonical(body).encode("utf-8")) > self.policy.max_input_bytes:
            return Decision(status="unavailable", reason="INPUT_TOO_LARGE")
        # Environment lookup is runtime-only; never return the value in diagnostics.
        key = os.environ.get("AI_GATEWAY_API_KEY", "").strip()
        if not key:
            return Decision(status="unavailable", reason="CREDENTIAL_UNAVAILABLE")
        try:
            import httpx2
            from typesafe_sdk import (
                AsyncTypeSafeClient,
                Choice,
                RetryPolicy,
                TypeSafeAPIResponseValidationError,
                TypeSafeAPITimeoutError,
                TypeSafeError,
            )

            from agent_checkpoint.gateway_transport import BoundedGatewayTransport
        except ImportError:
            return Decision(status="unavailable", reason="PROVIDER_DEPENDENCY_UNAVAILABLE")
        # The SDK supports wire-body debug logging; the application never enables it.
        for name in ("typesafe_sdk", "httpx2", "httpcore2"):
            logging.getLogger(name).disabled = True
        scope = "provider:" + task_id
        replay = self.store.claim_request(
            scope,
            request_id,
            {
                "request": request.model_dump(),
                "policy": self.policy.model_dump(),
                "revision": contract.contract_revision,
            },
        )
        if replay is not None:
            if replay.get("status") == "pending":
                return Decision(status="unavailable", reason="INTERRUPTED_OR_RUNNING")
            return Decision.model_validate(replay)
        started = monotonic()
        physical = 0

        async def before_send(outgoing: httpx2.Request) -> None:
            nonlocal physical
            if str(outgoing.url) != GATEWAY_URL + "/v1/systemone" or outgoing.method != "POST":
                raise StoreError("DESTINATION_NOT_ALLOWED")
            if len(outgoing.content) > self.policy.max_input_bytes:
                raise StoreError("INPUT_TOO_LARGE")
            if physical:
                raise StoreError("RETRY_NOT_ALLOWED")
            self.store.reserve_call(task_id, worktree_id, self.policy.max_calls_per_task)
            physical += 1

        try:
            async with asyncio.timeout(self.policy.timeout_seconds):
                async with httpx2.AsyncClient(
                    transport=BoundedGatewayTransport(self.transport),
                    follow_redirects=False,
                    trust_env=False,
                    timeout=self.policy.timeout_seconds,
                    event_hooks={"request": [before_send]},
                ) as http:
                    async with AsyncTypeSafeClient(
                        api_key=key,
                        base_url=GATEWAY_URL,
                        model=GATEWAY_MODEL,
                        retry=RetryPolicy(max_retries=0),
                        http_client=http,
                    ) as client:
                        result = await client.system_one(
                            state=request.state,
                            questions={
                                "selection": Choice(
                                    instructions=request.instructions,
                                    criteria={k: v for k, v in request.candidates.items()},
                                )
                            },
                        )
            if result.model != GATEWAY_MODEL:
                decision = Decision(status="unavailable", reason="MODEL_IDENTITY_MISMATCH")
            else:
                answer = result.choices.get("selection")
                if (
                    answer is None
                    or answer.choice not in request.candidates
                    or not math.isfinite(answer.confidence)
                    or not 0 <= answer.confidence <= 1
                    or set(answer.probabilities) != set(request.candidates)
                    or any(
                        not math.isfinite(p) or not 0 <= p <= 1
                        for p in answer.probabilities.values()
                    )
                    or abs(sum(answer.probabilities.values()) - 1) > 0.02
                ):
                    decision = Decision(status="unavailable", reason="MALFORMED_RESPONSE")
                else:
                    decision = Decision(
                        status="none" if answer.choice in {"none", "insufficient"} else "selected",
                        selected=answer.choice,
                        confidence=answer.confidence,
                        returned_model=result.model,
                        input_tokens=result.usage.input_tokens,
                        output_tokens=result.usage.output_tokens,
                    )
        except (TimeoutError, TypeSafeAPITimeoutError):
            decision = Decision(status="unavailable", reason="PROVIDER_TIMEOUT")
        except TypeSafeAPIResponseValidationError:
            decision = Decision(status="unavailable", reason="MALFORMED_RESPONSE")
        except StoreError as exc:
            decision = Decision(status="unavailable", reason=str(exc))
        except (TypeSafeError, httpx2.HTTPError, ValueError):
            decision = Decision(status="unavailable", reason="PROVIDER_UNAVAILABLE")
        decision = decision.model_copy(
            update={
                "physical_requests": physical,
                "duration_seconds": monotonic() - started,
            }
        )
        self.store.append_event(
            task_id,
            worktree_id,
            "decision",
            {
                **decision.model_dump(),
                "input_digest": digest(request.model_dump()),
                "contract_revision": contract.contract_revision,
            },
        )
        self.store.finish_request(scope, request_id, decision.model_dump())
        return decision
