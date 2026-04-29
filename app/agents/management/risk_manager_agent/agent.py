from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.management.risk_manager_agent.prompt import RISK_MANAGER_PROMPT
from app.tools.trading212_tools import get_account_summary, fetch_all_open_positions
from app.tools.yfinance_tools import get_historical_data

risk_manager_agent = LlmAgent(
    name="risk_manager_agent",
    model=settings.REASONING_MODEL,
    instruction=RISK_MANAGER_PROMPT,
    tools=[get_account_summary, fetch_all_open_positions, get_historical_data],
)
