from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.investors.monish_pabrai_agent.prompt import MONISH_PABRAI_PROMPT
from app.agents.investors.investor_formatter_agent.agent import build_investor_formatter_agent


def _build_persona() -> LlmAgent:
    return LlmAgent(
        name="monish_pabrai_agent",
        model=settings.REASONING_MODEL,
        instruction=MONISH_PABRAI_PROMPT,
        planner=BuiltInPlanner(
            thinking_config=types.ThinkingConfig(
                include_thoughts=True,
                thinking_level=types.ThinkingLevel.HIGH,
            )
        ),
        generate_content_config=types.GenerateContentConfig(temperature=0.3),
        output_key="monish_pabrai_persona_agent_output",
    )


def build_monish_pabrai_agent() -> SequentialAgent:
    return SequentialAgent(
        name="monish_pabrai_boardroom_agent",
        sub_agents=[
            _build_persona(),
            build_investor_formatter_agent("monish_pabrai"),
        ],
    )


def build_monish_pabrai_debate_agent() -> LlmAgent:
    return _build_persona()
