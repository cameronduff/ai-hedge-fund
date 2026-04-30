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

planner = BuiltInPlanner(
    thinking_config=types.ThinkingConfig(
        include_thoughts=True,
        thinking_level=types.ThinkingLevel.HIGH,
    )
)

generate_content_config = types.GenerateContentConfig(
    temperature=0.2,
)

valuations_agent = LlmAgent(
    name="valuations_agent",
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
    output_schema=ValuationAgentOutput,
    output_key="valuations_agent_output",
)
