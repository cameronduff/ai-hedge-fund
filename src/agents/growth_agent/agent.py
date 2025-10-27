import os

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.genai import types
from google.adk.models.lite_llm import LiteLlm

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

DEPLOYMENT = os.environ["AZURE_DEPLOYMENT_NAME"]  # e.g. "gpt-4o-mini"

# Growth Agent with tools for analyzing growth drivers and projecting future performance
growth_agent = LlmAgent(
    model=f"azure/{DEPLOYMENT}",
    name="growth_agent",
    instruction=GROWTH_AGENT_PROMPT,
    tools=[
        google_search,
        calculate_trend_slope,
        analyze_historical_growth,
        analyze_growth_valuation,
        analyze_margin_expansion,
        analyze_insider_activity,
        assess_financial_stability,
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.3,  # Moderate temperature for balanced growth analysis
    ),
    output_schema=GrowthAgentOutput,
    output_key="growth_agent_output",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)
