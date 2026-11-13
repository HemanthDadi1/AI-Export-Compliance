"""Run the review agent on the sample plant from the command line.

    pip install google-adk          # Python 3.10+
    export GOOGLE_API_KEY=...       # a Gemini key from Google AI Studio (GEMINI_API_KEY also works)
    python3 -m agent.run            # from the mvp/ folder
"""
import asyncio
import os

import server

# Load the sample files with the rule parser. Gemini is used only by the agent here.
key = os.environ.pop("GEMINI_API_KEY", None)
vertex = os.environ.pop("VERTEX_PROJECT", None)
for path in ("/api/reset", "/api/demo", "/api/review_all"):
    server.dispatch("POST", path, {}, None)
if key:
    os.environ.setdefault("GOOGLE_API_KEY", key)
if vertex:
    os.environ["VERTEX_PROJECT"] = vertex

from google.adk.runners import InMemoryRunner  # noqa: E402  (after the env is set)
from google.genai import types  # noqa: E402

from agent.agent import root_agent  # noqa: E402


async def main():
    runner = InMemoryRunner(agent=root_agent, app_name="cimex")
    session = await runner.session_service.create_session(app_name="cimex", user_id="clerk")
    ask = types.Content(role="user", parts=[types.Part(text="Review this plant's files for the 2027 report.")])
    async for event in runner.run_async(user_id="clerk", session_id=session.id, new_message=ask):
        for part in (event.content.parts if event.content else []) or []:
            if part.function_call:
                print(f"[tool] {part.function_call.name}")
            elif part.text:
                print(part.text)


if __name__ == "__main__":
    if not os.environ.get("GOOGLE_API_KEY") and not os.environ.get("GOOGLE_GENAI_USE_VERTEXAI"):
        raise SystemExit("Set GOOGLE_API_KEY (or GEMINI_API_KEY) to a Gemini key first.")
    try:
        asyncio.run(main())
    except Exception as e:  # show the API's reason, not a long traceback
        code, msg = getattr(e, "code", None), getattr(e, "message", None) or str(e)
        if code == 401 or "API key not valid" in msg:
            raise SystemExit("Gemini rejected the key. Use an API key from Google AI Studio (it starts with AIza), "
                             "not an access token or a Cloud service account key.")
        raise SystemExit(f"The agent stopped: {code or type(e).__name__} {msg}")
