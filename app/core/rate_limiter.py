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

    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> Optional[LlmResponse]:
        now = time.time()
        elapsed = now - self.last_call_timestamp
        if self.last_call_timestamp > 0 and elapsed < self.min_interval_seconds:
            sleep_needed = self.min_interval_seconds - elapsed
            logger.info(
                f"[RateLimiter] Pacing LLM request: sleeping {sleep_needed:.2f}s to enforce ≤ 13.3 RPM"
            )
            await asyncio.sleep(sleep_needed)

        self.last_call_timestamp = time.time()
        return None
