from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.aswath_damodaran_agent.prompt import ASWATH_DAMODARAN_PROMPT

aswath_damodaran_agent = LlmAgent(
    name="aswath_damodaran_agent",
    model=settings.REASONING_MODEL,
    instruction=ASWATH_DAMODARAN_PROMPT,
)
