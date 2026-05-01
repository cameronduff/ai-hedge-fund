from google.adk.agents import ParallelAgent, SequentialAgent, LlmAgent

from app.core.config import settings
from app.agents.investors.chief_investment_officer.prompt import (
    CHIEF_INVESTMENT_OFFICER_PROMPT,
)

from app.agents.investors.aswath_damodaran_agent.agent import aswath_damodaran_agent
from app.agents.investors.ben_graham_agent.agent import ben_graham_agent
from app.agents.investors.bill_ackman_agent.agent import bill_ackman_agent
from app.agents.investors.cathie_wood_agent.agent import cathie_wood_agent
from app.agents.investors.charlie_munger_agent.agent import charlie_munger_agent
from app.agents.investors.michael_burry_agent.agent import michael_burry_agent
from app.agents.investors.monish_pabrai_agent.agent import monish_pabrai_agent
from app.agents.investors.nassim_taleb_agent.agent import nassim_taleb_agent
from app.agents.investors.peter_lynch_agent.agent import peter_lynch_agent
from app.agents.investors.phil_fisher_agent.agent import phil_fisher_agent
from app.agents.investors.rakesh_jhunjhunwala_agent.agent import (
    rakesh_jhunjhunwala_agent,
)
from app.agents.investors.stanley_druckenmiller_agent.agent import (
    stanley_druckenmiller_agent,
)
from app.agents.investors.warren_buffet_agent.agent import warren_buffet_agent

chief_investment_officer_agent = LlmAgent(
    name="chief_investment_officer_agent",
    model=settings.REASONING_MODEL,
    instruction=CHIEF_INVESTMENT_OFFICER_PROMPT,
    output_key="chief_investment_officer_output"
)
