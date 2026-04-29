from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.investors.monish_pabrai_agent.prompt import MONISH_PABRAI_PROMPT

monish_pabrai_agent = LlmAgent(
    name="monish_pabrai_agent",
    model=settings.REASONING_MODEL,
    instruction=MONISH_PABRAI_PROMPT,
)
