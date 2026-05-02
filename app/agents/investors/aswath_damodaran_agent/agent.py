from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.models.quants_models import Ticker
from app.core.config import settings
from app.agents.investors.aswath_damodaran_agent.prompt import ASWATH_DAMODARAN_PROMPT
from app.agents.investors.investor_formatter_agent.agent import build_investor_formatter_agent


def _build_persona() -> LlmAgent:
    return LlmAgent(
        name="aswath_damodaran_agent",
        model=settings.REASONING_MODEL,
        instruction=ASWATH_DAMODARAN_PROMPT,
        input_schema=Ticker,
        planner=BuiltInPlanner(
            thinking_config=types.ThinkingConfig(
                include_thoughts=True,
                thinking_level=types.ThinkingLevel.HIGH,
            )
        ),
        generate_content_config=types.GenerateContentConfig(temperature=0.3),
        output_key="aswath_damodaran_persona_agent_output",
    )


def build_aswath_damodaran_agent() -> SequentialAgent:
    return SequentialAgent(
        name="aswath_damodaran_boardroom_agent",
        sub_agents=[
            _build_persona(),
            build_investor_formatter_agent("aswath_damodaran"),
        ],
    )


def build_aswath_damodaran_debate_agent() -> LlmAgent:
    return _build_persona()