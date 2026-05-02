from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.models.quants_models import Ticker
from app.core.config import settings
from app.agents.investors.michael_burry_agent.prompt import MICHAEL_BURRY_PROMPT
from app.agents.investors.investor_formatter_agent.agent import build_investor_formatter_agent


def _build_persona() -> LlmAgent:
    return LlmAgent(
        name="michael_burry_agent",
        model=settings.REASONING_MODEL,
        instruction=MICHAEL_BURRY_PROMPT,
        input_schema=Ticker,
        planner=BuiltInPlanner(
            thinking_config=types.ThinkingConfig(
                include_thoughts=True,
                thinking_level=types.ThinkingLevel.HIGH,
            )
        ),
        generate_content_config=types.GenerateContentConfig(temperature=0.3),
        output_key="michael_burry_persona_agent_output",
    )


def build_michael_burry_agent() -> SequentialAgent:
    return SequentialAgent(
        name="michael_burry_boardroom_agent",
        sub_agents=[
            _build_persona(),
            build_investor_formatter_agent("michael_burry"),
        ],
    )


def build_michael_burry_debate_agent() -> LlmAgent:
    return _build_persona()
