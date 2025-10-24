from google.adk.agents import LlmAgent
from google.genai import types

from src.agents.risk_manager.prompt import RISK_MANAGER_PROMPT
from src.agents.risk_manager.schema import RiskManagerOutput
from src.tools.risk_analysis import (
    calculate_volatility_metrics,
    calculate_volatility_adjusted_limit,
    analyze_correlation_risk,
    calculate_position_limits,
    assess_portfolio_risk_concentration,
)

# Risk Manager Agent with comprehensive risk analysis and position sizing tools
risk_manager_agent = LlmAgent(
    model="gemini-2.5-pro",
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
)
