from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.quants.valuations_agent.prompt import (
    VALUATIONS_PROMPT,
    VALUATIONS_FORMATTING_PROMPT,
)

from app.models.quants_models import Ticker, ValuationAgentOutput
from app.tools.yfinance_tools import (
    get_info_by_ticker,
    get_historical_data,
    get_balance_sheet_by_ticker,
)


def build_valuations_agent(ticker_name: str):

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
                multiplier=2.0,
            )
        ),
    )

    valuations_quant_agent = LlmAgent(
        name=f"valuations_raw_agent_{ticker_name}",
        model=settings.REASONING_MODEL,
        description="A mathematical appraiser that calculates intrinsic value and relative pricing multiples like P/E, P/B, and PEG to determine if a stock is trading at a discount.",
        instruction=VALUATIONS_PROMPT,
        planner=planner,
        tools=[
            get_info_by_ticker,
            get_historical_data,
            get_balance_sheet_by_ticker,
        ],
        generate_content_config=generate_content_config,
        input_schema=Ticker,
        output_key=f"temp:valuations_agent_raw_output_{ticker_name}",
    )

    valuations_formatter_agent = LlmAgent(
        name=f"valuations_formatter_agent_{ticker_name}",
        model=settings.FORMATTING_MODEL,
        instruction=VALUATIONS_FORMATTING_PROMPT,
        generate_content_config=generate_content_config,
        output_schema=ValuationAgentOutput,
        output_key=f"valuations_agent_output_{ticker_name}",
    )

    valuations_agent = SequentialAgent(
        name=f"valuations_agent_{ticker_name}",
        sub_agents=[
            valuations_quant_agent,
            valuations_formatter_agent,
        ],
    )

    return valuations_agent
