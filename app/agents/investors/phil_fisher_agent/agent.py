from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.investors.phil_fisher_agent.prompt import PHIL_FISHER_PROMPT

phil_fisher_agent = LlmAgent(
    name="phil_fisher_agent",
    model=settings.REASONING_MODEL,
    instruction=PHIL_FISHER_PROMPT,
)
