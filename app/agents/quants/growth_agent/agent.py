from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.quants.growth_agent.prompt import (
    GROWTH_PROMPT,
    GROWTH_FORMATTING_PROMPT,
)

from app.models.quants_models import Ticker, GrowthAgentOutput
from app.tools.yfinance_tools import (
    get_analyst_price_targets,
    get_info_by_ticker,
    get_calendar,
)


def build_growth_agent(ticker_name: str):

    planner = BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_level=types.ThinkingLevel.HIGH,
        )
    )

    generate_content_config = types.GenerateContentConfig(
        temperature=0.2,
    )

    growth_quant_agent = LlmAgent(
        name=f"growth_agent_{ticker_name}",
        model=settings.REASONING_MODEL,
        description="A forward-looking strategist that analyzes revenue expansion, Total Addressable Market (TAM), and analyst price targets to project future earnings trajectory.",
        instruction=GROWTH_PROMPT,
        planner=planner,
        tools=[
            get_analyst_price_targets,
            get_info_by_ticker,
            get_calendar,
        ],
        generate_content_config=generate_content_config,
        input_schema=Ticker,
        output_key=f"temp:growth_agent_raw_output_{ticker_name}",
    )

    growth_formatter_agent = LlmAgent(
        name=f"growth_formatter_agent_{ticker_name}",
        model=settings.REASONING_MODEL,
        instruction=GROWTH_FORMATTING_PROMPT,
        output_schema=GrowthAgentOutput,
        output_key=f"growth_agent_output_{ticker_name}",
    )

    growth_agent = SequentialAgent(
        name=f"growth_agent_{ticker_name}",
        sub_agents=[
            growth_quant_agent,
            growth_formatter_agent,
        ],
    )

    return growth_agent
