from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.investors.warren_buffet_agent.prompt import WARREN_BUFFET_PROMPT
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

warren_buffet_persona_agent = LlmAgent(
    name="warren_buffet_persona_agent",
    model=settings.REASONING_MODEL,
    instruction=WARREN_BUFFET_PROMPT,
    output_key="warren_buffet_persona_agent_output",
)

investor_formatter_agent = build_investor_formatter_agent("warren_buffet")

warren_buffet_agent = SequentialAgent(
    name="warren_buffet_agent",
    sub_agents=[
        warren_buffet_persona_agent, 
        investor_formatter_agent
    ],
)
