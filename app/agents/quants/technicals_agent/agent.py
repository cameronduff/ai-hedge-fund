from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.quants.technicals_agent.prompt import TECHNICALS_PROMPT

from app.tools.yfinance_tools import get_historical_data, get_options_chain

technicals_agent = LlmAgent(
    name="technicals_agent",
    model=settings.REASONING_MODEL,
    instruction=TECHNICALS_PROMPT,
    tools=[get_historical_data, get_options_chain],
)
