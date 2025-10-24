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
import time
import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
from src.clients.FinnhubClient import FinnhubQuoteProvider
from loguru import logger
import requests
import base64


# -----------------------------
# Exceptions
# -----------------------------
class T212Error(Exception): ...


class T212RateLimitError(T212Error): ...


class T212AuthError(T212Error): ...


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
            "User-Agent": "t212-agent-client/2.1",
        }

    # -------------------------
    # Request Helper
    # -------------------------
    def _req(self, method: str, path: str, **kwargs):
        url = path if path.startswith("http") else f"{self.base_url}{path}"

        for attempt in range(8):
            resp = requests.request(
                method, url, headers=self._headers, timeout=self.timeout, **kwargs
            )

            # Log key rate-limit headers
            remaining = resp.headers.get("x-ratelimit-remaining")
            reset = resp.headers.get("x-ratelimit-reset")
            used = resp.headers.get("x-ratelimit-used")
            logger.info(
                f"[{resp.status_code}] {path} | Remaining={remaining} "
                f"Reset={reset} Used={used}"
            )

            # Handle common error codes
            if resp.status_code == 401:
                raise T212AuthError("Unauthorized — check API credentials")
            if resp.status_code == 403:
                raise T212AuthError("Forbidden — missing scopes or IP not allowed")

            # Handle rate limiting with precise sleep
            if resp.status_code == 429:
                now = int(time.time())
                wait = None
                if reset and reset.isdigit():
                    reset_ts = int(reset)
                    wait = max(0, reset_ts - now) + random.uniform(0.2, 0.6)
                    logger.warning(
                        f"⚠️ 429 Rate-limited; sleeping until reset ({wait:.1f}s)..."
                    )
                    time.sleep(wait)
                    continue
                # fallback exponential back-off if no reset header
                wait = min(60, 2**attempt) + random.random()
                logger.warning(
                    f"⚠️ 429 Rate-limited (no reset header); retrying in {wait:.1f}s..."
                )
                time.sleep(wait)
                continue

            if not resp.ok:
                raise T212Error(f"HTTP {resp.status_code}: {resp.text[:200]}")

            # Success
            try:
                return resp.json()
            except Exception:
                return resp.text

        raise T212RateLimitError(
            "Repeated 429s from Trading 212 after multiple retries"
        )

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

    # --- Pies (AutoInvest) ---
    def pies_list(self) -> list:
        return self._req("GET", "/equity/pies")  # scope pies:read

    def pie_get(self, pie_id: int) -> dict:
        return self._req("GET", f"/equity/pies/{pie_id}")  # scope pies:read

    def pie_create(
        self,
        *,
        name: str,
        instrument_shares: Dict[str, float],
        goal: float,
        dividend_cash_action: str = "REINVEST",
        end_date: Optional[str] = None,
        icon: Optional[str] = None,
    ) -> dict:
        payload = {
            "name": name,
            "instrumentShares": instrument_shares,
            "goal": goal,
            "dividendCashAction": dividend_cash_action,
        }
        if end_date:
            payload["endDate"] = end_date
        if icon:
            payload["icon"] = icon
        return self._req("POST", "/equity/pies", json=payload)  # scope pies:write

    def pie_update(self, pie_id: int, **fields) -> dict:
        return self._req("POST", f"/equity/pies/{pie_id}", json=fields)

    def pie_duplicate(
        self, pie_id: int, *, name: str, icon: Optional[str] = None
    ) -> dict:
        payload = {"name": name}
        if icon:
            payload["icon"] = icon
        return self._req("POST", f"/equity/pies/{pie_id}/duplicate", json=payload)

    def pie_delete(self, pie_id: int) -> dict:
        return self._req("DELETE", f"/equity/pies/{pie_id}")

    # --- Instruments metadata ---
    def instruments(self, cursor: Optional[str] = None, limit: int = 200) -> dict:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        return self._req("GET", "/equity/metadata/instruments", params=params)

    def exchanges(self) -> dict:
        return self._req("GET", "/equity/metadata/exchanges")


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

    # --- Pies ---
    def list_pies(self) -> list:
        return self.broker.pies_list()

    def get_pie(self, pie_id: int) -> dict:
        return self.broker.pie_get(pie_id)

    def update_pie_weights(
        self, pie_id: int, weights: Dict[str, float], **kwargs
    ) -> dict:
        total = sum(weights.values()) or 1.0
        instrument_shares = {t: w / total for t, w in weights.items()}
        fields = {"instrumentShares": instrument_shares}
        fields.update(kwargs)
        return self.broker.pie_update(pie_id, **fields)

    # --- Research helpers ---
    def search_instruments(
        self, query: str, max_pages: int = 3, page_size: int = 200
    ) -> List[dict]:
        out, cursor = [], None
        for _ in range(max_pages):
            page = self.broker.instruments(cursor=cursor, limit=page_size)
            items = page.get("items") or page.get("instruments") or page
            for it in items:
                text = f"{it.get('ticker','')} {it.get('name','')} {it.get('isin','')}".lower()
                if query.lower() in text:
                    out.append(it)
            cursor = page.get("next") or page.get("cursor")
            if not cursor:
                break
        return out

    # --- Rebalancing ---
    def _to_simple_symbol(self, t212_ticker: str) -> Optional[str]:
        parts = t212_ticker.split("_")
        return parts[0] if len(parts) >= 3 and parts[1] == "US" else None

    def plan_pie_rebalance(self, pie_id: int) -> Dict[str, Any]:
        pie = self.get_pie(pie_id)
        instruments = pie.get("instruments", [])
        target_map = {
            i["ticker"]: i.get("expectedShare") for i in instruments if "ticker" in i
        }
        if not target_map or any(v is None for v in target_map.values()):
            settings = pie.get("settings", {})
            target_map = settings.get("instrumentShares", target_map)

        rows, total_value = [], 0.0
        for i in instruments:
            t = i["ticker"]
            owned_qty = float(i.get("ownedQuantity", 0) or 0)
            sym = self._to_simple_symbol(t)
            if not sym:
                continue
            q = self.quotes.get_quote(sym)
            px = float(q["price"])
            cur_val = owned_qty * px
            rows.append(
                {
                    "ticker": t,
                    "sym": sym,
                    "price": px,
                    "owned_qty": owned_qty,
                    "cur_val": cur_val,
                }
            )
            total_value += cur_val

        if total_value <= 0:
            return {"status": "error", "reason": "pie has zero value"}

        plan = []
        for r in rows:
            w_target = float(target_map.get(r["ticker"], 0.0))
            tgt_val = w_target * total_value
            tgt_qty = tgt_val / r["price"]
            delta_qty = tgt_qty - r["owned_qty"]
            if abs(delta_qty) >= 0.001:
                plan.append(
                    {
                        "ticker": r["ticker"],
                        "sym": r["sym"],
                        "price": r["price"],
                        "delta_qty": delta_qty,
                    }
                )

        return {"status": "ok", "pie_id": pie_id, "orders": plan}

    def execute_rebalance_plan(
        self, plan: Dict[str, Any], tif: str = "DAY"
    ) -> List[dict]:
        if plan.get("status") != "ok":
            return []
        results = []
        for o in plan["orders"]:
            qty = o["delta_qty"]
            res = self.broker.place_market_order(o["ticker"], qty, tif=tif)
            results.append({"ticker": o["ticker"], "placed": qty, "result": res})
        return results


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
    agent = get_agent()
    pies = agent.list_pies()
    print("== Pies ==")
    print(json.dumps(pies, indent=2))

    if pies:
        pie_id = pies[0]["id"]
        pie = agent.get_pie(pie_id)
        print(f"\n== Pie {pie_id} ==")
        print(json.dumps(pie, indent=2))
