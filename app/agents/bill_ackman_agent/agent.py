from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.bill_ackman_agent.prompt import BILL_ACKMAN_PROMPT

bill_ackman_agent = LlmAgent(
    name="bill_ackman_agent",
    model=settings.REASONING_MODEL,
    instruction=BILL_ACKMAN_PROMPT,
)
