from google.adk.agents import BaseAgent
from google.adk.events import Event, EventActions
from google.genai import types
import json

from app.models.quants_models import FundamentalsAgentOutput, TechnicalAgentOutput, GrowthAgentOutput, ValuationAgentOutput, TickerDossier

class QuantsAggregatorAgent(BaseAgent):
    async def _run_async_impl(self, ctx):
        fundamentals = FundamentalsAgentOutput.model_validate(ctx.session.state["fundamentals_agent_output"])
        technicals = TechnicalAgentOutput.model_validate(ctx.session.state["technicals_agent_output"])
        growth = GrowthAgentOutput.model_validate(ctx.session.state["growth_agent_output"])
        valuations = ValuationAgentOutput.model_validate(ctx.session.state["valuations_agent_output"])

        final = TickerDossier(
            fundamentals=fundamentals, 
            technicals=technicals, 
            growth=growth, 
            valuations=valuations
        )

        yield Event(
            author=self.name,
            content = types.Content(
                role="model",
                parts=[types.Part(text=final.model_dump_json())]
            ),
            actions=EventActions(
                state_delta={"quants_final_output": final.model_dump_json()}
            )
        )

quants_aggregator_agent = QuantsAggregatorAgent(name="quants_aggregator_agent")