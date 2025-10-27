import os

from google.adk.agents import LlmAgent
from google.genai import types
from google.adk.models.lite_llm import LiteLlm
from loguru import logger
from dotenv import load_dotenv

from src.agents.investors.charlie_munger.prompt import CHARLIE_MUNGER_PROMPT
from src.agents.investors.charlie_munger.schema import CharlieMungerSignal
from src.tools.munger_analysis import (
    analyze_moat_strength,
    analyze_management_quality,
    analyze_predictability,
    calculate_munger_valuation,
    calculate_munger_score,
)

load_dotenv()

DEPLOYMENT = os.environ["AZURE_DEPLOYMENT_NAME"]  # e.g. "gpt-4o-mini"


def build_charlie_munger_agent() -> LlmAgent:
    """
    Build Charlie Munger rational investing agent with quality-focused analysis tools.

    This agent implements Munger's investment methodology emphasizing:
    - Competitive moat assessment (ROIC consistency, pricing power, capital efficiency)
    - Management quality evaluation (capital allocation, shareholder alignment, financial discipline)
    - Business predictability analysis (earnings stability, margin consistency, cash flow reliability)
    - Rational valuation methodology (owner earnings, simple multiples, margin of safety)
    - Overall quality score synthesis (60% quality, 25% management, 15% valuation weighting)

    The agent follows Munger's philosophy of buying wonderful companies at fair prices,
    emphasizing business quality and predictability over complex quantitative models,
    and applying multidisciplinary mental models for robust investment decisions.
    """

    return LlmAgent(
        model=f"azure/{DEPLOYMENT}",
        name="charlie_munger_agent",
        instruction=CHARLIE_MUNGER_PROMPT,
        tools=[
            analyze_moat_strength,
            analyze_management_quality,
            analyze_predictability,
            calculate_munger_valuation,
            calculate_munger_score,
        ],
        generate_content_config=types.GenerateContentConfig(
            temperature=0.1,  # Very low temperature for rational, consistent analysis
        ),
        output_schema=CharlieMungerSignal,
        output_key="charlie_munger_agent_output",
        disallow_transfer_to_parent=True,
        disallow_transfer_to_peers=True,
    )


charlie_munger_agent = build_charlie_munger_agent()
