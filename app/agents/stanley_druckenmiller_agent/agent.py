from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.stanley_druckenmiller_agent.prompt import STANLEY_DRUCKENMILLER_PROMPT

stanley_druckenmiller_agent = LlmAgent(
    name="stanley_druckenmiller_agent",
    model=settings.REASONING_MODEL,
    instruction=STANLEY_DRUCKENMILLER_PROMPT,
)
