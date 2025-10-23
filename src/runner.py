import asyncio
import json
import uuid
from google.adk.agents import BaseAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from loguru import logger


async def run_pipeline_async(pipeline: BaseAgent, app_name: str, query: str) -> dict:
    user_id = str(uuid.uuid4())
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=app_name, user_id=user_id)
    runner = Runner(app_name=app_name, agent=pipeline, session_service=session_service)

    new_message = types.Content(
        role="user",
        parts=[types.Part(text=query)],
    )

    final_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=new_message,
    ):
        if getattr(event, "is_final_response", lambda: False)():
            if event.content and event.content.parts:
                final_text = event.content.parts[0].text or final_text

    logger.success("Pipeline execution complete.")

    # Try to parse ProgrammeOutput from final event text
    try:
        payload = json.loads(final_text)
        if isinstance(payload, dict) and "output" in payload:
            return {"output": payload["output"]}
    except Exception:
        pass

    # Fallback to session state
    po = session.state.get("programme_output_consensus")
    if po:
        return {"output": po}

    logger.warning("No programme_output_consensus found in state or event.")
    return {"output": {}}


def run_pipeline(pipeline: BaseAgent, app_name: str, query: str) -> dict:
    return asyncio.run(run_pipeline_async(pipeline, app_name, query))
