"""
Trading 212 Agent-Ready Client (Library Version)

Usage:
    - Imports `.env` for API credentials.
    - Exposes T212Client / AgentAPI for use in other scripts.
    - Includes a __main__ demo block showing common operations.

Environment (.env):
    T212_API_KEY=your_key_here
    T212_API_SECRET=your_secret_here
    T212_ENV=demo   # or live
"""

import os
import json
import random
import datetime as dt
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import requests
import base64
import time


# -----------------------------
# Exceptions
# -----------------------------
class T212Error(Exception): ...


class T212RateLimitError(T212Error): ...


class T212AuthError(T212Error): ...


class MarketDataError(Exception): ...


# -----------------------------
# Trading 212 Client
# -----------------------------
@dataclass
class T212Client:
    api_key: str
    api_secret: str
    env: str = "demo"
    base_url: Optional[str] = None
    timeout: float = 20.0
    respect_rate_limits: bool = True

    def __post_init__(self) -> None:
        if self.env not in ("demo", "live"):
            raise ValueError("env must be 'demo' or 'live'")
        if not self.base_url:
            self.base_url = (
                "https://demo.trading212.com/api/v0"
                if self.env == "demo"
                else "https://live.trading212.com/api/v0"
            )

        creds = f"{self.api_key}:{self.api_secret}".encode("utf-8")
        token = base64.b64encode(creds).decode("utf-8")
        self._headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "t212-agent-client/2.0",
        }

    # -------------------------
    # Request Helper
    # -------------------------
    def _req(self, method: str, path: str, **kwargs) -> Any:
        url = path if path.startswith("http") else f"{self.base_url}{path}"
        resp = requests.request(
            method, url, headers=self._headers, timeout=self.timeout, **kwargs
        )

        if resp.status_code == 401:
            raise T212AuthError("Unauthorized — check API credentials")
        if resp.status_code == 403:
            raise T212AuthError("Forbidden — missing scopes or IP not allowed")
        if resp.status_code == 429:
            raise T212RateLimitError("Rate limited (429)")
        if not resp.ok:
            raise T212Error(f"HTTP {resp.status_code}: {resp.text[:200]}")

        try:
            return resp.json()
        except Exception:
            return resp.text

    # -------------------------
    # Basic endpoints
    # -------------------------
    def get_cash(self):
        return self._req("GET", "/equity/account/cash")

    def get_account_info(self):
        return self._req("GET", "/equity/account/info")

    def get_portfolio(self):
        return self._req("GET", "/equity/portfolio")

    def get_position_by_ticker(self, ticker: str):
        return self._req("GET", f"/equity/portfolio/{ticker}")

    def place_market_order(self, ticker: str, quantity: float, tif="DAY"):
        payload = {"ticker": ticker, "quantity": quantity, "timeInForce": tif}
        return self._req("POST", "/equity/orders/market", json=payload)


# -----------------------------
# Market Data Provider
# -----------------------------
class FinnhubQuoteProvider:
    BASE = "https://finnhub.io/api/v1/quote"

    def __init__(self, api_key: str, timeout: float = 8.0):
        self.api_key = api_key
        self.timeout = timeout

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        params = {"symbol": symbol, "token": self.api_key}
        r = requests.get(self.BASE, params=params, timeout=self.timeout)
        if r.status_code != 200:
            raise MarketDataError(f"Finnhub HTTP {r.status_code}: {r.text[:200]}")
        data = r.json()
        if "c" not in data:
            raise MarketDataError(f"Unexpected response: {data}")
        return {
            "symbol": symbol,
            "price": data["c"],
            "currency": "USD",
            "asOf": dt.datetime.now(ZoneInfo("Europe/London")).strftime(
                "%Y-%m-%dT%H:%M:%S%z"
            ),
            "high": data.get("h"),
            "low": data.get("l"),
            "open": data.get("o"),
            "prev_close": data.get("pc"),
            "source": "finnhub",
        }


# -----------------------------
# Agent API
# -----------------------------
@dataclass
class AgentAPI:
    broker: T212Client
    quotes: FinnhubQuoteProvider

    def get_share_price(self, symbol: str):
        return self.quotes.get_quote(symbol)

    def get_position(self, ticker: str):
        return self.broker.get_position_by_ticker(ticker)

    def get_portfolio(self):
        return self.broker.get_portfolio()

    def get_cash(self):
        return self.broker.get_cash()

    def buy(self, ticker: str, qty: float):
        return self.broker.place_market_order(ticker, abs(qty))

    def sell(self, ticker: str, qty: float):
        return self.broker.place_market_order(ticker, -abs(qty))

    def hold(self):
        return {"status": "ok", "action": "HOLD"}

    def decide_and_execute(
        self, *, ticker: str, symbol: str, threshold_pct: float = 1.0
    ):
        pos = self.get_position(ticker)
        quote = self.get_share_price(symbol)
        price = quote.get("price")
        avg = pos.get("averagePrice", 0) if pos else 0
        qty = pos.get("quantity", 0) if pos else 0

        if not qty:
            trade = self.buy(ticker, 1)
            return {
                "action": "BUY",
                "reason": "no position",
                "trade": trade,
                "quote": quote,
            }

        up = avg * (1 + threshold_pct / 100)
        down = avg * (1 - threshold_pct / 100)
        if price >= up:
            trade = self.sell(ticker, 1)
            return {"action": "SELL", "reason": f"price >= {up}", "trade": trade}
        if price <= down:
            trade = self.buy(ticker, 1)
            return {"action": "BUY", "reason": f"price <= {down}", "trade": trade}
        return {"action": "HOLD", "reason": "within band"}


# -----------------------------
# Factory from .env
# -----------------------------
def get_t212_client() -> T212Client:
    load_dotenv()
    key = os.getenv("T212_API_KEY")
    secret = os.getenv("T212_API_SECRET")
    env = os.getenv("T212_ENV", "demo")
    if not key or not secret:
        raise RuntimeError("Missing T212_API_KEY or T212_API_SECRET in .env")
    return T212Client(api_key=key, api_secret=secret, env=env)


def get_agent() -> AgentAPI:
    load_dotenv()
    broker = get_t212_client()
    finnhub_key = os.getenv("FINNHUB_API_KEY")
    if not finnhub_key:
        raise RuntimeError("Missing FINNHUB_API_KEY in .env")
    quotes = FinnhubQuoteProvider(finnhub_key)
    return AgentAPI(broker=broker, quotes=quotes)


# -----------------------------
# Demo (__main__)
# -----------------------------
if __name__ == "__main__":
    load_dotenv()

    agent = get_agent()

    print("== Account info ==")
    print(json.dumps(agent.get_cash(), indent=2))

    print("\n== Portfolio ==")
    print(json.dumps(agent.get_portfolio(), indent=2))

    print("\n== Quote example (AAPL) ==")
    print(json.dumps(agent.get_share_price("AAPL"), indent=2))

    # Demo decision helper (no trade if no holdings)
    # print("\n== Demo decide_and_execute ==")
    # result = agent.decide_and_execute(ticker="VUSA", symbol="VUSA.L", threshold_pct=1.0)
    # print(json.dumps(result, indent=2))
