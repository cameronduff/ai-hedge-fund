from google.adk.agents import LlmAgent
from google.genai import types

from dotenv import load_dotenv

from src.agents.investors.stanley_druckenmiller.prompt import (
    STANLEY_DRUCKENMILLER_PROMPT,
)
from src.agents.investors.stanley_druckenmiller.schema import StanleyDruckenmillerOutput
from src.tools.druckenmiller_analysis import (
    analyze_growth_momentum,
    assess_risk_reward,
    analyze_druckenmiller_valuation,
    evaluate_sentiment_catalysts,
    analyze_insider_signals,
)

load_dotenv()


tools = [
    analyze_growth_momentum,
    assess_risk_reward,
    analyze_druckenmiller_valuation,
    evaluate_sentiment_catalysts,
    analyze_insider_signals,
]

stanley_druckenmiller_agent = LlmAgent(
    model="gemini-2.5-pro",
    name="stanley_druckenmiller_investment_agent",
    instruction=STANLEY_DRUCKENMILLER_PROMPT,
    tools=tools,
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1,  # Very low temperature for Druckenmiller's disciplined approach
    ),
    output_schema=StanleyDruckenmillerOutput,
    output_key="stanley_druckenmiller_agent_output",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)
