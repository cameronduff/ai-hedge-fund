from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.investors.cathie_wood_agent.prompt import CATHIE_WOOD_PROMPT

cathie_wood_agent = LlmAgent(
    name="cathie_wood_agent",
    model=settings.REASONING_MODEL,
    instruction=CATHIE_WOOD_PROMPT,
)
