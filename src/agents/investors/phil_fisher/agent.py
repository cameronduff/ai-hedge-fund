from google.adk.agents import LlmAgent
from google.genai import types

from src.agents.investors.phil_fisher.prompt import PHIL_FISHER_PROMPT
from src.agents.investors.phil_fisher.schema import PhilFisherSignal
from src.tools.fisher_analysis import (
    analyze_growth_quality_metrics,
    analyze_management_excellence,
    analyze_profit_margins_stability,
    analyze_competitive_position,
    calculate_fisher_score,
)

# Phil Fisher Agent with long-term growth and management excellence analysis tools
phil_fisher_agent = LlmAgent(
    model="gemini-2.5-pro",
    name="phil_fisher_agent",
    instruction=PHIL_FISHER_PROMPT,
    tools=[
        analyze_growth_quality_metrics,
        analyze_management_excellence,
        analyze_profit_margins_stability,
        analyze_competitive_position,
        calculate_fisher_score,
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.2,  # Low temperature for Fisher's methodical, analytical approach
    ),
    output_schema=PhilFisherSignal,
    output_key="phil_fisher_agent_output",
)
