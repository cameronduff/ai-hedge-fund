import os

from google.adk.agents import LlmAgent
from google.genai import types
from google.adk.models.lite_llm import LiteLlm, LiteLLMClient

from src.agents.investors.mohnish_pabrai.prompt import MOHNISH_PABRAI_PROMPT
from src.agents.investors.mohnish_pabrai.schema import MohnishPabraiSignal
from src.tools.pabrai_analysis import (
    analyze_downside_protection,
    analyze_pabrai_valuation,
    analyze_double_potential,
    analyze_business_simplicity,
    calculate_pabrai_score,
)

DEPLOYMENT = os.environ["AZURE_DEPLOYMENT_NAME"]  # e.g. "gpt-4o-mini"

# 1) one-time setup
# model must be your Azure *deployment name*, prefixed with 'azure/'
azure_llm = LiteLlm(model=f"azure/{DEPLOYMENT}", llm_client=LiteLLMClient())

# 2) use it in your agents
# Mohnish Pabrai Agent with "heads I win, tails I don't lose much" analysis tools
mohnish_pabrai_agent = LlmAgent(
    model=azure_llm,  # pass the instance, not a string
    name="mohnish_pabrai_agent",
    instruction=MOHNISH_PABRAI_PROMPT,
    tools=[
        analyze_downside_protection,
        analyze_pabrai_valuation,
        analyze_double_potential,
        analyze_business_simplicity,
        calculate_pabrai_score,
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.2,  # Low temperature for systematic, checklist-driven approach
    ),
    output_schema=MohnishPabraiSignal,
    output_key="mohnish_pabrai_agent_output",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)
