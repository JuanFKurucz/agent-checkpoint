"""Bound wire responses before the optional SDK decodes or validates them."""

import httpx2

from agent_checkpoint.storage import StoreError


class BoundedGatewayTransport(httpx2.AsyncBaseTransport):
    def __init__(self, inner: httpx2.AsyncBaseTransport | None, limit: int = 65536) -> None:
        self.inner = inner or httpx2.AsyncHTTPTransport(retries=0, trust_env=False)
        self.limit = limit

    async def handle_async_request(self, request: httpx2.Request) -> httpx2.Response:
        request.headers["Accept-Encoding"] = "identity"
        response = await self.inner.handle_async_request(request)
        try:
            if response.headers.get("Content-Encoding", "identity").lower() != "identity":
                raise StoreError("RESPONSE_ENCODING_UNSUPPORTED")
            if response.is_stream_consumed:
                data = response.content
                if len(data) > self.limit:
                    raise StoreError("PROVIDER_RESPONSE_TOO_LARGE")
            else:
                buffer = bytearray()
                async for chunk in response.aiter_raw():
                    if len(buffer) + len(chunk) > self.limit:
                        raise StoreError("PROVIDER_RESPONSE_TOO_LARGE")
                    buffer.extend(chunk)
                data = bytes(buffer)
            return httpx2.Response(
                response.status_code,
                headers=response.headers,
                content=data,
                extensions=response.extensions,
                request=request,
            )
        finally:
            await response.aclose()

    async def aclose(self) -> None:
        await self.inner.aclose()
