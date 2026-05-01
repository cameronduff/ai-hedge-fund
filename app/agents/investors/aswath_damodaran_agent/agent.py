from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.investors.aswath_damodaran_agent.prompt import ASWATH_DAMODARAN_PROMPT
from app.agents.investors.investor_formatter_agent.agent import build_investor_formatter_agent
from app.models.investors_models import InvestorResponse

planner = BuiltInPlanner(
    thinking_config=types.ThinkingConfig(
        include_thoughts=True,
        thinking_level=types.ThinkingLevel.HIGH,
    )
)

generate_content_config = types.GenerateContentConfig(
    temperature=0.3,
)

aswath_damodaran_persona_agent = LlmAgent(
    name="aswath_damodaran_persona_agent",
    model=settings.REASONING_MODEL,
    instruction=ASWATH_DAMODARAN_PROMPT,
    output_key="aswath_damodaran_persona_agent_output",
)

investor_formatter_agent = build_investor_formatter_agent("aswath_damodaran")

aswath_damodaran_agent = SequentialAgent(
    name="aswath_damodaran_agent",
    sub_agents=[
        aswath_damodaran_persona_agent, 
        investor_formatter_agent
    ],
)