import os

from google.adk.agents import LlmAgent
from google.genai import types
from google.adk.models.lite_llm import LiteLlm, LiteLLMClient

from src.agents.investors.warren_buffett.prompt import WARREN_BUFFETT_PROMPT
from src.agents.investors.warren_buffett.schema import WarrenBuffettSignal
from src.tools.buffett_analysis import (
    analyze_business_quality,
    analyze_competitive_moat,
    analyze_management_excellence,
    analyze_earnings_consistency,
    calculate_buffett_score,
)

DEPLOYMENT = os.environ["AZURE_DEPLOYMENT_NAME"]  # e.g. "gpt-4o-mini"

# 1) one-time setup
# model must be your Azure *deployment name*, prefixed with 'azure/'
azure_llm = LiteLlm(model=f"azure/{DEPLOYMENT}", llm_client=LiteLLMClient())

# 2) use it in your agents
# Warren Buffett Agent with value investing and business quality analysis tools
warren_buffett_agent = LlmAgent(
    model=azure_llm,  # pass the instance, not a string
    name="warren_buffett_agent",
    instruction=WARREN_BUFFETT_PROMPT,
    tools=[
        analyze_business_quality,
        analyze_competitive_moat,
        analyze_management_excellence,
        analyze_earnings_consistency,
        calculate_buffett_score,
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=1.0,  # Very low temperature for Buffett's disciplined, analytical approach
    ),
    output_schema=WarrenBuffettSignal,
    output_key="warren_buffett_agent_output",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)
