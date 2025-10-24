from google.adk.agents import LlmAgent
from google.adk.tools import google_search
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


# Valuation Agent with a variety of valuation model tools
valuation_agent = LlmAgent(
    model="gemini-2.5-pro",
    name="valuation_agent",
    instruction=VALUATION_AGENT_PROMPT,
    tools=[
        google_search,
        calculate_enhanced_dcf,
        calculate_owner_earnings,
        calculate_ev_ebitda_valuation,
        calculate_residual_income,
        aggregate_valuation_methods,
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1,  # Low temperature for precise, data-driven valuation
    ),
    output_schema=ValuationAgentOutput,
    output_key="valuation_agent_output",
)
