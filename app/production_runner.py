import argparse
import asyncio
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv
from google.adk.plugins import ReflectAndRetryToolPlugin
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from loguru import logger

# Load environment first
load_dotenv(".env.local")
load_dotenv(".env")

# Initialize Langfuse Observability & OpenTelemetry Instrumentation
langfuse_client = None
try:
    from openinference.instrumentation.google_adk import GoogleADKInstrumentor
    GoogleADKInstrumentor().instrument()
    from langfuse import get_client
    langfuse_client = get_client()
    if langfuse_client.auth_check():
        logger.info("Langfuse tracing authenticated and active (https://cloud.langfuse.com)")
    else:
        logger.warning("Langfuse credentials check failed; tracing may be degraded.")
except Exception as e:
    logger.warning(f"Langfuse instrumentation could not be initialized: {e}")

from app.core.config import settings
from app.core.rate_limiter import RateLimitPacerPlugin
from app.agents.investors.investors_orchestrator_agent.agent import (
    investors_orchestrator_agent,
)

from app.agents.management.portfolio_manager_agent.agent import portfolio_manager_agent
from app.agents.quants.quants_orchestrator_agent.agent import (
    build_quants_orchestrator_agent,
)
from app.clients.trading212_client import Trading212Client
from app.models.investors_models import CIOOutput
from app.models.management_models import PortfolioManagerOutput
from app.models.quants_models import Dossier, Ticker
from app.models.trading212_models import (
    LimitOrderPayload,
    MarketOrderPayload,
    StopLimitOrderPayload,
)
from app.runner.runner import run_stage
from app.services.watchlist_service import WatchlistService


def generate_executive_summary(
    run_timestamp: str,
    environment: str,
    is_dry_run: bool,
    account_summary: dict,
    stocks: list[Ticker],
    dossier: Dossier | None,
    cio_output: CIOOutput | None,
    portfolio_output: PortfolioManagerOutput | None,
    executed_trades: list[dict],
    api_stats: dict | None = None,
) -> str:
    """
    Builds a comprehensive, human-readable markdown summary of the weekly run.
    """
    total_val = account_summary.get("totalValue", 0.0) if account_summary else 0.0
    cash_val = (
        account_summary.get("cash", {}).get("availableToTrade", 0.0)
        if account_summary
        else 0.0
    )
    currency = account_summary.get("currency", "GBP") if account_summary else "GBP"

    md = []
    md.append(f"# AI Hedge Fund — Weekly Run Report")
    md.append(f"**Timestamp:** `{run_timestamp}`  ")
    md.append(f"**Environment:** `{environment.upper()}` {'(DRY RUN - No Real Money)' if is_dry_run else '(LIVE EXECUTION)'}  ")
    md.append(f"**Models:** Quants=`{settings.QUANTS_MODEL}` | Decisions=`{settings.DECISION_MODEL}` with Thinking  ")
    md.append(f"**Observability:** Langfuse Tracing Active (`https://cloud.langfuse.com`)  ")

    if api_stats:
        calls = api_stats.get("call_count", 0)
        pacing = api_stats.get("pacing_seconds", 0.0)
        duration = api_stats.get("duration", "N/A")
        md.append(f"**API Usage & Budget:** `{calls}` LLM calls ({duration} total, {pacing:.1f}s rate-limit pacing applied, strictly ≤ 13.3 RPM)  ")
    md.append("\n---\n")

    # Account Overview
    md.append("## 1. Account & Portfolio Status")
    md.append(f"- **Total Account Value:** {currency} {total_val:,.2f}")
    md.append(f"- **Available Cash:** {currency} {cash_val:,.2f}")
    if portfolio_output and portfolio_output.current_positions_summary:
        md.append(f"- **Holdings Overview:** {portfolio_output.current_positions_summary}")

    md.append("\n---\n")

    # Watchlist Evaluated
    md.append("## 2. Watchlist Candidates Analyzed")
    for s in stocks:
        news_line = ""
        catalysts_line = ""
        if dossier and dossier.final_dossier:
            for td in dossier.final_dossier:
                if td.fundamentals and td.fundamentals.yfinance_ticker == s.yfinance_ticker and td.news:
                    metrics = td.news.metrics
                    news_line = f" | News Sentiment: **{metrics.sentiment_label}** ({metrics.sentiment_score:+.2f}, Conf: {metrics.confidence:.0%})"
                    if metrics.major_catalysts:
                        catalysts_line += f"\n  - *Catalysts:* {', '.join(metrics.major_catalysts[:3])}"
                    if metrics.risk_factors:
                        catalysts_line += f"\n  - *Headwinds/Risks:* {', '.join(metrics.risk_factors[:3])}"
                    break
        md.append(f"- **{s.name}** (`{s.trading212_ticker}` | Yahoo: `{s.yfinance_ticker}`){news_line}{catalysts_line}")
    md.append("\n---\n")

    # CIO Decisions
    md.append("## 3. CIO Investment Boardroom Consensus")
    if cio_output and cio_output.decisions:
        for d in cio_output.decisions:
            md.append(f"### {d.trading212_ticker} — Rating: **{d.final_rating}**")
            md.append(f"- **Target Price:** {currency} {d.target_price} | **Target Size:** {d.position_size_pct}%")
            md.append(f"- **Consensus Strength:** {d.consensus_strength}")
            md.append(f"- **Debate Summary:** {d.debate_summary}")
            md.append("")
    else:
        md.append("No CIO investment decisions recorded.")
    md.append("\n---\n")

    # Portfolio Manager Trade Instructions
    md.append("## 4. Trade Execution Summary")
    if executed_trades:
        md.append("| Action | Quantity | Ticker | Order Type | Limit Price | Status |")
        md.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
        for t in executed_trades:
            status_text = "Simulated (Dry-Run)" if is_dry_run else t.get("result", {}).get("status", "Placed")
            md.append(
                f"| **{t['action']}** | {t['quantity']} | `{t['ticker']}` | {t['order_type']} | {t.get('limit_price', 'Market')} | `{status_text}` |"
            )
    else:
        md.append("No trade orders were scheduled or executed during this run.")

    if portfolio_output and portfolio_output.portfolio_summary:
        md.append(f"\n**Portfolio Manager Commentary:**  \n{portfolio_output.portfolio_summary}")

    return "\n".join(md)


def _run_hedge_fund_internal(
    dry_run: bool = True,
    max_candidates: int | None = None,
    environment: str | None = None,
):
    run_dt = datetime.now()
    run_timestamp = run_dt.strftime("%Y-%m-%d_%H%M%S")
    runs_dir = Path("runs") / run_timestamp
    runs_dir.mkdir(parents=True, exist_ok=True)

    if environment:
        settings.TRADING_212_ENVIRONMENT = environment
    env_str = settings.TRADING_212_ENVIRONMENT.strip().lower()

    if max_candidates is None:
        max_candidates = settings.MAX_CANDIDATES

    logger.info("=" * 60)
    logger.info(f"AI HEDGE FUND PRODUCTION RUN — {run_timestamp}")
    logger.info(
        f"Environment: {env_str.upper()} | Dry-Run: {dry_run} | "
        f"Models: Quants={settings.QUANTS_MODEL}, Decisions={settings.DECISION_MODEL}"
    )
    logger.info("=" * 60)

    # 1. Pre-flight Checks
    t212_client = Trading212Client(dry_run=dry_run)
    account_summary = t212_client.get_account_summary()
    if not account_summary:
        logger.error("Failed to fetch account summary from Trading 212. Verify credentials and network.")
        sys.exit(1)

    logger.info(f"Connected to Trading 212 ({env_str.upper()}): Total Value = £{account_summary.get('totalValue', 0):,.2f}")

    # 2. Watchlist Filtering & Ranking
    logger.info("Step 1: Screening & ranking watchlist...")
    watchlist_service = WatchlistService()
    stocks = watchlist_service.filter_watchlist(max_tickers=max_candidates)

    if not stocks:
        logger.warning("No candidate stocks found for analysis. Exiting.")
        return

    logger.info(f"Selected {len(stocks)} candidate stocks for analysis: {[s.yfinance_ticker for s in stocks]}")

    start_time = time.time()

    # Shared Session & Plugins
    app_name = "ai_hedge_fund"
    user_id = str(uuid4())
    session_service = InMemorySessionService()

    # Plugins: Rate-limiting pacer ensures strict spacing between LLM calls to stay <= 13.3 RPM
    pacer = RateLimitPacerPlugin(min_interval_seconds=settings.RATE_LIMIT_DELAY_SECONDS)
    plugins = [
        pacer,
        ReflectAndRetryToolPlugin(max_retries=3),
    ]


    # 3. Stage 1: Quant Analysis
    logger.info("=" * 60)
    logger.info("STAGE 1: QUANT ANALYSIS")
    logger.info("=" * 60)

    session_id_1 = str(uuid4())
    asyncio.run(
        session_service.create_session(
            app_name=app_name, session_id=session_id_1, user_id=user_id
        )
    )
    runner_quants = Runner(
        agent=build_quants_orchestrator_agent(stocks),
        app_name=app_name,
        session_service=session_service,
        plugins=plugins,
    )
    state_1 = run_stage(
        app_name=app_name,
        user_id=user_id,
        runner=runner_quants,
        session_service=session_service,
        session_id=session_id_1,
        message=f"Run quant analysis on watchlist: {[t.model_dump() for t in stocks]}",
        stage_name="quants-analysis",
        metadata={
            "stocks": [s.yfinance_ticker for s in stocks],
            "num_candidates": len(stocks),
            "dry_run": dry_run,
        },
    )

    dossier_json = state_1.get("dossier", "{}")
    if not dossier_json or dossier_json == "{}":
        from app.models.quants_models import TickerDossier
        reconstructed = []
        for k, v in state_1.items():
            if k.startswith("quants_final_output_") and v:
                try:
                    reconstructed.append(TickerDossier.model_validate_json(v))
                except Exception:
                    pass
        if reconstructed:
            dossier = Dossier(final_dossier=reconstructed)
            dossier_json = dossier.model_dump_json()
            logger.info(f"Reconstructed dossier with {len(reconstructed)} stocks from successful quant analyses.")
        else:
            dossier = None
    else:
        dossier = Dossier.model_validate_json(dossier_json)

    (runs_dir / "dossier.json").write_text(dossier_json or "{}")
    logger.info(f"Quants analysis complete. Saved to {runs_dir / 'dossier.json'}")

    if not dossier or not dossier.final_dossier:
        logger.error("No valid stock quant analyses available. Halting pipeline before Stage 2.")
        return


    # 4. Stage 2: Investors Boardroom
    logger.info("=" * 60)
    logger.info("STAGE 2: INVESTOR BOARDROOM")
    logger.info("=" * 60)

    session_id_2 = str(uuid4())
    asyncio.run(
        session_service.create_session(
            app_name=app_name,
            session_id=session_id_2,
            user_id=user_id,
            state={"dossier": dossier_json},
        )
    )
    runner_investors = Runner(
        agent=investors_orchestrator_agent,
        app_name=app_name,
        session_service=session_service,
        plugins=plugins,
    )
    state_2 = run_stage(
        app_name=app_name,
        user_id=user_id,
        runner=runner_investors,
        session_service=session_service,
        session_id=session_id_2,
        message="Review the dossier and produce investment recommendations.",
        stage_name="investor-boardroom",
        metadata={
            "dry_run": dry_run,
        },
    )

    cio_output_raw = state_2.get("chief_investment_officer_output", {})
    (runs_dir / "cio_output.json").write_text(json.dumps(cio_output_raw, indent=2))
    cio_output = CIOOutput.model_validate(cio_output_raw) if cio_output_raw else None
    logger.info(f"Investors complete. Saved to {runs_dir / 'cio_output.json'}")

    # 5. Stage 3: Portfolio Management
    logger.info("=" * 60)
    logger.info("STAGE 3: PORTFOLIO MANAGEMENT")
    logger.info("=" * 60)

    session_id_3 = str(uuid4())
    asyncio.run(
        session_service.create_session(
            app_name=app_name,
            session_id=session_id_3,
            user_id=user_id,
            state={"chief_investment_officer_output": cio_output_raw},
        )
    )
    runner_portfolio = Runner(
        agent=portfolio_manager_agent,
        app_name=app_name,
        session_service=session_service,
        plugins=plugins,
    )
    state_3 = run_stage(
        app_name=app_name,
        user_id=user_id,
        runner=runner_portfolio,
        session_service=session_service,
        session_id=session_id_3,
        message="Review the CIO recommendations and manage the portfolio accordingly.",
        stage_name="portfolio-management",
        metadata={
            "dry_run": dry_run,
        },
    )

    portfolio_output_raw = state_3.get("portfolio_manager_output", {})
    (runs_dir / "portfolio_output.json").write_text(json.dumps(portfolio_output_raw, indent=2))
    portfolio_output = (
        PortfolioManagerOutput.model_validate(portfolio_output_raw)
        if portfolio_output_raw
        else None
    )
    logger.info(f"Portfolio management complete. Saved to {runs_dir / 'portfolio_output.json'}")

    # 6. Stage 4: Order Execution & Safety Guards
    logger.info("=" * 60)
    logger.info("STAGE 4: ORDER EXECUTION")
    logger.info("=" * 60)

    executed_trades = []

    if portfolio_output and portfolio_output.instructions:
        for instruction in portfolio_output.instructions:
            if not instruction.risk_approved:
                logger.warning(
                    f"Skipping trade for {instruction.trading212_ticker}: Not risk approved."
                )
                continue

            if instruction.action == "HOLD":
                logger.info(f"HOLD instruction for {instruction.trading212_ticker}.")
                continue

            quantity = instruction.quantity
            if instruction.action in ["SELL", "REDUCE"] and quantity > 0:
                quantity = -quantity
            elif instruction.action in ["BUY", "ADD"] and quantity < 0:
                quantity = -quantity

            quantity = round(quantity, 2)
            limit_price = (
                round(instruction.limit_price, 4)
                if instruction.limit_price
                else None
            )

            trade_record = {
                "ticker": instruction.trading212_ticker,
                "action": instruction.action,
                "quantity": quantity,
                "order_type": instruction.order_type,
                "limit_price": limit_price,
                "rationale": instruction.rationale,
            }

            logger.info(
                f"{'[DRY RUN] Would execute' if dry_run else 'Executing'} "
                f"{instruction.action} {abs(quantity)} x {instruction.trading212_ticker} via {instruction.order_type}..."
            )

            try:
                if instruction.order_type == "MARKET":
                    payload = MarketOrderPayload(
                        limitPrice=limit_price or 0.01,
                        quantity=quantity,
                        ticker=instruction.trading212_ticker,
                        timeValidity=instruction.time_validity,
                    )
                    res = t212_client.place_market_order(payload)
                elif instruction.order_type == "LIMIT":
                    payload = LimitOrderPayload(
                        limitPrice=limit_price,
                        quantity=quantity,
                        ticker=instruction.trading212_ticker,
                        timeValidity=instruction.time_validity,
                    )
                    res = t212_client.place_limit_order(payload)
                elif instruction.order_type == "STOP_LIMIT":
                    payload = StopLimitOrderPayload(
                        limitPrice=instruction.limit_price,
                        stopPrice=instruction.stop_price,
                        quantity=quantity,
                        ticker=instruction.trading212_ticker,
                        timeValidity=instruction.time_validity,
                    )
                    res = t212_client.place_stop_limit_order(payload)
                else:
                    logger.error(f"Unsupported order type: {instruction.order_type}")
                    continue

                trade_record["result"] = res
                executed_trades.append(trade_record)
                logger.info(f"Order result for {instruction.trading212_ticker}: {res}")
            except Exception as e:
                logger.error(f"Failed to place order for {instruction.trading212_ticker}: {e}")
                trade_record["error"] = str(e)
                executed_trades.append(trade_record)

            # Pace orders to respect Trading 212 order API rate limits (1 req/sec)
            time.sleep(2.0)

    else:
        logger.info("No trade instructions generated.")

    (runs_dir / "trades.json").write_text(json.dumps(executed_trades, indent=2))

    # 7. Generate Executive Summary
    total_elapsed = time.time() - start_time
    api_stats = {
        "call_count": pacer.call_count,
        "pacing_seconds": pacer.total_pacing_seconds,
        "duration": f"{total_elapsed:.1f}s",
    }
    summary_md = generate_executive_summary(
        run_timestamp=run_timestamp,
        environment=env_str,
        is_dry_run=dry_run,
        account_summary=account_summary,
        stocks=stocks,
        dossier=dossier,
        cio_output=cio_output,
        portfolio_output=portfolio_output,
        executed_trades=executed_trades,
        api_stats=api_stats,
    )
    (runs_dir / "executive_summary.md").write_text(summary_md)
    (Path("runs") / "latest_summary.md").write_text(summary_md)


    logger.info("=" * 60)
    logger.info(f"PIPELINE RUN COMPLETE — Report saved to {runs_dir / 'executive_summary.md'}")
    logger.info("=" * 60)
    print("\n" + summary_md)


def run_hedge_fund(
    dry_run: bool = True,
    max_candidates: int | None = None,
    environment: str | None = None,
):
    """Entrypoint with automatic Langfuse telemetry lifecycle flush."""
    try:
        _run_hedge_fund_internal(
            dry_run=dry_run,
            max_candidates=max_candidates,
            environment=environment,
        )
    finally:
        if langfuse_client:
            logger.info("Flushing Langfuse telemetry...")
            try:
                langfuse_client.flush()
                logger.info("Langfuse telemetry flushed successfully.")
            except Exception as e:
                logger.warning(f"Error flushing Langfuse telemetry: {e}")


def main():
    parser = argparse.ArgumentParser(description="AI Hedge Fund Production Runner")
    parser.add_argument(
        "--live",
        action="store_true",
        help="Execute live orders on Trading 212 (default is dry-run)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Simulate orders without placing live trades (default)",
    )
    parser.add_argument(
        "--max-candidates",
        type=int,
        default=None,
        help="Maximum candidates to evaluate (default from config)",
    )
    parser.add_argument(
        "--environment",
        type=str,
        choices=["demo", "live"],
        default=None,
        help="Trading 212 environment ('demo' or 'live')",
    )

    args = parser.parse_args()
    is_dry_run = not args.live

    run_hedge_fund(
        dry_run=is_dry_run,
        max_candidates=args.max_candidates,
        environment=args.environment,
    )


if __name__ == "__main__":
    main()
