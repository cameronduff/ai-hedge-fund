from google.adk.agents import LlmAgent
from google.genai import types

from src.agents.investors.mohnish_pabrai.prompt import MOHNISH_PABRAI_PROMPT
from src.agents.investors.mohnish_pabrai.schema import MohnishPabraiSignal
from src.tools.pabrai_analysis import (
    analyze_downside_protection,
    analyze_pabrai_valuation,
    analyze_double_potential,
    analyze_business_simplicity,
    calculate_pabrai_score,
)

# Mohnish Pabrai Agent with "heads I win, tails I don't lose much" analysis tools
mohnish_pabrai_agent = LlmAgent(
    model="gemini-2.5-pro",
    name="mohnish_pabrai_agent",
    instruction=MOHNISH_PABRAI_PROMPT,
    tools=[
        analyze_downside_protection,
        analyze_pabrai_valuation,
        analyze_double_potential,
        analyze_business_simplicity,
        calculate_pabrai_score,
    ],
    generation_config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=MohnishPabraiSignal.model_json_schema(),
        temperature=0.2,  # Low temperature for systematic, checklist-driven approach
    ),
)
