import os

from google.adk.agents import LlmAgent
from google.genai import types
from google.adk.models.lite_llm import LiteLlm, LiteLLMClient

from dotenv import load_dotenv

from src.agents.investors.stanley_druckenmiller.prompt import (
    STANLEY_DRUCKENMILLER_PROMPT,
)
from src.agents.investors.stanley_druckenmiller.schema import StanleyDruckenmillerOutput
from src.tools.druckenmiller_analysis import (
    analyze_growth_momentum,
    assess_risk_reward,
    analyze_druckenmiller_valuation,
    evaluate_sentiment_catalysts,
    analyze_insider_signals,
)

load_dotenv()

DEPLOYMENT = os.environ["AZURE_DEPLOYMENT_NAME"]  # e.g. "gpt-4o-mini"

# 1) one-time setup
# model must be your Azure *deployment name*, prefixed with 'azure/'
azure_llm = LiteLlm(model=f"azure/{DEPLOYMENT}", llm_client=LiteLLMClient())

tools = [
    analyze_growth_momentum,
    assess_risk_reward,
    analyze_druckenmiller_valuation,
    evaluate_sentiment_catalysts,
    analyze_insider_signals,
]

# 2) use it in your agents
stanley_druckenmiller_agent = LlmAgent(
    model=azure_llm,  # pass the instance, not a string
    name="stanley_druckenmiller_investment_agent",
    instruction=STANLEY_DRUCKENMILLER_PROMPT,
    tools=tools,
    generate_content_config=types.GenerateContentConfig(
        temperature=1.0,  # Very low temperature for Druckenmiller's disciplined approach
    ),
    output_schema=StanleyDruckenmillerOutput,
    output_key="stanley_druckenmiller_agent_output",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)
