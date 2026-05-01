from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.investors.nassim_taleb_agent.prompt import NASSIM_TALEB_PROMPT
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

nassim_taleb_persona_agent = LlmAgent(
    name="nassim_taleb_persona_agent",
    model=settings.REASONING_MODEL,
    instruction=NASSIM_TALEB_PROMPT,
    output_key="nassim_taleb_persona_agent_output",
)

investor_formatter_agent = build_investor_formatter_agent("nassim_taleb")

nassim_taleb_agent = SequentialAgent(
    name="nassim_taleb_agent",
    sub_agents=[
        nassim_taleb_persona_agent, 
        investor_formatter_agent
    ],
)
