from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.quants.fundamentals_agent.prompt import (
    FUNDAMENTALS_PROMPT,
    FUNDAMENTALS_FORMATTING_PROMPT,
)

from app.models.quants_models import Ticker, FundamentalsAgentOutput
from app.tools.yfinance_tools import (
    get_balance_sheet_by_ticker,
    get_quarterly_income_statement,
    get_info_by_ticker,
)


def build_fundamentals_agent(ticker_name: str):

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
        )
    )

    fundamentals_quant_agent = LlmAgent(
        name=f"fundamentals_raw_agent_{ticker_name}",
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
        output_key=f"temp:fundamentals_agent_raw_output_{ticker_name}",
    )

    fundamentals_formatter_agent = LlmAgent(
        name=f"fundamentals_formatter_agent_{ticker_name}",
        model=settings.FORMATTING_MODEL,
        instruction=FUNDAMENTALS_FORMATTING_PROMPT,
        generate_content_config=generate_content_config,
        output_schema=FundamentalsAgentOutput,
        output_key=f"fundamentals_agent_output_{ticker_name}",
    )

    fundamentals_agent = SequentialAgent(
        name=f"fundamentals_agent_{ticker_name}",
        sub_agents=[fundamentals_quant_agent, fundamentals_formatter_agent],
    )

    return fundamentals_agent
