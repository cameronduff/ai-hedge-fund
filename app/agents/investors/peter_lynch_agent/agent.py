from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.investors.peter_lynch_agent.prompt import PETER_LYNCH_PROMPT

peter_lynch_agent = LlmAgent(
    name="peter_lynch_agent",
    model=settings.REASONING_MODEL,
    instruction=PETER_LYNCH_PROMPT,
)
