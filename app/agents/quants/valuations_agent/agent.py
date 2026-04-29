from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.quants.valuations_agent.prompt import VALUATIONS_PROMPT

valuations_agent = LlmAgent(
    name="valuations_agent",
    model=settings.REASONING_MODEL,
    instruction=VALUATIONS_PROMPT,
)
