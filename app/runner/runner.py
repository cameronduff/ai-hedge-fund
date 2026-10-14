from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import asyncio
from google.genai import types
from loguru import logger

try:
    from langfuse import propagate_attributes
    HAS_LANGFUSE = True
except ImportError:
    HAS_LANGFUSE = False


async def _run_stage_async(
    app_name: str,
    user_id: str,
    runner: Runner,
    session_service: InMemorySessionService,
    session_id: str,
    message: str,
    stage_name: str = "stage",
    metadata: dict | None = None,
) -> dict:
    content = types.Content(
        role="user",
        parts=[types.Part(text=message)]
    )

    context_manager = (
        propagate_attributes(
            trace_name=f"ai-hedge-fund-{stage_name}",
            session_id=session_id,
            user_id=user_id,
            tags=["ai-hedge-fund", stage_name],
            metadata=metadata or {},
        )
        if HAS_LANGFUSE
        else asyncio.nullcontext()
    )

    with context_manager:
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content,
        ):
            logger.info(f"  [{event.author}] is_final={event.is_final_response()} content={bool(event.content)}")
            if event.is_final_response() and event.content and event.content.parts:
                logger.info(f"  >> {event.content.parts[0].text.strip()[:150]}")

    final_session = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )
    logger.info(f"  State keys: {list(final_session.state.keys())}")
    return final_session.state


def run_stage(
    app_name: str,
    user_id: str,
    runner: Runner,
    session_service: InMemorySessionService,
    session_id: str,
    message: str,
    stage_name: str = "stage",
    metadata: dict | None = None,
) -> dict:
    return asyncio.run(
        _run_stage_async(
            app_name=app_name,
            user_id=user_id,
            runner=runner,
            session_service=session_service,
            session_id=session_id,
            message=message,
            stage_name=stage_name,
            metadata=metadata,
        )
    )