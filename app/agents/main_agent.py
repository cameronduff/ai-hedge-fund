from google.adk.agents import SequentialAgent

from app.agents.quants.quants_orchestrator_agent.agent import quants_orchestrator_agent
from app.agents.investors.investors_orchestrator_agent.agent import (
    investors_orchestrator_agent,
)
from app.agents.management.executive_orchestrator_agent.agent import (
    executive_orchestrator_agent,
)

chief_of_staff_agent = SequentialAgent(
    name="chief_of_staff_agent",
    sub_agents=[
        quants_orchestrator_agent,
        investors_orchestrator_agent,
        executive_orchestrator_agent,
    ],
)
