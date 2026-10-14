from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.quants.valuations_agent.prompt import VALUATIONS_PROMPT
from app.models.quants_models import Ticker, ValuationAgentOutput
from app.tools.yfinance_tools import (
    get_info_by_ticker,
    get_historical_data,
    get_balance_sheet_by_ticker,
)


def build_valuations_agent(ticker_name: str) -> LlmAgent:
    t = ticker_name.replace(".", "_")
    planner = BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_level=types.ThinkingLevel.HIGH,
        )
    )

    generate_content_config = types.GenerateContentConfig(
        temperature=0.2,
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                attempts=5,
                initial_delay=10.0,
                max_delay=360.0,
                exp_base=2.0,
            )
        ),
    )

    target_instruction = (
        f"TARGET TICKER: You must strictly analyze Yahoo Finance ticker '{ticker_name}'. Do NOT analyze any other tickers.\n\n"
        + VALUATIONS_PROMPT
    )

    valuations_agent = LlmAgent(
        name=f"valuations_agent_{t}",
        model=settings.QUANTS_MODEL,
        description="A mathematical appraiser that calculates intrinsic value and relative pricing multiples like P/E, P/B, and PEG to determine if a stock is trading at a discount.",
        instruction=target_instruction,
        planner=planner,
        tools=[
            get_info_by_ticker,
            get_historical_data,
            get_balance_sheet_by_ticker,
        ],
        generate_content_config=generate_content_config,
        input_schema=Ticker,
        output_schema=ValuationAgentOutput,
        output_key=f"valuations_agent_output_{t}",
    )

    return valuations_agent

