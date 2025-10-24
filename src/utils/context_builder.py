# context_builder.py
import time
from typing import Any, Dict, List
from datetime import datetime, timezone


def _compact_portfolio(portfolio: List[dict], top_n: int = 40) -> List[dict]:
    items = []
    for p in portfolio:
        items.append(
            {
                "ticker": p.get("ticker"),
                "qty": p.get("quantity"),
                "avg_px": p.get("averagePrice"),
                "px": p.get("currentPrice"),
                "ppl": p.get("ppl"),
            }
        )
    items.sort(key=lambda r: abs((r["qty"] or 0) * (r["px"] or 0)), reverse=True)
    return items[:top_n]


def _compact_pie(pie: dict) -> dict:
    out = {
        "id": pie.get("id"),
        "name": pie.get("name"),
        "goal": pie.get("goal"),
        "settings": {
            "dividendCashAction": (pie.get("settings") or {}).get("dividendCashAction")
        },
        "instruments": [],
    }
    for i in pie.get("instruments", []):
        out["instruments"].append(
            {
                "ticker": i.get("ticker"),
                "ownedQty": i.get("ownedQuantity"),
                "expectedShare": i.get("expectedShare"),
            }
        )
    return out


def build_account_context(agent, *, top_n_positions: int = 40) -> Dict[str, Any]:
    cash = agent.get_cash()
    portfolio = agent.get_portfolio()
    return {
        "schema_version": "1.0",
        "asOf": datetime.now(timezone.utc).isoformat(),
        "cash": cash,
        "portfolio": _compact_portfolio(portfolio, top_n=top_n_positions),
    }


def build_pies_context(agent, include_plans=True):
    pies = agent.list_pies()
    pie_details, plans = [], {}
    for i, p in enumerate(pies):
        # Use data from list if sufficient
        d = _compact_pie(p if "instruments" in p else agent.get_pie(p["id"]))
        pie_details.append(d)

        if include_plans:
            try:
                plan = agent.plan_pie_rebalance(p["id"])
                if plan.get("status") == "ok":
                    orders = [
                        {
                            "ticker": o["ticker"],
                            "delta_qty": o["delta_qty"],
                            "price": o["price"],
                        }
                        for o in plan["orders"]
                    ]
                    plans[p["id"]] = {"orders": orders}
            except Exception as e:
                print(f"Plan for pie {p['id']} failed: {e}")

        # throttle to avoid 429s
        if i < len(pies) - 1:
            time.sleep(31)  # or dynamically based on x-ratelimit-reset
    return {"schema_version": "1.0", "pies": pie_details, "rebalance_plans": plans}
