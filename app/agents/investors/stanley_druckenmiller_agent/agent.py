from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.investors.stanley_druckenmiller_agent.prompt import (
    STANLEY_DRUCKENMILLER_PROMPT,
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

stanley_druckenmiller_persona_agent = LlmAgent(
    name="stanley_druckenmiller_persona_agent",
    model=settings.REASONING_MODEL,
    instruction=STANLEY_DRUCKENMILLER_PROMPT,
    output_key="stanley_druckenmiller_persona_agent_output",
)

investor_formatter_agent = build_investor_formatter_agent("stanley_druckenmiller")

stanley_druckenmiller_agent = SequentialAgent(
    name="stanley_druckenmiller_agent",
    sub_agents=[
        stanley_druckenmiller_persona_agent, 
        investor_formatter_agent
    ],
)
