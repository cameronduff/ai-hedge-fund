import os

from google.adk.agents import LlmAgent
from google.genai import types
from google.adk.models.lite_llm import LiteLlm, LiteLLMClient

from src.agents.investors.michael_burry.prompt import MICHAEL_BURRY_PROMPT
from src.agents.investors.michael_burry.schema import MichaelBurrySignal
from src.tools.burry_analysis import (
    analyze_deep_value_metrics,
    analyze_balance_sheet_strength,
    analyze_insider_activity,
    analyze_contrarian_sentiment,
    calculate_burry_score,
)

DEPLOYMENT = os.environ["AZURE_DEPLOYMENT_NAME"]  # e.g. "gpt-4o-mini"

# 1) one-time setup
# model must be your Azure *deployment name*, prefixed with 'azure/'
azure_llm = LiteLlm(model=f"azure/{DEPLOYMENT}", llm_client=LiteLLMClient())

# 2) use it in your agents
# Michael Burry Agent with comprehensive deep value analysis tools
michael_burry_agent = LlmAgent(
    model=azure_llm,  # pass the instance, not a string
    name="michael_burry_agent",
    instruction=MICHAEL_BURRY_PROMPT,
    tools=[
        analyze_deep_value_metrics,
        analyze_balance_sheet_strength,
        analyze_insider_activity,
        analyze_contrarian_sentiment,
        calculate_burry_score,
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=1.0,  # Low temperature for analytical precision like Burry
    ),
    output_schema=MichaelBurrySignal,
    output_key="michael_burry_agent_output",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)
