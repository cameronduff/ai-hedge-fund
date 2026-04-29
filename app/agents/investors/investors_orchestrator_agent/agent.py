from google.adk.agents import ParallelAgent, SequentialAgent, LlmAgent

from app.agents.investors.chief_investment_officer.agent import (
    chief_investment_officer_agent,
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

investor_boardroom = ParallelAgent(
    name="investor_boardroom",
    sub_agents=[
        aswath_damodaran_agent,
        ben_graham_agent,
        bill_ackman_agent,
        cathie_wood_agent,
        charlie_munger_agent,
        michael_burry_agent,
        monish_pabrai_agent,
        nassim_taleb_agent,
        peter_lynch_agent,
        phil_fisher_agent,
        rakesh_jhunjhunwala_agent,
        stanley_druckenmiller_agent,
        warren_buffet_agent,
    ],
)

investors_orchestrator_agent = SequentialAgent(
    name="investors_orchestrator_agent",
    sub_agents=[investor_boardroom, chief_investment_officer_agent],
)
