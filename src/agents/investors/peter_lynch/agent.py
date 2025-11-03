import os

from google.adk.agents import LlmAgent
from google.genai import types
from google.adk.models.lite_llm import LiteLlm, LiteLLMClient

from src.agents.investors.peter_lynch.prompt import PETER_LYNCH_PROMPT
from src.agents.investors.peter_lynch.schema import PeterLynchSignal
from src.tools.lynch_analysis import (
    analyze_garp_metrics,
    analyze_business_simplicity,
    analyze_ten_bagger_potential,
    analyze_lynch_sentiment,
    calculate_lynch_score,
)

DEPLOYMENT = os.environ["AZURE_DEPLOYMENT_NAME"]  # e.g. "gpt-4o-mini"

# 1) one-time setup
# model must be your Azure *deployment name*, prefixed with 'azure/'
azure_llm = LiteLlm(model=f"azure/{DEPLOYMENT}", llm_client=LiteLLMClient())

# 2) use it in your agents
# Peter Lynch Agent with Growth at Reasonable Price (GARP) analysis tools
peter_lynch_agent = LlmAgent(
    model=azure_llm,  # pass the instance, not a string
    name="peter_lynch_agent",
    instruction=PETER_LYNCH_PROMPT,
    tools=[
        analyze_garp_metrics,
        analyze_business_simplicity,
        analyze_ten_bagger_potential,
        analyze_lynch_sentiment,
        calculate_lynch_score,
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=1.0,  # Moderate temperature for Lynch's practical, intuitive approach
    ),
    output_schema=PeterLynchSignal,
    output_key="peter_lynch_agent_output",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)
