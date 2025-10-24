from google.adk.agents import LlmAgent
from google.adk.tools import google_search
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
        google_search,
        analyze_profitability_metrics,
        analyze_growth_metrics,
        analyze_financial_health,
        analyze_valuation_ratios,
        calculate_fundamental_score,
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1,  # Very low temperature for precise fundamental analysis
    ),
    output_schema=FundamentalsAgentOutput,
    output_key="fundamentals_agent_output",
)
