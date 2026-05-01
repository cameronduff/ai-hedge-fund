from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.investors.cathie_wood_agent.prompt import CATHIE_WOOD_PROMPT
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

cathie_wood_persona_agent = LlmAgent(
    name="cathie_wood_persona_agent",
    model=settings.REASONING_MODEL,
    instruction=CATHIE_WOOD_PROMPT,
    output_key="cathie_wood_persona_agent_output",
)

investor_formatter_agent = build_investor_formatter_agent("cathie_wood")

cathie_wood_agent = SequentialAgent(
    name="cathie_wood_agent",
    sub_agents=[
        cathie_wood_persona_agent, 
        investor_formatter_agent
    ],
)
