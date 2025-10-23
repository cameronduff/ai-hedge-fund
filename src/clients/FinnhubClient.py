import datetime as dt
from typing import Any, Dict, List, Optional
from zoneinfo import ZoneInfo
import requests


# -----------------------------
# Exceptions
# -----------------------------
class MarketDataError(Exception): ...


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
