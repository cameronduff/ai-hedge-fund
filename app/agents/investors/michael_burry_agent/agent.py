from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.investors.michael_burry_agent.prompt import MICHAEL_BURRY_PROMPT

michael_burry_agent = LlmAgent(
    name="michael_burry_agent",
    model=settings.REASONING_MODEL,
    instruction=MICHAEL_BURRY_PROMPT,
)
