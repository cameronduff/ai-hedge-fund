from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.management.chief_of_staff_agent.prompt import (
    CHIEF_OF_STAFF_PROMPT,
)

chief_of_staff_agent = LlmAgent(
    name="chief_of_staff_agent",
    model=settings.REASONING_MODEL,
    instruction=CHIEF_OF_STAFF_PROMPT,
)
