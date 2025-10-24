from google.adk.agents import LlmAgent
from google.genai import types
from loguru import logger
from dotenv import load_dotenv

from src.agents.investors.ben_graham.prompt import BEN_GRAHAM_PROMPT
from src.agents.investors.ben_graham.schema import BenGrahamSignal
from src.tools.graham_analysis import (
    analyze_earnings_stability,
    analyze_financial_strength,
    analyze_valuation_graham,
    calculate_graham_score,
)

load_dotenv()


def build_ben_graham_agent() -> LlmAgent:
    """
    Build Ben Graham defensive value investing agent with classic analysis tools.

    This agent implements Benjamin Graham's conservative investment methodology:
    - Earnings stability analysis (multi-year positive earnings requirements)
    - Financial strength assessment (current ratio, debt ratios, dividend consistency)
    - Graham-specific valuation methods (Net-Net analysis, Graham Number calculations)
    - Overall Graham score synthesis (comprehensive defensive investment criteria)

    The agent follows Graham's "margin of safety" principle, emphasizing capital
    preservation and quantitative screening for undervalued securities with strong
    fundamentals. All calculations use Graham's original formulas and criteria.
    """

    return LlmAgent(
        model="gemini-2.5-pro",
        name="ben_graham_agent",
        instruction=BEN_GRAHAM_PROMPT,
        tools=[
            analyze_earnings_stability,
            analyze_financial_strength,
            analyze_valuation_graham,
            calculate_graham_score,
        ],
        generate_content_config=types.GenerateContentConfig(
            temperature=0.2,  # Low temperature for conservative, consistent analysis
        ),
        output_schema=BenGrahamSignal,
        output_key="ben_graham_agent_output",
    )


ben_graham_agent = build_ben_graham_agent()
