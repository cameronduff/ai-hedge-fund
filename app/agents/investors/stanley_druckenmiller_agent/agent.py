from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.models.quants_models import Ticker
from app.core.config import settings
from app.agents.investors.stanley_druckenmiller_agent.prompt import STANLEY_DRUCKENMILLER_PROMPT
from app.agents.investors.investor_formatter_agent.agent import build_investor_formatter_agent


def _build_persona() -> LlmAgent:
    return LlmAgent(
        name="stanley_druckenmiller_agent",
        model=settings.REASONING_MODEL,
        instruction=STANLEY_DRUCKENMILLER_PROMPT,
        input_schema=Ticker,
        planner=BuiltInPlanner(
            thinking_config=types.ThinkingConfig(
                include_thoughts=True,
                thinking_level=types.ThinkingLevel.HIGH,
            )
        ),
        generate_content_config=types.GenerateContentConfig(temperature=0.3),
        output_key="stanley_druckenmiller_persona_agent_output",
    )


def build_stanley_druckenmiller_agent() -> SequentialAgent:
    return SequentialAgent(
        name="stanley_druckenmiller_boardroom_agent",
        sub_agents=[
            _build_persona(),
            build_investor_formatter_agent("stanley_druckenmiller"),
        ],
    )


def build_stanley_druckenmiller_debate_agent() -> LlmAgent:
    return _build_persona()
