from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.management.risk_manager_agent.prompt import RISK_MANAGER_PROMPT
from app.tools.trading212_tools import get_account_summary, fetch_all_open_positions
from app.tools.yfinance_tools import get_historical_data
from app.tools.calculation_tools import (
    calculate_position_size,
    calculate_remaining_cash,
    calculate_position_value,
    calculate_portfolio_concentration,
    calculate_annualised_volatility,
    calculate_unrealised_pnl,
)

risk_manager_agent = LlmAgent(
    name="risk_manager_agent",
    model=settings.REASONING_MODEL,
    instruction=RISK_MANAGER_PROMPT,
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_level=types.ThinkingLevel.HIGH,
        )
    ),
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1,
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                attempts=5,
                initial_delay=10.0,
                max_delay=360.0,
                multiplier=2.0,
            )
        ),
    ),
    tools=[
        get_account_summary, 
        fetch_all_open_positions, 
        get_historical_data,
        calculate_position_size,
        calculate_remaining_cash,
        calculate_position_value,
        calculate_portfolio_concentration,
        calculate_annualised_volatility,
        calculate_unrealised_pnl,
    ],
)
