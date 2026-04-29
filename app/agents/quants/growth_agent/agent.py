from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.quants.growth_agent.prompt import GROWTH_PROMPT

from app.tools.yfinance_tools import (
    get_analyst_price_targets,
    get_info_by_ticker,
    get_calendar,
)

growth_agent = LlmAgent(
    name="growth_agent",
    model=settings.REASONING_MODEL,
    instruction=GROWTH_PROMPT,
    tools=[
        get_analyst_price_targets,
        get_info_by_ticker,
        get_calendar,
    ],
)
