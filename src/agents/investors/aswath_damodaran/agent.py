from google.adk.agents import LlmAgent
from google.genai import types
from loguru import logger
from dotenv import load_dotenv

from src.agents.investors.aswath_damodaran.prompt import ASWATH_DAMODARAN_PROMPT
from src.agents.investors.aswath_damodaran.schema import AswathDamodaranSignal
from src.tools.damodaran_analysis import (
    analyze_growth_and_reinvestment,
    analyze_risk_profile,
    analyze_relative_valuation,
    calculate_intrinsic_value_dcf,
    calculate_margin_of_safety,
)

load_dotenv()


def build_aswath_damodaran_agent() -> LlmAgent:
    """
    Build Aswath Damodaran investment analysis agent with financial analysis tools.

    This agent combines Damodaran's valuation methodology with rigorous quantitative tools:
    - Growth and reinvestment analysis (revenue CAGR, ROIC scoring)
    - Risk profile assessment (beta, leverage, interest coverage, cost of equity)
    - Relative valuation analysis (P/E vs historical medians)
    - DCF intrinsic value calculations (FCFF-based with terminal value)
    - Margin of safety computations (precise undervaluation metrics)

    The agent follows Damodaran's "Story → Numbers → Value" framework, using tools
    for all quantitative analysis while providing qualitative narrative reasoning.
    """

    return LlmAgent(
        model="gemini-2.5-flash",
        name="aswath_damodaran_agent",
        instruction=ASWATH_DAMODARAN_PROMPT,
        tools=[
            analyze_growth_and_reinvestment,
            analyze_risk_profile,
            analyze_relative_valuation,
            calculate_intrinsic_value_dcf,
            calculate_margin_of_safety,
        ],
        generate_content_config=types.GenerateContentConfig(
            temperature=0.1,  # Low temperature for consistent analytical approach
        ),
        output_schema=AswathDamodaranSignal,
    )


aswath_damodaran_agent = build_aswath_damodaran_agent()
