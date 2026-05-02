from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.plugins import ReflectAndRetryToolPlugin
from uuid import uuid4
import asyncio
import json
from pathlib import Path
from dotenv import load_dotenv
from google.genai import types
from loguru import logger

from app.runner.runner import run_stage
from app.models.quants_models import Ticker, Dossier
from app.models.investors_models import CIOOutput
from app.models.management_models import PortfolioManagerOutput
from app.agents.quants.quants_orchestrator_agent.agent import quants_orchestrator_agent
from app.agents.investors.investors_orchestrator_agent.agent import investors_orchestrator_agent
from app.agents.management.portfolio_manager_agent.agent import portfolio_manager_agent
from app.clients.trading212_client import Trading212Client
from app.models.trading212_models import (
    MarketOrderPayload,
    LimitOrderPayload,
    StopLimitOrderPayload,
)

load_dotenv(".env.local")

APP_NAME = "ai_hedge_fund"
USER_ID = str(uuid4())
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

STOCKS = [
    Ticker(name="Apple", trading212_ticker="AAPL", yfinance_ticker="AAPL"),
    Ticker(name="Microsoft", trading212_ticker="MSFT", yfinance_ticker="MSFT"),
    Ticker(name="Nvidia", trading212_ticker="NVDA", yfinance_ticker="NVDA"),
    Ticker(name="Tesla", trading212_ticker="TSLA", yfinance_ticker="TSLA"),
    Ticker(name="Amazon", trading212_ticker="AMZN", yfinance_ticker="AMZN"),
]

session_service = InMemorySessionService()

# =========================================================
# STAGE 1: QUANTS
# =========================================================
logger.info("=" * 60)
logger.info("STAGE 1: QUANT ANALYSIS")
logger.info("=" * 60)

session_id_1 = str(uuid4())
asyncio.run(session_service.create_session(
    app_name=APP_NAME, session_id=session_id_1, user_id=USER_ID,
))
runner_quants = Runner(
    agent=quants_orchestrator_agent,
    app_name=APP_NAME,
    session_service=session_service,
    plugins=[ReflectAndRetryToolPlugin(max_retries=3)],
)

state_1 = run_stage(
    APP_NAME,
    USER_ID,
    runner_quants,
    session_service,
    session_id_1,
    f"Run quant analysis on watchlist: {[t.model_dump() for t in STOCKS]}",
)

dossier_json = state_1["dossier"]
(OUTPUT_DIR / "dossier.json").write_text(dossier_json)
logger.info("Quants complete. Dossier saved to outputs/dossier.json")

# =========================================================
# STAGE 2: INVESTORS
# =========================================================
logger.info("=" * 60)
logger.info("STAGE 2: INVESTOR BOARDROOM")
logger.info("=" * 60)

session_id_2 = str(uuid4())
asyncio.run(session_service.create_session(
    app_name=APP_NAME,
    session_id=session_id_2,
    user_id=USER_ID,
    state={"dossier": dossier_json},
))
runner_investors = Runner(
    agent=investors_orchestrator_agent,
    app_name=APP_NAME,
    session_service=session_service,
    plugins=[ReflectAndRetryToolPlugin(max_retries=3)],
)

state_2 = run_stage(
    APP_NAME,
    USER_ID,
    runner_investors,
    session_service,
    session_id_2,
    "Review the dossier and produce investment recommendations.",
)

cio_output_raw = state_2["chief_investment_officer_output"]
(OUTPUT_DIR / "cio_output.json").write_text(json.dumps(cio_output_raw))
logger.info("Investors complete. CIO output saved to outputs/cio_output.json")

# =========================================================
# STAGE 3: PORTFOLIO MANAGER
# =========================================================
logger.info("=" * 60)
logger.info("STAGE 3: PORTFOLIO MANAGEMENT")
logger.info("=" * 60)

session_id_3 = str(uuid4())
asyncio.run(session_service.create_session(
    app_name=APP_NAME,
    session_id=session_id_3,
    user_id=USER_ID,
    state={"chief_investment_officer_output": cio_output_raw},
))
runner_portfolio = Runner(
    agent=portfolio_manager_agent,
    app_name=APP_NAME,
    session_service=session_service,
    plugins=[ReflectAndRetryToolPlugin(max_retries=3)],
)

state_3 = run_stage(
    APP_NAME,
    USER_ID,
    runner_portfolio,
    session_service,
    session_id_3,
    "Review the CIO recommendations and manage the portfolio accordingly.",
)

portfolio_output_raw = state_3["portfolio_manager_output"]
(OUTPUT_DIR / "portfolio_output.json").write_text(json.dumps(portfolio_output_raw))
logger.info("Portfolio management complete.")

# =========================================================
# FINAL OUTPUT
# =========================================================
logger.info("=" * 60)
logger.info("PIPELINE COMPLETE — FINAL DECISIONS")
logger.info("=" * 60)

# Quant dossier
logger.info("\nQUANT DOSSIER")
logger.info("-" * 40)
dossier = Dossier.model_validate_json(dossier_json)
for ticker_dossier in dossier.final_dossier:
    logger.info(f"\n{ticker_dossier.fundamentals.trading212_ticker}")
    logger.info(f"  Fundamentals: {ticker_dossier.fundamentals.summary}")
    logger.info(f"  Technicals:   {ticker_dossier.technicals.trend}")
    logger.info(f"  Growth:       {ticker_dossier.growth.catalysts}")
    logger.info(f"  Valuations:   {ticker_dossier.valuations.assessment}")

# CIO decisions
logger.info("\nCIO INVESTMENT DECISIONS")
logger.info("-" * 40)
cio_output = CIOOutput.model_validate(cio_output_raw)
for decision in cio_output.decisions:
    logger.info(
        f"\n{decision.trading212_ticker}: {decision.final_rating} "
        f"| Consensus: {decision.consensus_strength} "
        f"| Target: £{decision.target_price} "
        f"| Size: {decision.position_size_pct}%"
    )
    logger.info(f"  Debate: {decision.debate_summary}")

# Portfolio decisions
logger.info("\nPORTFOLIO MANAGER DECISIONS")
logger.info("-" * 40)
portfolio_output = PortfolioManagerOutput.model_validate(portfolio_output_raw)
logger.info(f"Account Value:   £{portfolio_output.account_value:,.2f}")
logger.info(f"Cash Available:  £{portfolio_output.cash_available:,.2f}")
logger.info(f"Positions:       {portfolio_output.current_positions_summary}")

if portfolio_output.instructions:
    logger.info("\nTRADE INSTRUCTIONS:")
    for instruction in portfolio_output.instructions:
        logger.info(
            f"  {instruction.action} {instruction.quantity} x "
            f"{instruction.trading212_ticker} @ £{instruction.limit_price} "
            f"| {instruction.order_type} "
            f"| Size: {instruction.target_position_size_pct}% "
            f"| Risk Approved: {instruction.risk_approved}"
        )
        logger.info(f"    Rationale: {instruction.rationale}")
        if instruction.risk_notes:
            logger.info(f"    Risk Notes: {instruction.risk_notes}")
else:
    logger.info("No trade instructions generated.")

if portfolio_output.deferred_instructions:
    logger.info("\nDEFERRED:")
    for deferred in portfolio_output.deferred_instructions:
        logger.info(f"  - {deferred}")

logger.info(f"\nSummary:     {portfolio_output.portfolio_summary}")
logger.info(f"Next Review: {portfolio_output.next_review_trigger}")

# =========================================================
# STAGE 4: TRADE EXECUTION
# =========================================================
logger.info("=" * 60)
logger.info("STAGE 4: TRADE EXECUTION")
logger.info("=" * 60)

trading212_client = Trading212Client()

if portfolio_output.instructions:
    for instruction in portfolio_output.instructions:
        if not instruction.risk_approved:
            logger.warning(f"Skipping trade for {instruction.trading212_ticker}: Not risk approved by Risk Manager.")
            continue
        
        if instruction.action == "HOLD":
            continue

        # Adjust quantity for Sell/Reduce (assuming negative for sell in T212 API)
        quantity = instruction.quantity
        if instruction.action in ["SELL", "REDUCE"] and quantity > 0:
            quantity = -quantity
        elif instruction.action in ["BUY", "ADD"] and quantity < 0:
            quantity = -quantity
        
        logger.info(f"Executing {instruction.action} {abs(quantity)} x {instruction.trading212_ticker} via {instruction.order_type}...")
        
        try:
            if instruction.order_type == "MARKET":
                # MarketOrderPayload in this project requires a limitPrice > 0
                payload = MarketOrderPayload(
                    limitPrice=instruction.limit_price or 0.01, 
                    quantity=quantity,
                    ticker=instruction.trading212_ticker,
                    timeValidity=instruction.time_validity
                )
                result = trading212_client.place_market_order(payload)
            elif instruction.order_type == "LIMIT":
                payload = LimitOrderPayload(
                    limitPrice=instruction.limit_price,
                    quantity=quantity,
                    ticker=instruction.trading212_ticker,
                    extendedHours=instruction.extended_hours
                )
                result = trading212_client.place_limit_order(payload)
            elif instruction.order_type == "STOP_LIMIT":
                payload = StopLimitOrderPayload(
                    limitPrice=instruction.limit_price,
                    stopPrice=instruction.stop_price,
                    quantity=quantity,
                    ticker=instruction.trading212_ticker,
                    timeValidity=instruction.time_validity
                )
                result = trading212_client.place_stop_limit_order(payload)
            else:
                logger.error(f"Unsupported order type: {instruction.order_type}")
                continue
            
            logger.info(f"Successfully placed order for {instruction.trading212_ticker}. Result: {result}")
        except Exception as e:
            logger.error(f"Failed to execute trade for {instruction.trading212_ticker}: {e}")
else:
    logger.info("No trade instructions to execute.")

# =========================================================
# CLEANUP
# =========================================================
for f in ["dossier.json", "cio_output.json", "portfolio_output.json"]:
    path = OUTPUT_DIR / f
    if path.exists():
        path.unlink()
        logger.info(f"Cleaned up {f}")

if OUTPUT_DIR.exists() and not any(OUTPUT_DIR.iterdir()):
    OUTPUT_DIR.rmdir()
    logger.info("Removed empty outputs directory")