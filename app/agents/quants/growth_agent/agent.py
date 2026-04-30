from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.quants.growth_agent.prompt import GROWTH_PROMPT

from app.models.quants_models import Ticker, GrowthAgentOutput
from app.tools.yfinance_tools import (
    get_analyst_price_targets,
    get_info_by_ticker,
    get_calendar,
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

growth_agent = LlmAgent(
    name="growth_agent",
    model=settings.REASONING_MODEL,
    description="A forward-looking strategist that analyzes revenue expansion, Total Addressable Market (TAM), and analyst price targets to project future earnings trajectory.",
    instruction=GROWTH_PROMPT,
    # planner=planner,
    tools=[
        get_analyst_price_targets,
        get_info_by_ticker,
        get_calendar,
    ],
    generate_content_config=generate_content_config,
    input_schema=Ticker,
    # output_schema=GrowthAgentOutput,
    output_key="growth_agent_output",
)
