from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.investors.rakesh_jhunjhunwala_agent.prompt import (
    RAKESH_JHUNJHUNWALA_PROMPT,
)
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

rakesh_jhunjhunwala_persona_agent = LlmAgent(
    name="rakesh_jhunjhunwala_persona_agent",
    model=settings.REASONING_MODEL,
    instruction=RAKESH_JHUNJHUNWALA_PROMPT,
    output_key="rakesh_jhunjhunwala_persona_agent_output",
)

investor_formatter_agent = build_investor_formatter_agent("rakesh_jhunjhunwala")

rakesh_jhunjhunwala_agent = SequentialAgent(
    name="rakesh_jhunjhunwala_agent",
    sub_agents=[
        rakesh_jhunjhunwala_persona_agent, 
        investor_formatter_agent
    ],
)
