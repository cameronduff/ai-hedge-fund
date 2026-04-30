from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.quants.technicals_agent.prompt import TECHNICALS_PROMPT

from app.models.quants_models import Ticker, TechnicalAgentOutput
from app.tools.yfinance_tools import get_historical_data, get_options_chain

planner = BuiltInPlanner(
    thinking_config=types.ThinkingConfig(
        include_thoughts=True,
        thinking_level=types.ThinkingLevel.HIGH,
    )
)

generate_content_config = types.GenerateContentConfig(
    temperature=0.2,
)

technicals_agent = LlmAgent(
    name="technicals_agent",
    model=settings.REASONING_MODEL,
    description="A pattern-recognition expert focused on price action, momentum indicators, and volume trends to identify market entry and exit signals.",
    instruction=TECHNICALS_PROMPT,
    # planner=planner,
    tools=[get_historical_data, get_options_chain],
    generate_content_config=generate_content_config,
    input_schema=Ticker,
    output_schema=TechnicalAgentOutput,
    output_key="technicals_agent_output",
)
