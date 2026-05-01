from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.investors.michael_burry_agent.prompt import MICHAEL_BURRY_PROMPT
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

michael_burry_persona_agent = LlmAgent(
    name="michael_burry_persona_agent",
    model=settings.REASONING_MODEL,
    instruction=MICHAEL_BURRY_PROMPT,
    output_key="michael_burry_persona_agent_output",
)

investor_formatter_agent = build_investor_formatter_agent("michael_burry")

michael_burry_agent = SequentialAgent(
    name="michael_burry_agent",
    sub_agents=[
        michael_burry_persona_agent, 
        investor_formatter_agent
    ],
)
