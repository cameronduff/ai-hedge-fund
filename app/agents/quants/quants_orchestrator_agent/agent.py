from google.adk.agents import ParallelAgent

from app.agents.quants.fundamentals_agent.agent import fundamentals_agent
from app.agents.quants.technicals_agent.agent import technicals_agent
from app.agents.quants.growth_agent.agent import growth_agent
from app.agents.quants.valuations_agent.agent import valuations_agent

# Note, needs a watch list to be fed in
# TODO: Implement an algorithmic or AI strategy to dynamically choose these
quants_orchestrator_agent = ParallelAgent(
    name="quants_orchestrator_agent",
    sub_agents=[fundamentals_agent, technicals_agent, growth_agent, valuations_agent],
)
