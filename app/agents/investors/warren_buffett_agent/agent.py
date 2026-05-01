from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.investors.warren_buffett_agent.prompt import WARREN_BUFFETT_PROMPT
from app.agents.investors.investor_formatter_agent.agent import build_investor_formatter_agent


def _build_persona() -> LlmAgent:
    return LlmAgent(
        name="warren_buffett_agent",
        model=settings.REASONING_MODEL,
        instruction=WARREN_BUFFETT_PROMPT,
        planner=BuiltInPlanner(
            thinking_config=types.ThinkingConfig(
                include_thoughts=True,
                thinking_level=types.ThinkingLevel.HIGH,
            )
        ),
        generate_content_config=types.GenerateContentConfig(temperature=0.3),
        output_key="warren_buffett_persona_agent_output",
    )


def build_warren_buffett_agent() -> SequentialAgent:
    return SequentialAgent(
        name="warren_buffett_boardroom_agent",
        sub_agents=[
            _build_persona(),
            build_investor_formatter_agent("warren_buffett"),
        ],
    )


def build_warren_buffett_debate_agent() -> LlmAgent:
    return _build_persona()
