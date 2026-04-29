from google.adk.agents import SequentialAgent

from app.agents.management.portfolio_manager_agent.agent import portfolio_manager_agent
from app.agents.management.risk_manager_agent.agent import risk_manager_agent

executive_orchestrator_agent = SequentialAgent(
    name="executive_orchestrator_agent",
    sub_agents=[portfolio_manager_agent, risk_manager_agent],
)
