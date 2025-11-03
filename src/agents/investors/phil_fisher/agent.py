import os

from google.adk.agents import LlmAgent
from google.genai import types
from google.adk.models.lite_llm import LiteLlm, LiteLLMClient

from src.agents.investors.phil_fisher.prompt import PHIL_FISHER_PROMPT
from src.agents.investors.phil_fisher.schema import PhilFisherSignal
from src.tools.fisher_analysis import (
    analyze_growth_quality_metrics,
    analyze_management_excellence,
    analyze_profit_margins_stability,
    analyze_competitive_position,
    calculate_fisher_score,
)

DEPLOYMENT = os.environ["AZURE_DEPLOYMENT_NAME"]  # e.g. "gpt-4o-mini"

# 1) one-time setup
# model must be your Azure *deployment name*, prefixed with 'azure/'
azure_llm = LiteLlm(model=f"azure/{DEPLOYMENT}", llm_client=LiteLLMClient())

# 2) use it in your agents
# Phil Fisher Agent with long-term growth and management excellence analysis tools
phil_fisher_agent = LlmAgent(
    model=azure_llm,  # pass the instance, not a string
    name="phil_fisher_agent",
    instruction=PHIL_FISHER_PROMPT,
    tools=[
        analyze_growth_quality_metrics,
        analyze_management_excellence,
        analyze_profit_margins_stability,
        analyze_competitive_position,
        calculate_fisher_score,
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.2,  # Low temperature for Fisher's methodical, analytical approach
    ),
    output_schema=PhilFisherSignal,
    output_key="phil_fisher_agent_output",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)
