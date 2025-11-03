import datetime as dt
import time
import random
from typing import Any, Dict
from zoneinfo import ZoneInfo
import requests


# -----------------------------
# Exceptions
# -----------------------------
class MarketDataError(Exception): ...


# -----------------------------
# Market Data Provider with Retry Logic
# -----------------------------
class FinnhubQuoteProvider:
    BASE = "https://finnhub.io/api/v1/quote"

    def __init__(self, api_key: str, timeout: float = 8.0, max_retries: int = 3):
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        params = {"symbol": symbol, "token": self.api_key}
        last_error = None

        for attempt in range(self.max_retries):
            try:
                r = requests.get(self.BASE, params=params, timeout=self.timeout)

                if r.status_code != 200:
                    # Retry on transient 5xx errors
                    if 500 <= r.status_code < 600:
                        raise MarketDataError(
                            f"Finnhub temporary HTTP {r.status_code}: {r.text[:200]}"
                        )
                    else:
                        raise MarketDataError(
                            f"Finnhub HTTP {r.status_code}: {r.text[:200]}"
                        )

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

            except (requests.exceptions.RequestException, MarketDataError) as e:
                last_error = e
                # Apply exponential backoff with jitter
                sleep_time = (2**attempt) + random.uniform(0.2, 0.8)
                print(
                    f"⚠️ Finnhub error ({e}), retrying in {sleep_time:.1f}s... ({attempt+1}/{self.max_retries})"
                )
                time.sleep(sleep_time)

        raise MarketDataError(
            f"Finnhub failed for {symbol} after {self.max_retries} retries: {last_error}"
        )
