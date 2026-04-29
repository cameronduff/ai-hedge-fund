from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.management.portfolio_manager_agent.prompt import (
    PORTFOLIO_MANAGER_PROMPT,
)

portfolio_manager_agent = LlmAgent(
    name="portfolio_manager_agent",
    model=settings.REASONING_MODEL,
    instruction=PORTFOLIO_MANAGER_PROMPT,
)
