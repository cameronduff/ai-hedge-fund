from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.quants.fundamentals_agent.prompt import FUNDAMENTALS_PROMPT

from app.tools.yfinance_tools import (
    get_balance_sheet_by_ticker,
    get_quarterly_income_statement,
    get_info_by_ticker,
)

fundamentals_agent = LlmAgent(
    name="fundamentals_agent",
    model=settings.REASONING_MODEL,
    instruction=FUNDAMENTALS_PROMPT,
    tools=[
        get_balance_sheet_by_ticker,
        get_quarterly_income_statement,
        get_info_by_ticker,
    ],
)
