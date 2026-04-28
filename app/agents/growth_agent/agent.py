from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.growth_agent.prompt import GROWTH_PROMPT

growth_agent = LlmAgent(
    name="growth_agent",
    model=settings.REASONING_MODEL,
    instruction=GROWTH_PROMPT,
)
