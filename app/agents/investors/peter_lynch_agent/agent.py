from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.investors.peter_lynch_agent.prompt import PETER_LYNCH_PROMPT
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

peter_lynch_persona_agent = LlmAgent(
    name="peter_lynch_persona_agent",
    model=settings.REASONING_MODEL,
    instruction=PETER_LYNCH_PROMPT,
    output_key="peter_lynch_persona_agent_output",
)

investor_formatter_agent = build_investor_formatter_agent("peter_lynch")

peter_lynch_agent = SequentialAgent(
    name="peter_lynch_agent",
    sub_agents=[
        peter_lynch_persona_agent, 
        investor_formatter_agent
    ],
)
