from google.adk.agents import LlmAgent
from google.genai import types

from dotenv import load_dotenv

from src.agents.technicals_agent.prompt import TECHNICALS_AGENT_PROMPT
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


technical_agent = LlmAgent(
    model="gemini-2.0-flash-exp",
    name="technical_analysis_agent",
    instruction=TECHNICALS_AGENT_PROMPT,
    tools=[
        calculate_trend_indicators,
        calculate_mean_reversion_indicators,
        calculate_momentum_indicators,
        calculate_volatility_indicators,
        calculate_statistical_indicators,
        combine_technical_signals,
    ],
    response_config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=TechnicalAgentOutput.model_json_schema(),
        temperature=0.1,
    ),
)
