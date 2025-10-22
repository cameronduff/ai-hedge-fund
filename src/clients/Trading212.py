"""
Trading 212 Agent-Ready Client — single-file Python module + CLI

What’s new vs previous version:
- **Agent-friendly facade** (`AgentAPI`) for easy buy/sell/hold + info.
- **Live/share price fetch** via a built-in Yahoo Finance quote provider (no extra deps).
- **Cleaner separation**: `T212Client` (broker ops) + `QuoteProvider` (market data) + `AgentAPI` (high-level tasks).
- **Extra CLI commands**: `quote`, `agent-*` helpers for simple automation/testing.

Features (broker):
- Read account info (cash, account details)
- View portfolio (all positions, per-ticker)
- List, fetch, create, update, delete Pies
- Inspect historical data (orders, dividends, transactions, CSV exports)
- Place/cancel orders (market for live; market/limit/stop in demo as per API)
- Instruments metadata lookup (exchanges, instruments)

Features (market data):
- Fetch current share price, currency, and latest trade time via Yahoo Finance HTTP endpoint.

Requirements:
- Python 3.9+
- `requests` (`pip install requests`)

Security:
- Uses HTTP Basic Auth header built from API Key + API Secret
- Optional IP allow-list can be configured in your Trading 212 account

IMPORTANT (from official docs):
- API environments: demo and live
- Only *Market Orders* supported in LIVE (real money) env
- To SELL, pass a NEGATIVE quantity
- Supported account types: Invest & Stocks ISA
- API is in beta and subject to change

See CLI examples at the bottom of this file.
"""

from __future__ import annotations

import base64
import datetime as dt
import json
import os
import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

import requests


# -----------------------------
# Exceptions
# -----------------------------
class T212Error(Exception):
    """Generic Trading212 API error."""


class T212RateLimitError(T212Error):
    """Raised when rate limits are exceeded."""


class T212AuthError(T212Error):
    """Raised for authentication problems."""


class MarketDataError(Exception):
    """Raised when market data (quotes) cannot be fetched."""


# -----------------------------
# Client (Trading 212)
# -----------------------------
@dataclass
class T212Client:
    api_key: str
    api_secret: str
    # env: "demo" or "live"
    env: str = "demo"
    # Optional: override base URL (mainly for testing/mocking)
    base_url: Optional[str] = None
    timeout: float = 20.0
    # When true, the client will automatically respect x-ratelimit headers
    respect_rate_limits: bool = True
    # Backoff parameters when 429 is encountered
    backoff_initial: float = 1.0
    backoff_max: float = 60.0

    def __post_init__(self) -> None:
        if self.env not in ("demo", "live"):
            raise ValueError("env must be 'demo' or 'live'")
        if not self.base_url:
            self.base_url = (
                "https://demo.trading212.com/api/v0"
                if self.env == "demo"
                else "https://live.trading212.com/api/v0"
            )
        # Build Basic auth header once
        creds = f"{self.api_key}:{self.api_secret}".encode("utf-8")
        token = base64.b64encode(creds).decode("utf-8")
        self._headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "t212-agent-client/1.1 (+https://github.com/you/t212-client)",
        }

    # -------------------------
    # HTTP helpers
    # -------------------------
    def _url(self, path: str) -> str:
        if path.startswith("http"):
            return path
        return f"{self.base_url}{path}"

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Dict[str, Any]] = None,
        expected_status: Iterable[int] = (200, 201, 202, 204),
        allow_429_backoff: bool = True,
    ) -> Tuple[requests.Response, Any]:
        url = self._url(path)
        backoff = self.backoff_initial
        while True:
            resp = requests.request(
                method=method.upper(),
                url=url,
                headers=self._headers,
                params=params,
                json=json_body,
                timeout=self.timeout,
            )

            # Basic error handling
            if resp.status_code == 401:
                raise T212AuthError("Unauthorized — check API key/secret and scopes")
            if resp.status_code == 403:
                raise T212AuthError(
                    "Forbidden — missing required scopes or IP not allowed"
                )
            if resp.status_code == 404:
                try:
                    data = resp.json()
                except Exception:
                    data = {"error": "Not found"}
                return resp, data

            if resp.status_code == 429:
                # Rate limited — try to respect reset header or exponential backoff
                if not allow_429_backoff:
                    raise T212RateLimitError("Rate limited (429)")
                reset_ts = resp.headers.get("x-ratelimit-reset")
                if self.respect_rate_limits and reset_ts:
                    now = int(time.time())
                    to_sleep = max(0, int(reset_ts) - now)
                    time.sleep(min(to_sleep, self.backoff_max))
                else:
                    time.sleep(backoff)
                    backoff = min(self.backoff_max, backoff * 2)
                continue

            if resp.status_code not in expected_status:
                try:
                    payload = resp.json()
                except Exception:
                    payload = {"body": resp.text}
                raise T212Error(f"HTTP {resp.status_code}: {json.dumps(payload)[:400]}")

            try:
                data = None if resp.status_code == 204 else resp.json()
            except ValueError:
                data = resp.text

            if self.respect_rate_limits:
                remaining = resp.headers.get("x-ratelimit-remaining")
                period = resp.headers.get("x-ratelimit-period")
                if remaining is not None and period is not None:
                    try:
                        remaining_i = max(1, int(remaining))
                        period_i = max(1, int(period))
                        time.sleep(min(0.15, period_i / remaining_i))
                    except Exception:
                        pass

            return resp, data

    # -------------------------
    # Account Data
    # -------------------------
    def get_cash(self) -> Dict[str, Any]:
        _, data = self._request("GET", "/equity/account/cash")
        return data

    def get_account_info(self) -> Dict[str, Any]:
        _, data = self._request("GET", "/equity/account/info")
        return data

    # -------------------------
    # Portfolio
    # -------------------------
    def get_portfolio(self) -> Dict[str, Any]:
        _, data = self._request("GET", "/equity/portfolio")
        return data

    def get_position_by_ticker(self, ticker: str) -> Dict[str, Any]:
        _, data = self._request("GET", f"/equity/portfolio/{ticker}")
        return data

    def refresh_portfolio_tickers(self, tickers: List[str]) -> Dict[str, Any]:
        payload = {"tickers": tickers}
        _, data = self._request("POST", "/equity/portfolio/ticker", json_body=payload)
        return data

    # -------------------------
    # Orders (LIVE: market only)
    # -------------------------
    def list_orders(
        self, status: Optional[str] = None, ticker: Optional[str] = None
    ) -> Dict[str, Any]:
        params = {}
        if status:
            params["status"] = status
        if ticker:
            params["ticker"] = ticker
        _, data = self._request("GET", "/equity/orders", params=params)
        return data

    def place_market_order(
        self, ticker: str, quantity: float, time_in_force: str = "DAY"
    ) -> Dict[str, Any]:
        payload = {
            "ticker": ticker,
            "quantity": quantity,  # NOTE: negative quantity means SELL
            "timeInForce": time_in_force,
        }
        _, data = self._request(
            "POST",
            "/equity/orders/market",
            json_body=payload,
            expected_status=(201, 202),
        )
        return data

    def place_limit_order(
        self,
        ticker: str,
        quantity: float,
        limit_price: float,
        time_in_force: str = "DAY",
    ) -> Dict[str, Any]:
        payload = {
            "ticker": ticker,
            "quantity": quantity,
            "limitPrice": limit_price,
            "timeInForce": time_in_force,
        }
        _, data = self._request(
            "POST",
            "/equity/orders/limit",
            json_body=payload,
            expected_status=(201, 202),
        )
        return data

    def place_stop_order(
        self,
        ticker: str,
        quantity: float,
        stop_price: float,
        time_in_force: str = "DAY",
    ) -> Dict[str, Any]:
        payload = {
            "ticker": ticker,
            "quantity": quantity,
            "stopPrice": stop_price,
            "timeInForce": time_in_force,
        }
        _, data = self._request(
            "POST", "/equity/orders/stop", json_body=payload, expected_status=(201, 202)
        )
        return data

    def place_stop_limit_order(
        self,
        ticker: str,
        quantity: float,
        stop_price: float,
        limit_price: float,
        time_in_force: str = "DAY",
    ) -> Dict[str, Any]:
        payload = {
            "ticker": ticker,
            "quantity": quantity,
            "stopPrice": stop_price,
            "limitPrice": limit_price,
            "timeInForce": time_in_force,
        }
        _, data = self._request(
            "POST",
            "/equity/orders/stop_limit",
            json_body=payload,
            expected_status=(201, 202),
        )
        return data

    def get_order(self, order_id: str) -> Dict[str, Any]:
        _, data = self._request("GET", f"/equity/orders/{order_id}")
        return data

    def cancel_order(self, order_id: str) -> None:
        self._request("DELETE", f"/equity/orders/{order_id}", expected_status=(204,))

    # -------------------------
    # Historical items
    # -------------------------
    def history_orders(
        self, cursor: Optional[str] = None, limit: int = 50
    ) -> Dict[str, Any]:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        _, data = self._request("GET", "/equity/history/orders", params=params)
        return data

    def history_dividends(
        self, cursor: Optional[str] = None, limit: int = 50
    ) -> Dict[str, Any]:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        _, data = self._request("GET", "/history/dividends", params=params)
        return data

    def history_transactions(
        self, cursor: Optional[str] = None, limit: int = 50
    ) -> Dict[str, Any]:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        _, data = self._request("GET", "/history/transactions", params=params)
        return data

    def history_exports_list(self) -> Dict[str, Any]:
        _, data = self._request("GET", "/history/exports")
        return data

    def history_exports_request(
        self, report_type: str, period_from: str, period_to: str
    ) -> Dict[str, Any]:
        payload = {
            "reportType": report_type,  # e.g. "DIVIDENDS" | "ORDERS" | "TRANSACTIONS"
            "periodFrom": period_from,  # YYYY-MM-DD
            "periodTo": period_to,  # YYYY-MM-DD
        }
        _, data = self._request(
            "POST", "/history/exports", json_body=payload, expected_status=(202,)
        )
        return data

    # -------------------------
    # Metadata
    # -------------------------
    def metadata_exchanges(self) -> Dict[str, Any]:
        _, data = self._request("GET", "/equity/metadata/exchanges")
        return data

    def metadata_instruments(
        self, cursor: Optional[str] = None, limit: int = 200
    ) -> Dict[str, Any]:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        _, data = self._request("GET", "/equity/metadata/instruments", params=params)
        return data

    # -------------------------
    # Pies (AutoInvest)
    # -------------------------
    def pies_list(
        self, cursor: Optional[str] = None, limit: int = 50
    ) -> Dict[str, Any]:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        _, data = self._request("GET", "/pies", params=params)
        return data

    def pies_get(self, pie_id: str) -> Dict[str, Any]:
        _, data = self._request("GET", f"/pies/{pie_id}")
        return data

    def pies_create(
        self,
        *,
        name: str,
        items: List[Dict[str, Any]],
        icon: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = {"name": name, "items": items}
        if icon:
            payload["icon"] = icon
        if description:
            payload["description"] = description
        _, data = self._request(
            "POST", "/pies", json_body=payload, expected_status=(201,)
        )
        return data

    def pies_update(self, pie_id: str, **fields: Any) -> Dict[str, Any]:
        # fields can include name, description, icon, items etc. per API model
        _, data = self._request("POST", f"/pies/{pie_id}", json_body=fields)
        return data

    def pies_delete(self, pie_id: str) -> None:
        self._request("DELETE", f"/pies/{pie_id}", expected_status=(204,))


# -----------------------------
# Market Data: Quote Providers
# -----------------------------
class QuoteProvider:
    def get_quote(self, symbol: str) -> Dict[str, Any]:  # pragma: no cover
        raise NotImplementedError


class YahooQuoteProvider(QuoteProvider):
    """Lightweight quote provider using Yahoo Finance's public quote endpoint.

    Notes:
    - No API key needed; subject to Yahoo's terms/rate limits.
    - Symbol mapping: use Yahoo symbols (e.g., "AAPL", "VUSA.L" for LSE-listed).
    - Returns last price, currency, and timestamp.
    """

    BASE = "https://query1.finance.yahoo.com/v7/finance/quote"

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        params = {"symbols": symbol}
        resp = requests.get(self.BASE, params=params, timeout=self.timeout)
        if resp.status_code != 200:
            raise MarketDataError(f"Quote HTTP {resp.status_code}: {resp.text[:200]}")
        data = resp.json()
        try:
            r = data["quoteResponse"]["result"][0]
        except Exception as e:
            raise MarketDataError(f"No quote for symbol {symbol}") from e
        price = r.get("regularMarketPrice")
        currency = r.get("currency")
        ts = r.get("regularMarketTime")  # epoch seconds
        return {
            "symbol": symbol,
            "price": float(price) if price is not None else None,
            "currency": currency,
            "asOf": dt.datetime.utcfromtimestamp(ts).isoformat() + "Z" if ts else None,
            "raw": r,
        }


# -----------------------------
# Agent-friendly Facade
# -----------------------------
@dataclass
class AgentAPI:
    broker: T212Client
    quotes: QuoteProvider

    # --- Info helpers ---
    def get_share_price(self, symbol: str) -> Dict[str, Any]:
        """Return current quote dict: {symbol, price, currency, asOf}.
        Use Yahoo symbols (e.g., AAPL, MSFT, NVDA, VUSA.L, TSLA, etc.).
        """
        return self.quotes.get_quote(symbol)

    def get_position(self, ticker: str) -> Dict[str, Any]:
        return self.broker.get_position_by_ticker(ticker)

    def get_portfolio(self) -> Dict[str, Any]:
        return self.broker.get_portfolio()

    def get_cash(self) -> Dict[str, Any]:
        return self.broker.get_cash()

    # --- Trading helpers ---
    def buy(self, ticker: str, quantity: float, tif: str = "DAY") -> Dict[str, Any]:
        return self.broker.place_market_order(ticker, abs(quantity), time_in_force=tif)

    def sell(self, ticker: str, quantity: float, tif: str = "DAY") -> Dict[str, Any]:
        # Trading 212 expects negative quantity to SELL
        return self.broker.place_market_order(ticker, -abs(quantity), time_in_force=tif)

    def hold(self, *_: Any, **__: Any) -> Dict[str, Any]:
        return {"status": "ok", "action": "HOLD", "reason": "No trade executed"}

    # --- Simple decision utility (optional) ---
    def decide_and_execute(
        self, *, ticker: str, symbol: str, threshold_pct: float = 1.0
    ) -> Dict[str, Any]:
        """Toy strategy: if current price is >= (1+threshold) vs avg price -> SELL 1; if <= (1-threshold) -> BUY 1; else HOLD.
        - ticker: Trading212 ticker used for orders/positions (e.g., VUSA for LSE ETF)
        - symbol: Quote symbol for market data (e.g., VUSA.L)
        - threshold_pct: band around average price
        """
        pos = self.get_position(ticker)
        quote = self.get_share_price(symbol)
        price = quote.get("price")
        if not pos or not price:
            return {
                "status": "error",
                "message": "Missing position or price",
                "position": pos,
                "quote": quote,
            }
        avg_price = (
            pos.get("averagePrice") or pos.get("avgPrice") or pos.get("average_price")
        )
        qty = pos.get("quantity") or pos.get("qty") or 0
        if not avg_price or qty == 0:
            # no holding — buy one share to open
            trade = self.buy(ticker, 1)
            return {
                "status": "ok",
                "action": "BUY",
                "reason": "No position",
                "trade": trade,
                "quote": quote,
            }
        up_band = avg_price * (1 + threshold_pct / 100.0)
        down_band = avg_price * (1 - threshold_pct / 100.0)
        if price >= up_band:
            trade = self.sell(ticker, 1)
            return {
                "status": "ok",
                "action": "SELL",
                "reason": f"price >= {up_band:.2f}",
                "trade": trade,
                "quote": quote,
            }
        if price <= down_band:
            trade = self.buy(ticker, 1)
            return {
                "status": "ok",
                "action": "BUY",
                "reason": f"price <= {down_band:.2f}",
                "trade": trade,
                "quote": quote,
            }
        return {
            "status": "ok",
            "action": "HOLD",
            "reason": "within band",
            "quote": quote,
        }


# -----------------------------
# Convenience: pretty print JSON
# -----------------------------
def _pp(obj: Any) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False)


# -----------------------------
# CLI
# -----------------------------
def _require_env(name: str) -> str:
    val = os.getenv(name)
    if not val:
        print(f"Environment variable {name} is required", file=sys.stderr)
        sys.exit(2)
    return val


def _build_client_from_env() -> T212Client:
    key = _require_env("T212_API_KEY")
    secret = _require_env("T212_API_SECRET")
    env = os.getenv("T212_ENV", "demo")  # demo | live
    base = os.getenv("T212_BASE_URL")  # optional override
    return T212Client(api_key=key, api_secret=secret, env=env, base_url=base)


def _build_agent_from_env() -> AgentAPI:
    broker = _build_client_from_env()
    quotes = YahooQuoteProvider()
    return AgentAPI(broker=broker, quotes=quotes)


def main(argv: Optional[List[str]] = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="Trading 212 Agent-Ready Client CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    # Account
    sub.add_parser("cash")
    sub.add_parser("account")

    # Portfolio
    sub.add_parser("portfolio")
    gpos = sub.add_parser("position")
    gpos.add_argument("ticker")

    # Orders
    lorders = sub.add_parser("orders")
    lorders.add_argument("--status")
    lorders.add_argument("--ticker")

    mkt = sub.add_parser("buy")
    mkt.add_argument("ticker")
    mkt.add_argument("quantity", type=float, help="Positive qty = BUY; negative = SELL")
    mkt.add_argument("--tif", default="DAY")

    canc = sub.add_parser("cancel")
    canc.add_argument("order_id")

    # History
    horders = sub.add_parser("history-orders")
    horders.add_argument("--cursor")
    horders.add_argument("--limit", type=int, default=50)

    hdiv = sub.add_parser("history-dividends")
    hdiv.add_argument("--cursor")
    hdiv.add_argument("--limit", type=int, default=50)

    htr = sub.add_parser("history-transactions")
    htr.add_argument("--cursor")
    htr.add_argument("--limit", type=int, default=50)

    hexp_list = sub.add_parser("exports")
    hexp_req = sub.add_parser("export-request")
    hexp_req.add_argument(
        "report_type", choices=["DIVIDENDS", "ORDERS", "TRANSACTIONS"]
    )  # adjust if API expands
    hexp_req.add_argument("period_from", help="YYYY-MM-DD")
    hexp_req.add_argument("period_to", help="YYYY-MM-DD")

    # Metadata
    sub.add_parser("exchanges")
    minst = sub.add_parser("instruments")
    minst.add_argument("--cursor")
    minst.add_argument("--limit", type=int, default=200)

    # Pies
    sub.add_parser("pies")

    gpie = sub.add_parser("pie")
    gpie.add_argument("pie_id")

    cp = sub.add_parser("pie-create")
    cp.add_argument("name")
    cp.add_argument(
        "items_json",
        help='JSON list of items, e.g. [{"ticker":"AAPL","targetPercentage":25}]',
    )
    cp.add_argument("--icon")
    cp.add_argument("--description")

    up = sub.add_parser("pie-update")
    up.add_argument("pie_id")
    up.add_argument("update_json", help="JSON of fields to update (per API model)")

    dp = sub.add_parser("pie-delete")
    dp.add_argument("pie_id")

    # Quotes
    q = sub.add_parser("quote")
    q.add_argument("symbol", help="Yahoo symbol, e.g. AAPL, VUSA.L")

    # Agent helpers
    ainfo = sub.add_parser("agent-info")
    ainfo.add_argument("ticker", help="Trading212 ticker, e.g. VUSA")
    ainfo.add_argument("symbol", help="Quote symbol, e.g. VUSA.L")

    abuy = sub.add_parser("agent-buy")
    abuy.add_argument("ticker")
    abuy.add_argument("quantity", type=float)

    asell = sub.add_parser("agent-sell")
    asell.add_argument("ticker")
    asell.add_argument("quantity", type=float)

    ahold = sub.add_parser("agent-hold")

    decide = sub.add_parser("agent-decide")
    decide.add_argument("ticker", help="Trading212 ticker (orders)")
    decide.add_argument("symbol", help="Quote symbol (pricing)")
    decide.add_argument(
        "--threshold", type=float, default=1.0, help="Percent band around avg price"
    )

    args = p.parse_args(argv)

    client = _build_client_from_env()
    agent = _build_agent_from_env()

    try:
        if args.cmd == "cash":
            print(_pp(client.get_cash()))
        elif args.cmd == "account":
            print(_pp(client.get_account_info()))
        elif args.cmd == "portfolio":
            print(_pp(client.get_portfolio()))
        elif args.cmd == "position":
            print(_pp(client.get_position_by_ticker(args.ticker)))
        elif args.cmd == "orders":
            print(_pp(client.list_orders(status=args.status, ticker=args.ticker)))
        elif args.cmd == "buy":
            # Use negative quantity for SELL
            print(
                _pp(
                    client.place_market_order(
                        args.ticker, args.quantity, time_in_force=args.tif
                    )
                )
            )
        elif args.cmd == "cancel":
            client.cancel_order(args.order_id)
            print("OK")
        elif args.cmd == "history-orders":
            print(_pp(client.history_orders(cursor=args.cursor, limit=args.limit)))
        elif args.cmd == "history-dividends":
            print(_pp(client.history_dividends(cursor=args.cursor, limit=args.limit)))
        elif args.cmd == "history-transactions":
            print(
                _pp(client.history_transactions(cursor=args.cursor, limit=args.limit))
            )
        elif args.cmd == "exports":
            print(_pp(client.history_exports_list()))
        elif args.cmd == "export-request":
            print(
                _pp(
                    client.history_exports_request(
                        args.report_type, args.period_from, args.period_to
                    )
                )
            )
        elif args.cmd == "exchanges":
            print(_pp(client.metadata_exchanges()))
        elif args.cmd == "instruments":
            print(
                _pp(client.metadata_instruments(cursor=args.cursor, limit=args.limit))
            )
        elif args.cmd == "pies":
            print(_pp(client.pies_list()))
        elif args.cmd == "pie":
            print(_pp(client.pies_get(args.pie_id)))
        elif args.cmd == "pie-create":
            items = json.loads(args.items_json)
            print(
                _pp(
                    client.pies_create(
                        name=args.name,
                        items=items,
                        icon=args.icon,
                        description=args.description,
                    )
                )
            )
        elif args.cmd == "pie-update":
            update = json.loads(args.update_json)
            print(_pp(client.pies_update(args.pie_id, **update)))
        elif args.cmd == "pie-delete":
            client.pies_delete(args.pie_id)
            print("OK")
        elif args.cmd == "quote":
            print(_pp(agent.get_share_price(args.symbol)))
        elif args.cmd == "agent-info":
            out = {
                "position": agent.get_position(args.ticker),
                "portfolio": agent.get_portfolio(),
                "cash": agent.get_cash(),
                "quote": agent.get_share_price(args.symbol),
            }
            print(_pp(out))
        elif args.cmd == "agent-buy":
            print(_pp(agent.buy(args.ticker, args.quantity)))
        elif args.cmd == "agent-sell":
            print(_pp(agent.sell(args.ticker, args.quantity)))
        elif args.cmd == "agent-hold":
            print(_pp(agent.hold()))
        elif args.cmd == "agent-decide":
            print(
                _pp(
                    agent.decide_and_execute(
                        ticker=args.ticker,
                        symbol=args.symbol,
                        threshold_pct=args.threshold,
                    )
                )
            )
        else:
            p.print_help()
            return 2
    except (T212Error, MarketDataError, requests.RequestException) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
    # Quote (Yahoo symbol)
    # python t212_client.py quote AAPL
    # python t212_client.py quote VUSA.L

    # # Agent info bundle (position, portfolio, cash, quote)
    # python t212_client.py agent-info VUSA VUSA.L

    # # Trading (Market Orders; SELL uses negative quantity under the hood)
    # python t212_client.py agent-buy VUSA 1
    # python t212_client.py agent-sell VUSA 1
    # python t212_client.py agent-hold

    # # Toy decision helper: buy/sell/hold around avg price band
    # python t212_client.py agent-decide VUSA VUSA.L --threshold 1.0
