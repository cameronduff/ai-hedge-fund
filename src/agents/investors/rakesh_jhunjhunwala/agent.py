from google.adk.agents import LlmAgent
from google.genai import types

from src.agents.investors.rakesh_jhunjhunwala.prompt import RAKESH_JHUNJHUNWALA_PROMPT
from src.agents.investors.rakesh_jhunjhunwala.schema import RakeshJhunjhunwalaSignal
from src.tools.jhunjhunwala_analysis import (
    analyze_quality_fundamentals,
    analyze_growth_sustainability,
    analyze_balance_sheet_strength,
    analyze_cash_flow_quality,
    calculate_jhunjhunwala_score,
)

# Rakesh Jhunjhunwala Agent with quality-focused value with growth analysis tools
rakesh_jhunjhunwala_agent = LlmAgent(
    model="gemini-2.5-pro",
    name="rakesh_jhunjhunwala_agent",
    instruction=RAKESH_JHUNJHUNWALA_PROMPT,
    tools=[
        analyze_quality_fundamentals,
        analyze_growth_sustainability,
        analyze_balance_sheet_strength,
        analyze_cash_flow_quality,
        calculate_jhunjhunwala_score,
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1,  # Very low temperature for Jhunjhunwala's disciplined, analytical approach
    ),
    output_schema=RakeshJhunjhunwalaSignal,
    output_key="rakesh_jhunjhunwala_agent_output",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)
