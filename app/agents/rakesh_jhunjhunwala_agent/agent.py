from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.rakesh_jhunjhunwala_agent.prompt import RAKESH_JHUNJHUNWALA_PROMPT

rakesh_jhunjhunwala_agent = LlmAgent(
    name="rakesh_jhunjhunwala_agent",
    model=settings.REASONING_MODEL,
    instruction=RAKESH_JHUNJHUNWALA_PROMPT,
)
