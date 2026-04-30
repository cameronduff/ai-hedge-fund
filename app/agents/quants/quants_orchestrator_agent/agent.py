from google.adk.agents import ParallelAgent, SequentialAgent
from google.genai import types

from app.agents.quants.fundamentals_agent.agent import fundamentals_agent
from app.agents.quants.technicals_agent.agent import technicals_agent
from app.agents.quants.growth_agent.agent import growth_agent
from app.agents.quants.valuations_agent.agent import valuations_agent
from app.agents.quants.quants_aggregator_agent.agent import quants_aggregator_agent
from app.models.quants_models import Ticker

from loguru import logger

# Note, needs a watch list to be fed in
# TODO: Implement an algorithmic or AI strategy to dynamically choose these
quants_parallel_agent = ParallelAgent(
    name="quants_parallel_agent",
    sub_agents=[
        fundamentals_agent, 
        technicals_agent, 
        growth_agent, 
        valuations_agent
    ],
)

quants_orchestrator_agent = SequentialAgent(
    name="quants_orchestrator_agent", 
    sub_agents=[
        quants_parallel_agent,
        quants_aggregator_agent
    ]
)

if __name__ == "__main__":
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.adk.plugins import ReflectAndRetryToolPlugin
    from uuid import uuid4
    import asyncio
    from dotenv import load_dotenv

    load_dotenv()

    APP_NAME = "ai_hedge_fund"
    USER_ID = str(uuid4())
    SESSION_ID = str(uuid4())

    STOCKS = [
        # --- US TECH & GROWTH ---
        Ticker(name="Apple", trading212_ticker="AAPL", yfinance_ticker="AAPL"),
        Ticker(name="Microsoft", trading212_ticker="MSFT", yfinance_ticker="MSFT"),
        Ticker(name="Nvidia", trading212_ticker="NVDA", yfinance_ticker="NVDA"),
        Ticker(name="Tesla", trading212_ticker="TSLA", yfinance_ticker="TSLA"),
        Ticker(name="Amazon", trading212_ticker="AMZN", yfinance_ticker="AMZN"),
        Ticker(name="Alphabet A", trading212_ticker="GOOGL", yfinance_ticker="GOOGL"),
        Ticker(name="Meta", trading212_ticker="META", yfinance_ticker="META"),
        Ticker(name="AMD", trading212_ticker="AMD", yfinance_ticker="AMD"),
        Ticker(
            name="Berkshire Hathaway B",
            trading212_ticker="BRK.B",
            yfinance_ticker="BRK-B",
        ),
        Ticker(name="Netflix", trading212_ticker="NFLX", yfinance_ticker="NFLX"),
        # --- UK BLUE CHIPS ---
        Ticker(name="Tesco", trading212_ticker="TSCO", yfinance_ticker="TSCO.L"),
        Ticker(name="Rolls-Royce", trading212_ticker="RR", yfinance_ticker="RR.L"),
        Ticker(name="BP", trading212_ticker="BP", yfinance_ticker="BP.L"),
        Ticker(name="HSBC", trading212_ticker="HSBA", yfinance_ticker="HSBA.L"),
        Ticker(name="AstraZeneca", trading212_ticker="AZN", yfinance_ticker="AZN.L"),
        Ticker(name="Barclays", trading212_ticker="BARC", yfinance_ticker="BARC.L"),
        Ticker(
            name="Lloyds Banking Group",
            trading212_ticker="LLOY",
            yfinance_ticker="LLOY.L",
        ),
        Ticker(name="Vodafone", trading212_ticker="VOD", yfinance_ticker="VOD.L"),
        Ticker(name="Glencore", trading212_ticker="GLEN", yfinance_ticker="GLEN.L"),
        Ticker(name="GSK", trading212_ticker="GSK", yfinance_ticker="GSK.L"),
        Ticker(
            name="Legal & General",
            trading212_ticker="LGEN",
            yfinance_ticker="LGEN.L",
        ),
        Ticker(name="National Grid", trading212_ticker="NG", yfinance_ticker="NG.L"),
    ]

    TICKER = Ticker(name="Apple", trading212_ticker="AAPL", yfinance_ticker="AAPL")

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
        plugins=[ReflectAndRetryToolPlugin(max_retries=3)]
    )

    content = types.Content(
        role="user", parts=[types.Part(text=TICKER.model_dump_json())]
    )

    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    for event in events:
        if event.is_final_response() and event.content:
            response = event.content.parts[0].text.strip()
            logger.info(response)
