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
        self._lock: asyncio.Lock | None = None

    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> Optional[LlmResponse]:
        if self._lock is None:
            self._lock = asyncio.Lock()

        async with self._lock:
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
            backoff_delays = [15.0, 30.0, 60.0]
            invocation_context = getattr(callback_context, "_invocation_context", None)
            agent = getattr(invocation_context, "agent", None) if invocation_context else None

            # Fallback to QUANTS_MODEL if 429 quota exhaustion hit on higher tier model
            if ("ResourceExhausted" in err_msg or "429" in err_msg):
                fallback_model = settings.QUANTS_MODEL
                if getattr(llm_request, "model", None) != fallback_model:
                    logger.warning(
                        f"[RateLimiter] Quota exhausted on {getattr(llm_request, 'model', 'unknown')}. "
                        f"Falling back agent '{getattr(agent, 'name', 'unknown')}' to {fallback_model}"
                    )
                    llm_request.model = fallback_model
                    if agent and hasattr(agent, "model"):
                        agent.model = fallback_model

            for attempt, delay in enumerate(backoff_delays, 1):
                logger.warning(
                    f"[RateLimiter] Model error (attempt {attempt}/{len(backoff_delays)}): {error}. "
                    f"Backing off {delay}s before retry..."
                )
                await asyncio.sleep(delay)

                try:
                    llm = getattr(agent, "canonical_model", None) if agent else None
                    if not llm:
                        from google.adk.models.google_llm import Gemini
                        llm = Gemini(model=llm_request.model)

                    async for resp in llm.generate_content_async(llm_request):
                        logger.info(f"[RateLimiter] Retry succeeded on attempt {attempt}!")
                        self.last_call_timestamp = time.time()
                        return resp
                except Exception as retry_err:
                    logger.error(f"[RateLimiter] Retry attempt {attempt} failed: {retry_err}")
                    err_msg = str(retry_err)
        return None


