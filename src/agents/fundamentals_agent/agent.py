from google.adk.agents import LlmAgent
from google.genai import types

from src.agents.fundamentals_agent.prompt import FUNDAMENTALS_AGENT_PROMPT
from src.agents.fundamentals_agent.schema import FundamentalsAgentOutput
from src.tools.fundamental_analysis import (
    analyze_profitability_metrics,
    analyze_growth_metrics,
    analyze_financial_health,
    analyze_valuation_ratios,
    calculate_fundamental_score,
)

# Fundamentals Agent with comprehensive financial analysis tools
fundamentals_agent = LlmAgent(
    model="gemini-2.5-pro",
    name="fundamentals_agent",
    instruction=FUNDAMENTALS_AGENT_PROMPT,
    tools=[
        analyze_profitability_metrics,
        analyze_growth_metrics,
        analyze_financial_health,
        analyze_valuation_ratios,
        calculate_fundamental_score,
    ],
    generation_config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=FundamentalsAgentOutput.model_json_schema(),
        temperature=0.1,  # Very low temperature for precise fundamental analysis
    ),
)
