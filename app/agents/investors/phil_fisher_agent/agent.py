from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.investors.phil_fisher_agent.prompt import PHIL_FISHER_PROMPT
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

phil_fisher_persona_agent = LlmAgent(
    name="phil_fisher_persona_agent",
    model=settings.REASONING_MODEL,
    instruction=PHIL_FISHER_PROMPT,
    output_key="phil_fisher_persona_agent_output",
)

investor_formatter_agent = build_investor_formatter_agent("phil_fisher")

phil_fisher_agent = SequentialAgent(
    name="phil_fisher_agent",
    sub_agents=[
        phil_fisher_persona_agent, 
        investor_formatter_agent
    ],
)
