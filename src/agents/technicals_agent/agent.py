from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.genai import types

from dotenv import load_dotenv

from src.agents.technicals_agent.prompt import TECHNICAL_AGENT_PROMPT
from src.agents.technicals_agent.schema import TechnicalAgentOutput
from src.tools.technical_analysis import (
    calculate_trend_indicators,
    calculate_mean_reversion_indicators,
    calculate_momentum_indicators,
    calculate_volatility_indicators,
    calculate_statistical_indicators,
    combine_technical_signals,
)

load_dotenv()


# Technicals Agent with a suite of technical analysis tools
technical_agent = LlmAgent(
    model="gemini-2.5-pro",
    name="technical_agent",
    instruction=TECHNICAL_AGENT_PROMPT,
    tools=[
        google_search,
        calculate_trend_indicators,
        calculate_mean_reversion_indicators,
        calculate_momentum_indicators,
        calculate_volatility_indicators,
        calculate_statistical_indicators,
        combine_technical_signals,
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.2,  # Low temperature for precise technical analysis
    ),
    output_schema=TechnicalAgentOutput,
)
