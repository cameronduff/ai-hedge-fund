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
    generation_config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=RakeshJhunjhunwalaSignal.model_json_schema(),
        temperature=0.1,  # Very low temperature for Jhunjhunwala's disciplined, analytical approach
    ),
)
