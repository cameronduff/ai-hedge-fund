from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.quants.fundamentals_agent.prompt import FUNDAMENTALS_PROMPT
from app.models.quants_models import Ticker, FundamentalsAgentOutput
from app.tools.yfinance_tools import (
    get_balance_sheet_by_ticker,
    get_quarterly_income_statement,
    get_info_by_ticker,
)


def build_fundamentals_agent(ticker_name: str) -> LlmAgent:
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
        )
    )

    target_instruction = (
        f"TARGET TICKER: You must strictly analyze Yahoo Finance ticker '{ticker_name}'. Do NOT analyze any other tickers.\n\n"
        + FUNDAMENTALS_PROMPT
    )

    fundamentals_agent = LlmAgent(
        name=f"fundamentals_agent_{t}",
        model=settings.QUANTS_MODEL,
        description="A rigorous accounting specialist that dissects balance sheets and income statements to verify financial health, debt levels, and operational efficiency.",
        instruction=target_instruction,
        planner=planner,
        tools=[
            get_balance_sheet_by_ticker,
            get_quarterly_income_statement,
            get_info_by_ticker,
        ],
        generate_content_config=generate_content_config,
        input_schema=Ticker,
        output_schema=FundamentalsAgentOutput,
        output_key=f"fundamentals_agent_output_{t}",
    )

    return fundamentals_agent

