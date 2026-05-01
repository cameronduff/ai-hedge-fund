# TODO: Implement an algorithmic or AI strategy to dynamically choose these
from google.adk.agents import ParallelAgent, SequentialAgent
from google.genai import types

from app.agents.quants.fundamentals_agent.agent import build_fundamentals_agent
from app.agents.quants.technicals_agent.agent import build_technicals_agent
from app.agents.quants.growth_agent.agent import build_growth_agent
from app.agents.quants.valuations_agent.agent import build_valuations_agent
from app.agents.quants.quants_aggregator_agent.agent import QuantsAggregatorAgent, DossierAggregatorAgent
from app.models.quants_models import Ticker, Dossier

from loguru import logger

STOCKS = [
    # --- US TECH & GROWTH ---
    Ticker(name="Apple", trading212_ticker="AAPL", yfinance_ticker="AAPL"),
    Ticker(name="Microsoft", trading212_ticker="MSFT", yfinance_ticker="MSFT"),
    # Ticker(name="Nvidia", trading212_ticker="NVDA", yfinance_ticker="NVDA"),
    # Ticker(name="Tesla", trading212_ticker="TSLA", yfinance_ticker="TSLA"),
    # Ticker(name="Amazon", trading212_ticker="AMZN", yfinance_ticker="AMZN"),
]


def build_ticker_pipeline(ticker: Ticker) -> SequentialAgent:
    t = ticker.yfinance_ticker

    quants_team = ParallelAgent(
        name=f"quants_{t}",
        sub_agents=[
            build_fundamentals_agent(t),
            build_technicals_agent(t),
            build_growth_agent(t),
            build_valuations_agent(t),
        ]
    )

    quants_aggregator_agent = QuantsAggregatorAgent(
        name=f"quants_aggregator_{t}",
        ticker=ticker
    )

    return SequentialAgent(
        name=f"quants_pipeline_{t}",
        sub_agents=[
            quants_team,
            quants_aggregator_agent,
        ]
    )

quants_orchestrator_agent = SequentialAgent(
    name="quants_orchestrator_agent",
    sub_agents=[
        *[build_ticker_pipeline(ticker) for ticker in STOCKS], 
        DossierAggregatorAgent(name="dossier_aggregator", stocks=STOCKS)
    ],
)

root_agent = quants_orchestrator_agent

if __name__ == "__main__":
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.adk.plugins import ReflectAndRetryToolPlugin
    from uuid import uuid4
    import asyncio
    from dotenv import load_dotenv

    load_dotenv(".env.local")

    APP_NAME = "ai_hedge_fund"
    USER_ID = str(uuid4())
    SESSION_ID = str(uuid4())

    session_service = InMemorySessionService()
    session = asyncio.run(
        session_service.create_session(
            app_name=APP_NAME, session_id=SESSION_ID, user_id=USER_ID
        )
    )
    runner = Runner(
        agent=quants_orchestrator_agent,
        app_name=APP_NAME,
        session_service=session_service,
        plugins=[ReflectAndRetryToolPlugin(max_retries=3)],
    )

    content = types.Content(
        role="user", parts=[types.Part(text="Run quant analysis on watchlist.")]
    )

    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    for event in events:
        if event.is_final_response() and event.content:
            response = event.content.parts[0].text.strip()
            logger.info(response)
    
    final_session = asyncio.run(
        session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )
    )

    dossier = Dossier.model_validate_json(final_session.state["dossier"])
    logger.info("======================================================")
    logger.info(dossier)