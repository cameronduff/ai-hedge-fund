from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.planners import BuiltInPlanner
from google.adk.tools.agent_tool import AgentTool
from google.genai import types

from app.core.config import settings
from app.agents.investors.chief_investment_officer.prompt import (
    CHIEF_INVESTMENT_OFFICER_PROMPT,
    CHIEF_INVESTMENT_OFFICER_FORMATTING_PROMPT,
)
from app.models.investors_models import CIOOutput

from app.agents.investors.aswath_damodaran_agent.agent import build_aswath_damodaran_debate_agent
from app.agents.investors.ben_graham_agent.agent import build_ben_graham_debate_agent
from app.agents.investors.bill_ackman_agent.agent import build_bill_ackman_debate_agent
from app.agents.investors.cathie_wood_agent.agent import build_cathie_wood_debate_agent
from app.agents.investors.charlie_munger_agent.agent import build_charlie_munger_debate_agent
from app.agents.investors.michael_burry_agent.agent import build_michael_burry_debate_agent
from app.agents.investors.mohnish_pabrai_agent.agent import build_mohnish_pabrai_debate_agent
from app.agents.investors.nassim_taleb_agent.agent import build_nassim_taleb_debate_agent
from app.agents.investors.peter_lynch_agent.agent import build_peter_lynch_debate_agent
from app.agents.investors.phil_fisher_agent.agent import build_phil_fisher_debate_agent
from app.agents.investors.rakesh_jhunjhunwala_agent.agent import build_rakesh_jhunjhunwala_debate_agent
from app.agents.investors.stanley_druckenmiller_agent.agent import build_stanley_druckenmiller_debate_agent
from app.agents.investors.warren_buffett_agent.agent import build_warren_buffett_debate_agent


chief_investment_officer_debater = LlmAgent(
    name="chief_investment_officer_debater",
    model=settings.REASONING_MODEL,
    instruction=CHIEF_INVESTMENT_OFFICER_PROMPT,
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_level=types.ThinkingLevel.HIGH,
        )
    ),
    tools=[
        AgentTool(agent=build_aswath_damodaran_debate_agent()),
        AgentTool(agent=build_ben_graham_debate_agent()),
        AgentTool(agent=build_bill_ackman_debate_agent()),
        AgentTool(agent=build_cathie_wood_debate_agent()),
        AgentTool(agent=build_charlie_munger_debate_agent()),
        AgentTool(agent=build_michael_burry_debate_agent()),
        AgentTool(agent=build_mohnish_pabrai_debate_agent()),
        AgentTool(agent=build_nassim_taleb_debate_agent()),
        AgentTool(agent=build_peter_lynch_debate_agent()),
        AgentTool(agent=build_phil_fisher_debate_agent()),
        AgentTool(agent=build_rakesh_jhunjhunwala_debate_agent()),
        AgentTool(agent=build_stanley_druckenmiller_debate_agent()),
        AgentTool(agent=build_warren_buffett_debate_agent()),
    ],
    output_key="chief_investment_officer_debate_output",
    generate_content_config=types.GenerateContentConfig(temperature=0.0),
)

chief_investment_officer_formatter = LlmAgent(
    name="chief_investment_officer_formatter",
    model=settings.REASONING_MODEL,
    instruction=CHIEF_INVESTMENT_OFFICER_FORMATTING_PROMPT,
    output_schema=CIOOutput,
    output_key="chief_investment_officer_output",
)

chief_investment_officer_agent = SequentialAgent(
    name="chief_investment_officer_agent",
    sub_agents=[
        chief_investment_officer_debater,
        chief_investment_officer_formatter,
    ],
)
