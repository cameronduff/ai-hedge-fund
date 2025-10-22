from google.adk.agents import LlmAgent
from google.genai import types

from dotenv import load_dotenv

from src.agents.valuation_agent.prompt import VALUATION_AGENT_PROMPT
from src.agents.valuation_agent.schema import ValuationAgentOutput
from src.tools.valuation_analysis import (
    calculate_enhanced_dcf,
    calculate_owner_earnings,
    calculate_ev_ebitda_valuation,
    calculate_residual_income,
    aggregate_valuation_methods,
)

load_dotenv()


valuation_agent = LlmAgent(
    model="gemini-2.5-pro",
    name="valuation_analysis_agent",
    instruction=VALUATION_AGENT_PROMPT,
    tools=[
        calculate_enhanced_dcf,
        calculate_owner_earnings,
        calculate_ev_ebitda_valuation,
        calculate_residual_income,
        aggregate_valuation_methods,
    ],
    response_config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=ValuationAgentOutput.model_json_schema(),
        temperature=0.1,
    ),
)
