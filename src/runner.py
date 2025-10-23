# runner.py (adapt your existing functions)
import asyncio
import json
import uuid
from google.adk.agents import BaseAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from loguru import logger


async def run_pipeline_async(
    pipeline: BaseAgent,
    app_name: str,
    task: str,
    *,
    account_ctx: dict | None = None,
    pies_ctx: dict | None = None,
    task_cfg: dict | None = None,  # optional third JSON (constraints/prefs/schema)
) -> dict:
    user_id = str(uuid.uuid4())
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=app_name, user_id=user_id)
    runner = Runner(app_name=app_name, agent=pipeline, session_service=session_service)

    parts: list[types.Part] = []

    if account_ctx:
        parts.append(types.Part(text="BEGIN_JSON t212_account"))
        parts.append(types.Part(text=json.dumps(account_ctx, ensure_ascii=False)))
        parts.append(types.Part(text="END_JSON t212_account"))

    if pies_ctx:
        parts.append(types.Part(text="BEGIN_JSON t212_pies"))
        parts.append(types.Part(text=json.dumps(pies_ctx, ensure_ascii=False)))
        parts.append(types.Part(text="END_JSON t212_pies"))

    # Put the actual research/execution request last, with strict output rules
    # You can either pass this as JSON or free text; JSON is cleaner for your collectors.
    task_envelope = {
        "schema_version": "1.0",
        "task": task,
        "output_contract": {
            "recommendations": [
                {
                    "ticker": "string",
                    "exchange": "string",
                    "weight": 0.10,
                    "reason": "string",
                }
            ],
            "actions": [
                {"type": "BUY|SELL", "ticker": "string", "qty": 0.0, "why": "string"}
            ],
            "notes": "string",
        },
        "constraints": (task_cfg or {}),
        "instructions": [
            "Use t212_account and t212_pies JSON above as the single source of portfolio truth.",
            "Prefer instruments available on Trading 212; specify exchange explicitly.",
            "Return ONLY a single JSON object conforming to output_contract.",
        ],
    }
    parts.append(types.Part(text="BEGIN_JSON task"))
    parts.append(types.Part(text=json.dumps(task_envelope, ensure_ascii=False)))
    parts.append(types.Part(text="END_JSON task"))

    new_message = types.Content(role="user", parts=parts)

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

    # Try to parse final JSON
    try:
        payload = json.loads(final_text)
        if isinstance(payload, dict) and (
            "recommendations" in payload or "actions" in payload
        ):
            return {"output": payload}
    except Exception:
        pass

    # Fallback to session state (unchanged from your code)
    po = session.state.get("programme_output_consensus")
    if po:
        return {"output": po}

    logger.warning("No structured output found.")
    return {"output": {}}


def run_pipeline(
    pipeline: BaseAgent,
    app_name: str,
    task: str,
    *,
    account_ctx: dict | None = None,
    pies_ctx: dict | None = None,
    task_cfg: dict | None = None,
) -> dict:
    return asyncio.run(
        run_pipeline_async(
            pipeline,
            app_name,
            task,
            account_ctx=account_ctx,
            pies_ctx=pies_ctx,
            task_cfg=task_cfg,
        )
    )
