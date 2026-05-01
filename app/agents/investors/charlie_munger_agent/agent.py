from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.investors.charlie_munger_agent.prompt import CHARLIE_MUNGER_PROMPT
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

charlie_munger_persona_agent = LlmAgent(
    name="charlie_munger_persona_agent",
    model=settings.REASONING_MODEL,
    instruction=CHARLIE_MUNGER_PROMPT,
    output_key="charlie_munger_persona_agent_output",
)

investor_formatter_agent = build_investor_formatter_agent("charlie_munger")

charlie_munger_agent = SequentialAgent(
    name="charlie_munger_agent",
    sub_agents=[
        charlie_munger_persona_agent, 
        investor_formatter_agent
    ],
)
