from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.technicals_agent.prompt import TECHNICALS_PROMPT

technicals_agent = LlmAgent(
    name="technicals_agent",
    model=settings.REASONING_MODEL,
    instruction=TECHNICALS_PROMPT,
)
