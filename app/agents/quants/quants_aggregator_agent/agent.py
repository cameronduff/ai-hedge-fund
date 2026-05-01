from google.adk.agents import BaseAgent
from google.adk.events import Event, EventActions
from google.genai import types
import json
from typing import List

from app.models.quants_models import FundamentalsAgentOutput, TechnicalAgentOutput, GrowthAgentOutput, ValuationAgentOutput, TickerDossier, Ticker, Dossier

class QuantsAggregatorAgent(BaseAgent):
    ticker: Ticker

    async def _run_async_impl(self, ctx):
        ticker_name = self.ticker.yfinance_ticker

        fundamentals = FundamentalsAgentOutput.model_validate(ctx.session.state[f"fundamentals_agent_output_{ticker_name}"])
        technicals = TechnicalAgentOutput.model_validate(ctx.session.state[f"technicals_agent_output_{ticker_name}"])
        growth = GrowthAgentOutput.model_validate(ctx.session.state[f"growth_agent_output_{ticker_name}"])
        valuations = ValuationAgentOutput.model_validate(ctx.session.state[f"valuations_agent_output_{ticker_name}"])

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
                state_delta={f"quants_final_output_{ticker_name}": final.model_dump_json()}
            )
        )


class DossierAggregatorAgent(BaseAgent):
    stocks: List[Ticker]
    async def _run_async_impl(self, ctx):
        dossier = Dossier(final_dossier=[])
        for stock in self.stocks:
            ticker_name = stock.yfinance_ticker

            quants_analysis = TickerDossier.model_validate_json(
                ctx.session.state[f"quants_final_output_{ticker_name}"]
            )
            dossier.final_dossier.append(quants_analysis)

        yield Event(
            author=self.name,
            content = types.Content(
                role="model",
                parts=[types.Part(text=dossier.model_dump_json())]
            ),
            actions=EventActions(
                state_delta={"dossier": dossier.model_dump_json()}
            )
        )