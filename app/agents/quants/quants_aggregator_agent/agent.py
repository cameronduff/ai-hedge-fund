from google.adk.agents import BaseAgent
from google.adk.events import Event, EventActions
from google.genai import types
import json
from typing import List
from loguru import logger

from app.models.quants_models import FundamentalsAgentOutput, TechnicalAgentOutput, GrowthAgentOutput, ValuationAgentOutput, TickerDossier, Ticker, Dossier

class QuantsAggregatorAgent(BaseAgent):
    ticker: Ticker

    async def _run_async_impl(self, ctx):
        ticker_name = self.ticker.yfinance_ticker.replace(".", "_")

        fundamentals = None
        fund_key = f"fundamentals_agent_output_{ticker_name}"
        if fund_key in ctx.session.state and ctx.session.state[fund_key]:
            try:
                fundamentals = FundamentalsAgentOutput.model_validate(ctx.session.state[fund_key])
            except Exception as e:
                logger.warning(f"Error parsing fundamentals for {ticker_name}: {e}")

        technicals = None
        tech_key = f"technicals_agent_output_{ticker_name}"
        if tech_key in ctx.session.state and ctx.session.state[tech_key]:
            try:
                technicals = TechnicalAgentOutput.model_validate(ctx.session.state[tech_key])
            except Exception as e:
                logger.warning(f"Error parsing technicals for {ticker_name}: {e}")

        growth = None
        growth_key = f"growth_agent_output_{ticker_name}"
        if growth_key in ctx.session.state and ctx.session.state[growth_key]:
            try:
                growth = GrowthAgentOutput.model_validate(ctx.session.state[growth_key])
            except Exception as e:
                logger.warning(f"Error parsing growth for {ticker_name}: {e}")

        valuations = None
        val_key = f"valuations_agent_output_{ticker_name}"
        if val_key in ctx.session.state and ctx.session.state[val_key]:
            try:
                valuations = ValuationAgentOutput.model_validate(ctx.session.state[val_key])
            except Exception as e:
                logger.warning(f"Error parsing valuations for {ticker_name}: {e}")

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
            ticker_name = stock.yfinance_ticker.replace(".", "_")
            key = f"quants_final_output_{ticker_name}"
            if key in ctx.session.state and ctx.session.state[key]:
                try:
                    quants_analysis = TickerDossier.model_validate_json(
                        ctx.session.state[key]
                    )
                    dossier.final_dossier.append(quants_analysis)
                except Exception as e:
                    logger.warning(f"Failed to parse {key}: {e}")
            else:
                logger.warning(f"No quant final output found for {ticker_name}")

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