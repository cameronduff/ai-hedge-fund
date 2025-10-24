from google.adk.agents import LlmAgent
from google.genai import types
from loguru import logger
from dotenv import load_dotenv

from src.agents.investors.cathie_wood.prompt import CATHIE_WOOD_PROMPT
from src.agents.investors.cathie_wood.schema import CathieWoodSignal
from src.tools.cathie_wood_analysis import (
    analyze_disruptive_potential,
    analyze_innovation_growth,
    analyze_cathie_wood_valuation,
    calculate_cathie_wood_score,
)

load_dotenv()


def build_cathie_wood_agent() -> LlmAgent:
    """
    Build Cathie Wood disruptive innovation investing agent with exponential growth analysis tools.

    This agent implements Wood's investment methodology focusing on:
    - Disruptive potential assessment (breakthrough technology adoption, R&D intensity, scaling indicators)
    - Innovation-driven growth analysis (sustainable innovation scaling, reinvestment capacity)
    - High-growth valuation methodology (exponential DCF with 20% growth, 25x multiples)
    - Overall innovation score synthesis (breakthrough technology prioritization)

    The agent follows Wood's approach of identifying transformative technologies with
    exponential growth potential, accepting short-term volatility for multi-year
    compounding from platform businesses and network effects in large TAM markets.
    """

    return LlmAgent(
        model="gemini-2.5-pro",  # Use newer model for innovation-focused analysis
        name="cathie_wood_agent",
        instruction=CATHIE_WOOD_PROMPT,
        tools=[
            analyze_disruptive_potential,
            analyze_innovation_growth,
            analyze_cathie_wood_valuation,
            calculate_cathie_wood_score,
        ],
        generate_content_config=types.GenerateContentConfig(
            temperature=0.4,  # Higher temperature for creative/optimistic innovation analysis
        ),
        output_schema=CathieWoodSignal,
        output_key="cathie_wood_agent_output",
        disallow_transfer_to_parent=True,
        disallow_transfer_to_peers=True,
    )


cathie_wood_agent = build_cathie_wood_agent()
