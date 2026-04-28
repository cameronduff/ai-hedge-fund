from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.ben_graham_agent.prompt import BEN_GRAHAM_PROMPT

ben_graham_agent = LlmAgent(
    name="ben_graham_agent",
    model=settings.REASONING_MODEL,
    instruction=BEN_GRAHAM_PROMPT,
)
