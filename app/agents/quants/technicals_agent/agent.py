from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.quants.technicals_agent.prompt import (
    TECHNICALS_PROMPT,
    TECHNICALS_FORMATTING_PROMPT,
)

from app.models.quants_models import Ticker, TechnicalAgentOutput
from app.tools.yfinance_tools import get_historical_data, get_options_chain


def build_technicals_agent(ticker_name: str):

    planner = BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_level=types.ThinkingLevel.HIGH,
        )
    )

    generate_content_config = types.GenerateContentConfig(
        temperature=0.2,
    )

    technicals_quant_agent = LlmAgent(
        name=f"technicals_raw_agent_{ticker_name}",
        model=settings.REASONING_MODEL,
        description="A pattern-recognition expert focused on price action, momentum indicators, and volume trends to identify market entry and exit signals.",
        instruction=TECHNICALS_PROMPT,
        planner=planner,
        tools=[get_historical_data, get_options_chain],
        generate_content_config=generate_content_config,
        input_schema=Ticker,
        output_key=f"temp:technicals_agent_raw_output_{ticker_name}",
    )

    technicals_formatter_agent = LlmAgent(
        name=f"technicals_formatter_agent_{ticker_name}",
        model=settings.REASONING_MODEL,
        instruction=TECHNICALS_FORMATTING_PROMPT,
        output_schema=TechnicalAgentOutput,
        output_key=f"technicals_agent_output_{ticker_name}",
    )

    technicals_agent = SequentialAgent(
        name=f"technicals_agent_{ticker_name}",
        sub_agents=[
            technicals_quant_agent,
            technicals_formatter_agent,
        ],
    )

    return technicals_agent
