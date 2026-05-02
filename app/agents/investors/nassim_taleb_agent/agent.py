from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.models.quants_models import Ticker
from app.core.config import settings
from app.agents.investors.nassim_taleb_agent.prompt import NASSIM_TALEB_PROMPT
from app.agents.investors.investor_formatter_agent.agent import build_investor_formatter_agent


def _build_persona() -> LlmAgent:
    return LlmAgent(
        name="nassim_taleb_agent",
        model=settings.REASONING_MODEL,
        instruction=NASSIM_TALEB_PROMPT,
        input_schema=Ticker,
        planner=BuiltInPlanner(
            thinking_config=types.ThinkingConfig(
                include_thoughts=True,
                thinking_level=types.ThinkingLevel.HIGH,
            )
        ),
        generate_content_config=types.GenerateContentConfig(temperature=0.3),
        output_key="nassim_taleb_persona_agent_output",
    )


def build_nassim_taleb_agent() -> SequentialAgent:
    return SequentialAgent(
        name="nassim_taleb_boardroom_agent",
        sub_agents=[
            _build_persona(),
            build_investor_formatter_agent("nassim_taleb"),
        ],
    )


def build_nassim_taleb_debate_agent() -> LlmAgent:
    return _build_persona()
