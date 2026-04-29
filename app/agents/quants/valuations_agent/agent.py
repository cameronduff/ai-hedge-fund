from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.quants.valuations_agent.prompt import VALUATIONS_PROMPT

from app.tools.yfinance_tools import (
    get_info_by_ticker,
    get_historical_data,
    get_balance_sheet_by_ticker,
)

valuations_agent = LlmAgent(
    name="valuations_agent",
    model=settings.REASONING_MODEL,
    instruction=VALUATIONS_PROMPT,
    tools=[
        get_info_by_ticker,
        get_historical_data,
        get_balance_sheet_by_ticker,
    ],
)
