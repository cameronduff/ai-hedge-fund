from google.adk.agents import ParallelAgent, SequentialAgent, LlmAgent

from app.agents.investors.chief_investment_officer.agent import (
    chief_investment_officer_agent,
)
from app.agents.investors.aswath_damodaran_agent.agent import aswath_damodaran_agent
from app.agents.investors.ben_graham_agent.agent import ben_graham_agent
from app.agents.investors.bill_ackman_agent.agent import bill_ackman_agent
from app.agents.investors.cathie_wood_agent.agent import cathie_wood_agent
from app.agents.investors.charlie_munger_agent.agent import charlie_munger_agent
from app.agents.investors.michael_burry_agent.agent import michael_burry_agent
from app.agents.investors.monish_pabrai_agent.agent import monish_pabrai_agent
from app.agents.investors.nassim_taleb_agent.agent import nassim_taleb_agent
from app.agents.investors.peter_lynch_agent.agent import peter_lynch_agent
from app.agents.investors.phil_fisher_agent.agent import phil_fisher_agent
from app.agents.investors.rakesh_jhunjhunwala_agent.agent import (
    rakesh_jhunjhunwala_agent,
)
from app.agents.investors.stanley_druckenmiller_agent.agent import (
    stanley_druckenmiller_agent,
)
from app.agents.investors.warren_buffet_agent.agent import warren_buffet_agent

investor_boardroom = ParallelAgent(
    name="investor_boardroom",
    sub_agents=[
        aswath_damodaran_agent,
        ben_graham_agent,
        bill_ackman_agent,
        cathie_wood_agent,
        charlie_munger_agent,
        michael_burry_agent,
        monish_pabrai_agent,
        nassim_taleb_agent,
        peter_lynch_agent,
        phil_fisher_agent,
        rakesh_jhunjhunwala_agent,
        stanley_druckenmiller_agent,
        warren_buffet_agent,
    ],
)

investors_orchestrator_agent = SequentialAgent(
    name="investors_orchestrator_agent",
    sub_agents=[investor_boardroom, chief_investment_officer_agent],
)

if __name__=="__main__":
    from app.models.quants_models import Ticker, Dossier, TickerDossier, FundamentalsAgentOutput, FundamentalsMetrics, TechnicalAgentOutput, TechnicalMetrics, ValuationAgentOutput, ValuationMetrics, GrowthAgentOutput, GrowthMetrics
    
    final_dossier=[
        TickerDossier(
            fundamentals=FundamentalsAgentOutput(
                trading212_ticker='AAPL', 
                yfinance_ticker='AAPL', 
                metrics=FundamentalsMetrics(
                    total_debt=84710998016.0, 
                    cash_and_equivalents=68507000832.0, 
                    debt_to_equity=79.548, 
                    net_income_ttm=122575003648.0, 
                    return_on_equity_pct=141.47099, 
                    operating_margin_pct=32.275, 
                    current_ratio=1.07
                ), 
                summary='Apple Inc. maintains a "Fortress" balance sheet characterized by a manageable debt-to-equity ratio of 0.80 and a current ratio of 1.07, ensuring solid short-term liquidity. The company\'s operational efficiency is exceptional, boasting industry-leading operating margins of 32.28% and a return on equity of 141.47%, which underscores its massive cash-generating power and efficient use of shareholder capital.'), 
            technicals=TechnicalAgentOutput(
                trading212_ticker='AAPL', 
                yfinance_ticker='AAPL', 
                indicators=TechnicalMetrics(
                    current_price=284.13, 
                    rsi_14=71.35, 
                    macd='Bullish', 
                    sma_50=262.35, 
                    sma_200=241.5, 
                    fifty_two_week_high=288.35, 
                    volume_24h_change_pct=-57.28), 
                    trend='AAPL is in a strong uptrend, trading well above its 50-day and 200-day moving averages. However, the RSI of 71.35 indicates overbought conditions as the price approaches the 52-week high resistance of 288.35.'), 
            growth=GrowthAgentOutput(
                trading212_ticker='AAPL', 
                yfinance_ticker='AAPL', 
                forecast=GrowthMetrics(revenue_growth_yoy_pct=16.6, 
                analyst_mean_target=298.46, 
                analyst_consensus='Buy', 
                next_earnings_date='2026-07-30', 
                estimated_eps_growth_next_5y=14.74), 
                catalysts="Apple is experiencing a significant revenue resurgence (16.6% YoY) driven by the AI-led iPhone upgrade cycle and high-margin Services momentum. Analysts maintain a strong 'Buy' consensus, anticipating that the integration of 'Apple Intelligence' will sustain double-digit earnings growth over the next five years."), 
            valuations=ValuationAgentOutput(trading212_ticker='AAPL', 
                yfinance_ticker='AAPL', 
                multiples=ValuationMetrics(trailing_pe=35.97, 
                forward_pe=30.24, 
                peg_ratio=2.44, 
                price_to_book=47.37, 
                intrinsic_value_estimate=245.5, 
                valuation_status='Overvalued'), 
                assessment="AAPL is currently trading at a significant premium with a PEG ratio of 2.44, well above the 'expensive' threshold of 2.0. While forward earnings growth is healthy at 21.8%, the extreme Price-to-Book ratio of 47.37 and high P/E multiples suggest the market has already priced in aggressive growth, leaving a minimal margin of safety.")), 
        TickerDossier(
            fundamentals=FundamentalsAgentOutput(
                trading212_ticker='MSFT', 
                yfinance_ticker='MSFT', 
                metrics=FundamentalsMetrics(total_debt=125431996416.0, 
                cash_and_equivalents=78227996672.0, 
                debt_to_equity=30.271, 
                net_income_ttm=125215997952.0, 
                return_on_equity_pct=34.013999, 
                operating_margin_pct=46.326, 
                current_ratio=1.283
                ), 
                summary='Microsoft Corporation maintains a "Fortress" balance sheet with a conservative debt-to-equity ratio of 0.30 and a current ratio of 1.28, indicating excellent solvency and short-term liquidity. The company\'s operational efficiency remains top-tier, characterized by a 46.33% operating margin and a 34.01% return on equity, reflecting its massive cash-generating power and dominant position in the cloud and software sectors.'), 
            technicals=TechnicalAgentOutput(trading212_ticker='MSFT', 
                yfinance_ticker='MSFT', 
                indicators=TechnicalMetrics(current_price=413.69, 
                rsi_14=62.55, 
                macd='Bullish', 
                sma_50=396.6, 
                sma_200=465.0, 
                fifty_two_week_high=552.24, 
                volume_24h_change_pct=-62.0), 
                trend='MSFT is currently in a recovery phase, having reclaimed its 50-day SMA but remaining below the 200-day SMA. The stock is showing signs of a trend reversal with bullish MACD momentum, though recent volume has significantly tapered off.'), 
                growth=GrowthAgentOutput(trading212_ticker='MSFT', 
                yfinance_ticker='MSFT', 
            forecast=GrowthMetrics(revenue_growth_yoy_pct=18.3, 
                analyst_mean_target=570.72, 
                analyst_consensus='Strong Buy', 
                next_earnings_date='2026-07-29', 
                estimated_eps_growth_next_5y=19.15), 
                catalysts="Microsoft is a premier 'Compounder' leveraging its first-mover advantage in Generative AI to drive Azure cloud expansion and Copilot monetization. With revenue growing at 18.3% YoY and a dominant position in enterprise software, the company is well-positioned to capture significant share in the evolving AI economy."), 
                valuations=ValuationAgentOutput(trading212_ticker='MSFT', 
                yfinance_ticker='MSFT', 
                multiples=ValuationMetrics(trailing_pe=24.62, 
                forward_pe=21.44, 
                peg_ratio=1.29, 
                price_to_book=7.86, 
                intrinsic_value_estimate=525.0, 
                valuation_status='Undervalued'), 
                assessment='MSFT is currently trading at a compelling Forward P/E of 21.44, which is notably low for its historical growth profile and dominant market position. With a PEG ratio of 1.29 and a significant 38% discount to the analyst mean target of $570.72, the stock offers a robust margin of safety for a high-margin software leader.'))
            ]
    
    master_dossier = Dossier(final_dossier=final_dossier)

    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.adk.plugins import ReflectAndRetryToolPlugin
    from uuid import uuid4
    import asyncio
    from dotenv import load_dotenv
    from google.genai import types
    from loguru import logger

    load_dotenv(".env.local")

    APP_NAME = "ai_hedge_fund"
    USER_ID = str(uuid4())
    SESSION_ID = str(uuid4())

    session_service = InMemorySessionService()
    session = asyncio.run(
        session_service.create_session(
            app_name=APP_NAME, 
            session_id=SESSION_ID, 
            user_id=USER_ID, 
            state={"dossier": master_dossier.model_dump_json()},
        )
    )
    runner = Runner(
        agent=investors_orchestrator_agent,
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

    chief_investment_officer_output = Dossier.model_validate_json(final_session.state["chief_investment_officer_output"])
    logger.info("======================================================")
    logger.info(chief_investment_officer_output)