from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.investors.ben_graham_agent.prompt import BEN_GRAHAM_PROMPT
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

ben_graham_persona_agent = LlmAgent(
    name="ben_graham_persona_agent",
    model=settings.REASONING_MODEL,
    instruction=BEN_GRAHAM_PROMPT,
    output_key="ben_graham_persona_agent_output",
)

investor_formatter_agent = build_investor_formatter_agent("ben_graham")

ben_graham_agent = SequentialAgent(
    name="ben_graham_agent",
    sub_agents=[
        ben_graham_persona_agent, 
        investor_formatter_agent
    ],
)
