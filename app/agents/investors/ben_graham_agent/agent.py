from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.models.quants_models import Ticker
from app.core.config import settings
from app.agents.investors.ben_graham_agent.prompt import BEN_GRAHAM_PROMPT
from app.agents.investors.investor_formatter_agent.agent import build_investor_formatter_agent


def _build_persona() -> LlmAgent:
    return LlmAgent(
        name="ben_graham_agent",
        model=settings.REASONING_MODEL,
        instruction=BEN_GRAHAM_PROMPT,
        input_schema=Ticker,
        planner=BuiltInPlanner(
            thinking_config=types.ThinkingConfig(
                include_thoughts=True,
                thinking_level=types.ThinkingLevel.HIGH,
            )
        ),
        generate_content_config=types.GenerateContentConfig(temperature=0.3),
        output_key="ben_graham_persona_agent_output",
    )


def build_ben_graham_agent() -> SequentialAgent:
    return SequentialAgent(
        name="ben_graham_boardroom_agent",
        sub_agents=[
            _build_persona(),
            build_investor_formatter_agent("ben_graham"),
        ],
    )


def build_ben_graham_debate_agent() -> LlmAgent:
    return _build_persona()
