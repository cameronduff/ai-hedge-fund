from google.adk.agents import SequentialAgent

from app.agents.quants.quants_orchestrator_agent.agent import quants_orchestrator_agent
from app.agents.investors.investors_orchestrator_agent.agent import (
    investors_orchestrator_agent,
)
from app.agents.management.portfolio_manager_agent.agent import (
    portfolio_manager_agent,
)

chief_of_staff_agent = SequentialAgent(
    name="chief_of_staff_agent",
    sub_agents=[
        quants_orchestrator_agent,
        investors_orchestrator_agent,
        portfolio_manager_agent,
    ],
)
