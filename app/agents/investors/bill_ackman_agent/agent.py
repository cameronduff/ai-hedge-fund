from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.investors.bill_ackman_agent.prompt import BILL_ACKMAN_PROMPT
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

bill_ackman_persona_agent = LlmAgent(
    name="bill_ackman_persona_agent",
    model=settings.REASONING_MODEL,
    instruction=BILL_ACKMAN_PROMPT,
    output_key="bill_ackman_persona_agent_output",
)

investor_formatter_agent = build_investor_formatter_agent("bill_ackman")

bill_ackman_agent = SequentialAgent(
    name="bill_ackman_agent",
    sub_agents=[
        bill_ackman_persona_agent, 
        investor_formatter_agent
    ],
)
