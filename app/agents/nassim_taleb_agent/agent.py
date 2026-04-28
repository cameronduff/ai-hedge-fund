from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.nassim_taleb_agent.prompt import NASSIM_TALEB_PROMPT

nassim_taleb_agent = LlmAgent(
    name="nassim_taleb_agent",
    model=settings.REASONING_MODEL,
    instruction=NASSIM_TALEB_PROMPT,
)
