from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.quants.technicals_agent.prompt import TECHNICALS_PROMPT
from app.models.quants_models import Ticker, TechnicalAgentOutput
from app.tools.yfinance_tools import get_historical_data, get_options_chain


def build_technicals_agent(ticker_name: str) -> LlmAgent:
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
        + TECHNICALS_PROMPT
    )

    technicals_agent = LlmAgent(
        name=f"technicals_agent_{t}",
        model=settings.QUANTS_MODEL,
        description="A pattern-recognition expert focused on price action, momentum indicators, and volume trends to identify market entry and exit signals.",
        instruction=target_instruction,
        planner=planner,
        tools=[get_historical_data, get_options_chain],
        generate_content_config=generate_content_config,
        input_schema=Ticker,
        output_schema=TechnicalAgentOutput,
        output_key=f"technicals_agent_output_{t}",
    )

    return technicals_agent

