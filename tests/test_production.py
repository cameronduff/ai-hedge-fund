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
