from google.adk.agents import LlmAgent
from google.genai import types

from src.agents.growth_agent.prompt import GROWTH_AGENT_PROMPT
from src.agents.growth_agent.schema import GrowthAgentOutput
from src.tools.growth_analysis import (
    calculate_trend_slope,
    analyze_historical_growth,
    analyze_growth_valuation,
    analyze_margin_expansion,
    analyze_insider_activity,
    assess_financial_stability,
)

# Growth Agent with comprehensive growth analysis tools
growth_agent = LlmAgent(
    model="gemini-2.5-pro",
    name="growth_agent",
    instruction=GROWTH_AGENT_PROMPT,
    tools=[
        calculate_trend_slope,
        analyze_historical_growth,
        analyze_growth_valuation,
        analyze_margin_expansion,
        analyze_insider_activity,
        assess_financial_stability,
    ],
    generation_config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=GrowthAgentOutput.model_json_schema(),
        temperature=0.1,  # Very low temperature for precise growth analysis
    ),
)
