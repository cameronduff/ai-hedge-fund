from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.risk_manager_agent.prompt import RISK_MANAGER_PROMPT

risk_manager_agent = LlmAgent(
    name="risk_manager_agent",
    model=settings.REASONING_MODEL,
    instruction=RISK_MANAGER_PROMPT,
)
