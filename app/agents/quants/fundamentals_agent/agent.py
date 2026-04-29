from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.quants.fundamentals_agent.prompt import FUNDAMENTALS_PROMPT

fundamentals_agent = LlmAgent(
    name="fundamentals_agent",
    model=settings.REASONING_MODEL,
    instruction=FUNDAMENTALS_PROMPT,
)
