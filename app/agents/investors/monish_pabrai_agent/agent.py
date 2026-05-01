from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.investors.monish_pabrai_agent.prompt import MONISH_PABRAI_PROMPT
from app.agents.investors.investor_formatter_agent.agent import build_investor_formatter_agent

planner = BuiltInPlanner(
    thinking_config=types.ThinkingConfig(
        include_thoughts=True,
        thinking_level=types.ThinkingLevel.HIGH,
    )
)

generate_content_config = types.GenerateContentConfig(
    temperature=0.3,
)

monish_pabrai_persona_agent = LlmAgent(
    name="monish_pabrai_persona_agent",
    model=settings.REASONING_MODEL,
    instruction=MONISH_PABRAI_PROMPT,
    output_key="monish_pabrai_persona_agent_output",
)

investor_formatter_agent = build_investor_formatter_agent("monish_pabrai")

monish_pabrai_agent = SequentialAgent(
    name="monish_pabrai_agent",
    sub_agents=[
        monish_pabrai_persona_agent, 
        investor_formatter_agent
    ],
)
