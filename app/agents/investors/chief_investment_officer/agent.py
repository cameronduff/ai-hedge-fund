from google.adk.agents import ParallelAgent, SequentialAgent, LlmAgent

from app.core.config import settings
from app.agents.investors.chief_investment_officer.prompt import (
    CHIEF_INVESTMENT_OFFICER_PROMPT,
)

chief_investment_officer_agent = LlmAgent(
    "chief_investment_officer_agent",
    model=settings.REASONING_MODEL,
    instruction=CHIEF_INVESTMENT_OFFICER_PROMPT,
)
