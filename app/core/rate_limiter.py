import asyncio
import time
from typing import Optional

from google.adk.plugins import BasePlugin
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from loguru import logger

from app.core.config import settings


class RateLimitPacerPlugin(BasePlugin):
    """
    Enforces a strict minimum time interval between LLM calls to stay
    comfortably under Gemini API free-tier quotas (15 RPM max).
    """

    def __init__(
        self,
        name: str = "rate_limit_pacer_plugin",
        min_interval_seconds: float | None = None,
    ):
        super().__init__(name=name)
        self.min_interval_seconds = (
            min_interval_seconds
            if min_interval_seconds is not None
            else settings.RATE_LIMIT_DELAY_SECONDS
        )
        self.last_call_timestamp: float = 0.0
        self.call_count: int = 0
        self.total_pacing_seconds: float = 0.0

    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> Optional[LlmResponse]:
        self.call_count += 1
        now = time.time()
        elapsed = now - self.last_call_timestamp
        if self.last_call_timestamp > 0 and elapsed < self.min_interval_seconds:
            sleep_needed = self.min_interval_seconds - elapsed
            self.total_pacing_seconds += sleep_needed
            logger.info(
                f"[RateLimiter] Call #{self.call_count} | Pacing request: sleeping {sleep_needed:.2f}s to enforce ≤ 13.3 RPM"
            )
            await asyncio.sleep(sleep_needed)
        else:
            logger.info(f"[RateLimiter] Call #{self.call_count} | Executing LLM request directly")

        self.last_call_timestamp = time.time()
        return None

    async def on_model_error_callback(
        self,
        *,
        callback_context: CallbackContext,
        llm_request: LlmRequest,
        error: Exception,
    ) -> Optional[LlmResponse]:
        err_msg = str(error)
        if any(code in err_msg for code in ["503", "429", "UNAVAILABLE", "ResourceExhausted"]):
            logger.warning(
                f"[RateLimiter] Transient model error encountered: {error}. Backing off 15s and retrying..."
            )
            await asyncio.sleep(15.0)
            agent = callback_context.invocation_context.agent
            if hasattr(agent, "model"):
                try:
                    async for resp in agent.model.generate_content_async(llm_request):
                        logger.info(f"[RateLimiter] Retry succeeded after transient error!")
                        self.last_call_timestamp = time.time()
                        return resp
                except Exception as retry_err:
                    logger.error(f"[RateLimiter] Retry after transient error failed: {retry_err}")
        return None

