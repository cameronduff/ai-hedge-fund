from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.charlie_munger_agent.prompt import CHARLIE_MUNGER_PROMPT

charlie_munger_agent = LlmAgent(
    name="charlie_munger_agent",
    model=settings.REASONING_MODEL,
    instruction=CHARLIE_MUNGER_PROMPT,
)
