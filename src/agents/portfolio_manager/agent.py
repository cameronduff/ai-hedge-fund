from google.adk.agents import LlmAgent
from google.genai import types

from src.agents.portfolio_manager.prompt import PORTFOLIO_MANAGER_PROMPT
from src.agents.portfolio_manager.schema import PortfolioManagerOutput
from src.tools.portfolio_management import (
    analyze_signal_consensus,
    calculate_position_size,
    assess_portfolio_risk,
    optimize_trade_timing,
)

# Portfolio Manager Agent with advanced portfolio management and risk assessment tools
portfolio_manager_agent = LlmAgent(
    model="gemini-2.5-pro",
    name="portfolio_manager_agent",
    instruction=PORTFOLIO_MANAGER_PROMPT,
    tools=[
        analyze_signal_consensus,
        calculate_position_size,
        assess_portfolio_risk,
        optimize_trade_timing,
    ],
    generation_config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=PortfolioManagerOutput.model_json_schema(),
        temperature=0.2,  # Low temperature for disciplined, systematic portfolio management
    ),
)
