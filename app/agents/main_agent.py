from google.adk.agents import SequentialAgent

from app.agents.quants.quants_orchestrator_agent.agent import quants_orchestrator_agent
from app.agents.investors.investors_orchestrator_agent.agent import (
    investors_orchestrator_agent,
)
from app.agents.management.portfolio_manager_agent.agent import (
    portfolio_manager_agent,
)

ai_hedge_fund = SequentialAgent(
    name="ai_hedge_fund",
    sub_agents=[
        quants_orchestrator_agent,
        investors_orchestrator_agent,
        portfolio_manager_agent,
    ],
)
