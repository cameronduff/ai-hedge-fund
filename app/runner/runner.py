from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import asyncio
from google.genai import types
from loguru import logger

def run_stage(app_name: str, user_id: str, runner: Runner, session_service: InMemorySessionService, session_id: str, message: str) -> dict:
    content = types.Content(
        role="user",
        parts=[types.Part(text=message)]
    )
    events = runner.run(
        user_id=user_id,
        session_id=session_id,
        new_message=content,
    )
    for event in events:
        logger.info(f"  [{event.author}] is_final={event.is_final_response()} content={bool(event.content)}")
        if event.is_final_response() and event.content:
            logger.info(f"  >> {event.content.parts[0].text.strip()[:150]}")

    final_session = asyncio.run(
        session_service.get_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
        )
    )
    logger.info(f"  State keys: {list(final_session.state.keys())}")
    return final_session.state