# Jev-only Vercel AI Gateway smoke example

Separate user-requested TypeScript example; Agent Checkpoint remains Python.
This example uses npm because the repository's uv manager cannot install the npm
`ai` package and there was no existing JavaScript package manager/manifest.

1. Enter a replacement gateway key locally in the repository root `.env.local` as
   `AI_GATEWAY_API_KEY=...`. Never paste credentials into chat or commit them.
2. From this directory, run `npm ci --ignore-scripts`, then `npm run typecheck`.
3. Run `npm start` for one synthetic Jev skill-selection request. It prints only
   sanitized decision/usage metadata, never credentials or raw transport objects.

The request uses an explicit Vercel Gateway provider and typesafe-ai/jev via the
experimental evaluation API, no SDK retries, and a five-second deadline. It sends
no repository code. Provider/account billing remains
the user's responsibility; it is not a hard dollar-cap mechanism. No local tracing
is enabled. Vercel may retain gateway operational records under account settings.

The runtime loads the ignored secret without displaying it. Exceptions are not
printed. Do not turn on HTTP/debug logging while testing credentials.

Validated 2026-09-27: `npm run typecheck` and `npm start` pass with Jev. The returned
choice was testing; usage was 350 input / 38 output tokens; measured evaluation
time was 692 ms (command wall time 2.97 s). Requested/reported model was
typesafe-ai/jev. This is an alias, not proof of an exact underlying model version;
the SDK can fill absent response model metadata from the requested model.

Historical, superseded test: after the user entered the key
locally, `npm start` exited 0 and returned a nonempty holiday description titled
Lanternleaf Day. No key or raw request/error payload was printed. Observed command
wall time was 6.60 seconds; billing was not independently inspected. GPT-5.5 text
generation was not a Jev decision-model integration test. The user's later
Jev-through-Gateway-only instruction supersedes that example; no GPT code remains
in the runnable script. Do not rerun GPT or use the direct TypeSafe endpoint.

References: [AI Gateway quickstart](https://vercel.com/docs/ai-gateway/getting-started),
[TypeSafe-compatible gateway](https://vercel.com/docs/ai-gateway/sdks-and-apis/typesafe).
