import pytest
import time
from app.utils.ticker_utils import map_trading212_to_yfinance
from app.services.watchlist_service import WatchlistService
from app.clients.trading212_client import Trading212Client
from app.models.trading212_models import MarketOrderPayload
from app.models.quants_models import Ticker


def test_ticker_mapping():
    assert map_trading212_to_yfinance("AAPL_US_EQ") == "AAPL"
    assert map_trading212_to_yfinance("BRK_B_US_EQ") == "BRK-B"
    assert map_trading212_to_yfinance("VODl_EQ", short_name="VOD") == "VOD.L"
    assert map_trading212_to_yfinance("AZNl_EQ") == "AZN.L"
    assert map_trading212_to_yfinance("BMW_DE_EQ") == "BMW.DE"
    assert map_trading212_to_yfinance("SUp_EQ", short_name="SU") == "SU.PA"
    assert map_trading212_to_yfinance("ASMLa_EQ", short_name="ASML") == "ASML.AS"
    assert map_trading212_to_yfinance("FSZ_CA_EQ") == "FSZ.TO"


def test_watchlist_scoring():
    ws = WatchlistService()
    score, metrics = ws.score_ticker("AAPL")
    assert isinstance(score, float)
    assert 0.0 <= score <= 100.0
    assert "rsi" in metrics


def test_watchlist_filter_caps():
    ws = WatchlistService()
    candidates = [
        Ticker(name="Apple", trading212_ticker="AAPL_US_EQ", yfinance_ticker="AAPL"),
        Ticker(name="Microsoft", trading212_ticker="MSFT_US_EQ", yfinance_ticker="MSFT"),
        Ticker(name="Alphabet", trading212_ticker="GOOGL_US_EQ", yfinance_ticker="GOOGL"),
        Ticker(name="Amazon", trading212_ticker="AMZN_US_EQ", yfinance_ticker="AMZN"),
    ]
    # Filter with cap of 2
    filtered = ws.filter_watchlist(candidates=candidates, max_tickers=2, include_traded_instruments=False)
    assert len(filtered) <= 2


def test_trading212_dry_run_safety():
    client = Trading212Client(dry_run=True)
    payload = MarketOrderPayload(
        limitPrice=100.0,
        quantity=1.0,
        ticker="AAPL_US_EQ",
        timeValidity="DAY",
    )
    res = client.place_market_order(payload)
    assert res.get("status") == "DRY_RUN"
    assert res.get("simulated") is True


def test_single_step_agents_and_hybrid_models():
    from google.adk.agents import LlmAgent
    from app.core.config import settings
    from app.agents.quants.fundamentals_agent.agent import build_fundamentals_agent
    from app.agents.quants.technicals_agent.agent import build_technicals_agent
    from app.agents.quants.growth_agent.agent import build_growth_agent
    from app.agents.quants.valuations_agent.agent import build_valuations_agent
    from app.agents.investors.chief_investment_officer.agent import chief_investment_officer_agent
    from app.agents.management.portfolio_manager_agent.agent import portfolio_manager_agent
    from app.models.quants_models import FundamentalsAgentOutput, TechnicalAgentOutput, GrowthAgentOutput, ValuationAgentOutput
    from app.models.investors_models import CIOOutput
    from app.models.management_models import PortfolioManagerOutput

    # 1. Quants are single-step LlmAgents with output_schema
    fa = build_fundamentals_agent("AAPL")
    assert isinstance(fa, LlmAgent)
    assert fa.output_schema == FundamentalsAgentOutput
    assert fa.model == settings.QUANTS_MODEL

    ta = build_technicals_agent("AAPL")
    assert isinstance(ta, LlmAgent)
    assert ta.output_schema == TechnicalAgentOutput
    assert ta.model == settings.QUANTS_MODEL

    ga = build_growth_agent("AAPL")
    assert isinstance(ga, LlmAgent)
    assert ga.output_schema == GrowthAgentOutput
    assert ga.model == settings.QUANTS_MODEL

    va = build_valuations_agent("AAPL")
    assert isinstance(va, LlmAgent)
    assert va.output_schema == ValuationAgentOutput
    assert va.model == settings.QUANTS_MODEL

    # 2. CIO and PM are single-step LlmAgents with output_schema and DECISION_MODEL
    assert isinstance(chief_investment_officer_agent, LlmAgent)
    assert chief_investment_officer_agent.output_schema == CIOOutput
    assert chief_investment_officer_agent.model == settings.DECISION_MODEL

    assert isinstance(portfolio_manager_agent, LlmAgent)
    assert portfolio_manager_agent.output_schema == PortfolioManagerOutput
    assert portfolio_manager_agent.model == settings.DECISION_MODEL

