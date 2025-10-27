import os

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.genai import types
from google.adk.models.lite_llm import LiteLlm

from src.agents.fundamentals_agent.prompt import FUNDAMENTALS_AGENT_PROMPT
from src.agents.fundamentals_agent.schema import FundamentalsAgentOutput
from src.tools.fundamental_analysis import (
    analyze_profitability_metrics,
    analyze_growth_metrics,
    analyze_financial_health,
    analyze_valuation_ratios,
    calculate_fundamental_score,
)

DEPLOYMENT = os.environ["AZURE_DEPLOYMENT_NAME"]  # e.g. "gpt-4o-mini"

# Fundamentals Agent with comprehensive financial analysis tools
fundamentals_agent = LlmAgent(
    model=f"azure/{DEPLOYMENT}",
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
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)
