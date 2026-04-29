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

planner = BuiltInPlanner(
    thinking_config=types.ThinkingConfig(
        include_thoughts=True,
        thinking_budget=settings.LOW_THINKING_BUDGET,
        thinking_level=types.ThinkingLevel.HIGH,
    )
)

generate_content_config = types.GenerateContentConfig(
    temperature=0.2,
)

fundamentals_agent = LlmAgent(
    name="fundamentals_agent",
    model=settings.REASONING_MODEL,
    description="A rigorous accounting specialist that dissects balance sheets and income statements to verify financial health, debt levels, and operational efficiency.",
    instruction=FUNDAMENTALS_PROMPT,
    planner=planner,
    tools=[
        get_balance_sheet_by_ticker,
        get_quarterly_income_statement,
        get_info_by_ticker,
    ],
    generate_content_config=generate_content_config,
    input_schema=Ticker,
    output_schema=FundamentalsAgentOutput,
    output_key="fundamentals_agent_output",
)
