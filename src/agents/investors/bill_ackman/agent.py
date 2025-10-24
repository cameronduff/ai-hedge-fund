from google.adk.agents import LlmAgent
from google.genai import types
from loguru import logger
from dotenv import load_dotenv

from src.agents.investors.bill_ackman.prompt import BILL_ACKMAN_PROMPT
from src.agents.investors.bill_ackman.schema import BillAckmanSignal
from src.tools.ackman_analysis import (
    analyze_business_quality,
    analyze_financial_discipline,
    analyze_activism_potential,
    analyze_ackman_valuation,
    calculate_ackman_score,
)

load_dotenv()


def build_bill_ackman_agent() -> LlmAgent:
    """
    Build Bill Ackman concentrated value investing agent with activism-focused analysis tools.

    This agent implements Ackman's investment methodology combining:
    - Business quality assessment (competitive advantages, cash flow consistency, brand moats)
    - Financial discipline analysis (balance sheet strength, capital allocation efficiency)
    - Activism potential evaluation (operational improvement opportunities)
    - Rigorous valuation analysis (DCF with margin of safety requirements)
    - Overall Ackman score synthesis (concentrated investing criteria)

    The agent follows Ackman's approach of making large, high-conviction investments in
    exceptional businesses with clear value creation catalysts, often involving activist
    engagement to drive operational excellence and strategic improvements.
    """

    return LlmAgent(
        model="gemini-2.5-pro",
        name="bill_ackman_agent",
        instruction=BILL_ACKMAN_PROMPT,
        tools=[
            analyze_business_quality,
            analyze_financial_discipline,
            analyze_activism_potential,
            analyze_ackman_valuation,
            calculate_ackman_score,
        ],
        generate_content_config=types.GenerateContentConfig(
            temperature=0.2,  # Low temperature for disciplined, consistent analysis
        ),
        output_schema=BillAckmanSignal,
        output_key="bill_ackman_agent_output",
    )


bill_ackman_agent = build_bill_ackman_agent()
