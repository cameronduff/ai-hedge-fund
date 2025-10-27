import os

from google.adk.agents import LlmAgent
from google.genai import types
from google.adk.models.lite_llm import LiteLlm

from src.agents.risk_manager.prompt import RISK_MANAGER_PROMPT
from src.agents.risk_manager.schema import RiskManagerOutput
from src.tools.risk_analysis import (
    calculate_volatility_metrics,
    calculate_volatility_adjusted_limit,
    analyze_correlation_risk,
    calculate_position_limits,
    assess_portfolio_risk_concentration,
)

DEPLOYMENT = os.environ["AZURE_DEPLOYMENT_NAME"]  # e.g. "gpt-4o-mini"

# Risk Manager Agent with comprehensive risk analysis and position sizing tools
risk_manager_agent = LlmAgent(
    model=f"azure/{DEPLOYMENT}",
    name="risk_manager_agent",
    instruction=RISK_MANAGER_PROMPT,
    tools=[
        calculate_volatility_metrics,
        calculate_volatility_adjusted_limit,
        analyze_correlation_risk,
        calculate_position_limits,
        assess_portfolio_risk_concentration,
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1,  # Very low temperature for precise risk calculations
    ),
    output_schema=RiskManagerOutput,
    output_key="risk_manager_output",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)
