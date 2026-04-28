from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.warren_buffet_agent.prompt import WARREN_BUFFET_PROMPT

warren_buffet_agent = LlmAgent(
    name="warren_buffet_agent",
    model=settings.REASONING_MODEL,
    instruction=WARREN_BUFFET_PROMPT,
)
