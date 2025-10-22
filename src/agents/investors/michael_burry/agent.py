from google.adk.agents import LlmAgent
from google.genai import types

from src.agents.investors.michael_burry.prompt import MICHAEL_BURRY_PROMPT
from src.agents.investors.michael_burry.schema import MichaelBurrySignal
from src.tools.burry_analysis import (
    analyze_deep_value_metrics,
    analyze_balance_sheet_strength,
    analyze_insider_activity,
    analyze_contrarian_sentiment,
    calculate_burry_score,
)

# Michael Burry Agent with comprehensive deep value analysis tools
michael_burry_agent = LlmAgent(
    model="gemini-2.5-pro",
    name="michael_burry_agent",
    instruction=MICHAEL_BURRY_PROMPT,
    tools=[
        analyze_deep_value_metrics,
        analyze_balance_sheet_strength,
        analyze_insider_activity,
        analyze_contrarian_sentiment,
        calculate_burry_score,
    ],
    generation_config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=MichaelBurrySignal.model_json_schema(),
        temperature=0.1,  # Low temperature for analytical precision like Burry
    ),
)
