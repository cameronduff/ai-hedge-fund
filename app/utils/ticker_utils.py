import csv
import json
import urllib.request
from pathlib import Path
from typing import Any

import pandas as pd
from loguru import logger

from app.clients.trading212_client import Trading212Client
from app.clients.yfinance_client import YFinanceClient
from app.models.quants_models import Ticker


def map_trading212_to_yfinance(
    t212_ticker: str,
    short_name: str = "",
    currency_code: str = "",
    isin: str = "",
) -> str:
    """
    Deterministically maps a Trading 212 ticker to its Yahoo Finance equivalent.
    Supports US, UK (LSE), German (XETRA), French (Euronext Paris), Dutch, Spanish, Italian, and Canadian stocks.
    """
    clean_ticker = t212_ticker.strip()
    s_name = (short_name or "").strip()

    # 1. US Equities (_US_EQ suffix)
    if clean_ticker.endswith("_US_EQ"):
        base = clean_ticker[:-6]
        # Berkshire and dual-class shares with slash, dot, or underscore
        return base.replace("/", "-").replace(".", "-").replace("_", "-")

    # 2. London Stock Exchange (l_EQ suffix or GBX / GBP with shortName)
    if clean_ticker.endswith("l_EQ") or clean_ticker.endswith("_UK_EQ"):
        base = s_name if s_name else clean_ticker.split("_")[0]
        if base.endswith("l"):
            base = base[:-1]
        return f"{base}.L"

    # 3. German XETRA (d_EQ or _DE_EQ)
    if clean_ticker.endswith("d_EQ") or clean_ticker.endswith("_DE_EQ"):
        base = s_name if s_name else clean_ticker.split("_")[0]
        if base.endswith("d"):
            base = base[:-1]
        return f"{base}.DE"

    # 4. Euronext Paris (p_EQ or _PA_EQ)
    if clean_ticker.endswith("p_EQ") or clean_ticker.endswith("_PA_EQ"):
        base = s_name if s_name else clean_ticker.split("_")[0]
        if base.endswith("p"):
            base = base[:-1]
        return f"{base}.PA"

    # 5. Euronext Amsterdam (a_EQ or _AS_EQ)
    if clean_ticker.endswith("a_EQ") or clean_ticker.endswith("_AS_EQ"):
        base = s_name if s_name else clean_ticker.split("_")[0]
        if base.endswith("a"):
            base = base[:-1]
        return f"{base}.AS"

    # 6. Bolsas y Mercados Españoles Madrid (m_EQ or _MC_EQ)
    if clean_ticker.endswith("m_EQ") or clean_ticker.endswith("_MC_EQ"):
        base = s_name if s_name else clean_ticker.split("_")[0]
        if base.endswith("m"):
            base = base[:-1]
        return f"{base}.MC"

    # 7. Borsa Italiana Milan (i_EQ or _MI_EQ)
    if clean_ticker.endswith("i_EQ") or clean_ticker.endswith("_MI_EQ"):
        base = s_name if s_name else clean_ticker.split("_")[0]
        if base.endswith("i"):
            base = base[:-1]
        return f"{base}.MI"

    # 8. Toronto Stock Exchange (_CA_EQ)
    if clean_ticker.endswith("_CA_EQ"):
        base = s_name if s_name else clean_ticker[:-6]
        return f"{base}.TO"

    # Default fallback: use short_name or split by underscore
    return s_name or clean_ticker.split("_")[0]


def query_yahoo_symbol_by_isin(isin: str) -> str | None:
    """
    Queries Yahoo Finance search API using the ISIN code to find the exact Yahoo symbol.
    """
    if not isin or len(isin.strip()) < 8:
        return None
    try:
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={isin.strip()}&quotesCount=1&newsCount=0"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            quotes = data.get("quotes", [])
            if quotes and "symbol" in quotes[0]:
                return quotes[0]["symbol"]
    except Exception as e:
        logger.debug(f"ISIN search failed for {isin}: {e}")
    return None


def load_watchlist(tickers_path: str = "app/tickers.csv") -> list[Ticker]:
    """
    Loads active tickers from CSV. If no tickers are marked active,
    defaults to a sensible core universe.
    """
    path = Path(tickers_path)
    if not path.exists():
        logger.warning(f"{tickers_path} does not exist, creating default watchlist.")
        create_default_universe(tickers_path)

    tickers = pd.read_csv(tickers_path)
    if "active" not in tickers.columns:
        tickers["active"] = False

    active_tickers = tickers.loc[tickers["active"] == True]
    if active_tickers.empty:
        logger.info("No active tickers found in CSV. Activating default liquid top 15 universe.")
        tickers.loc[tickers.index[:15], "active"] = True
        tickers.to_csv(tickers_path, index=False)
        active_tickers = tickers.loc[tickers["active"] == True]

    return [
        Ticker(
            name=str(row.name),
            trading212_ticker=str(row.trading212_ticker),
            yfinance_ticker=str(row.yfinance_ticker),
        )
        for row in active_tickers.itertuples()
    ]


def create_default_universe(filename: str = "app/tickers.csv"):
    """
    Generates a curated liquid default universe of major US, UK, and European equities.
    """
    core_stocks = [
        {"name": "Apple", "trading212_ticker": "AAPL_US_EQ", "yfinance_ticker": "AAPL", "active": True},
        {"name": "Microsoft", "trading212_ticker": "MSFT_US_EQ", "yfinance_ticker": "MSFT", "active": True},
        {"name": "Alphabet (Class A)", "trading212_ticker": "GOOGL_US_EQ", "yfinance_ticker": "GOOGL", "active": True},
        {"name": "Amazon", "trading212_ticker": "AMZN_US_EQ", "yfinance_ticker": "AMZN", "active": True},
        {"name": "NVIDIA", "trading212_ticker": "NVDA_US_EQ", "yfinance_ticker": "NVDA", "active": True},
        {"name": "Meta Platforms", "trading212_ticker": "META_US_EQ", "yfinance_ticker": "META", "active": True},
        {"name": "Bank of America", "trading212_ticker": "BAC_US_EQ", "yfinance_ticker": "BAC", "active": True},
        {"name": "JPMorgan Chase", "trading212_ticker": "JPM_US_EQ", "yfinance_ticker": "JPM", "active": True},
        {"name": "Berkshire Hathaway", "trading212_ticker": "BRK_B_US_EQ", "yfinance_ticker": "BRK-B", "active": True},
        {"name": "Tesla", "trading212_ticker": "TSLA_US_EQ", "yfinance_ticker": "TSLA", "active": True},
        {"name": "AstraZeneca", "trading212_ticker": "AZNl_EQ", "yfinance_ticker": "AZN.L", "active": True},
        {"name": "Shell", "trading212_ticker": "SHELl_EQ", "yfinance_ticker": "SHEL.L", "active": True},
        {"name": "ASML Holding", "trading212_ticker": "ASMLa_EQ", "yfinance_ticker": "ASML.AS", "active": True},
        {"name": "BMW", "trading212_ticker": "BMW_DE_EQ", "yfinance_ticker": "BMW.DE", "active": True},
        {"name": "Schneider Electric", "trading212_ticker": "SUp_EQ", "yfinance_ticker": "SU.PA", "active": True},
    ]
    df = pd.DataFrame(core_stocks)
    df.to_csv(filename, index=False)
    logger.info(f"Saved default universe of {len(core_stocks)} stocks to {filename}")


def sync_active_universe_from_trading212(
    target_csv: str = "app/tickers.csv",
    active_count: int = 25,
) -> pd.DataFrame:
    """
    Fetches all available instruments from Trading 212, maps them accurately to Yahoo Finance,
    and sets the top liquid instruments as active candidates.
    """
    t212_client = Trading212Client()
    instruments = t212_client.get_all_available_instruments()
    if not instruments:
        logger.warning("Could not fetch instruments from Trading 212, fallback to default universe.")
        create_default_universe(target_csv)
        return pd.read_csv(target_csv)

    rows = []
    seen = set()

    # Prioritize STOCKS (not CFDs / short ETFs)
    stocks_only = [i for i in instruments if i.get("type") == "STOCK"]

    for inst in stocks_only:
        t212_ticker = inst.get("ticker")
        if not t212_ticker or t212_ticker in seen:
            continue
        seen.add(t212_ticker)

        short_name = inst.get("shortName", "")
        currency = inst.get("currencyCode", "")
        isin = inst.get("isin", "")
        name = inst.get("name", short_name)

        yf_ticker = map_trading212_to_yfinance(
            t212_ticker=t212_ticker,
            short_name=short_name,
            currency_code=currency,
            isin=isin,
        )

        rows.append(
            {
                "name": name,
                "trading212_ticker": t212_ticker,
                "yfinance_ticker": yf_ticker,
                "isin": isin,
                "currency": currency,
                "active": False,
            }
        )

    df = pd.DataFrame(rows)

    # Activate top liquid / popular US, UK, and European stocks
    core_popular = {
        "AAPL_US_EQ", "MSFT_US_EQ", "GOOGL_US_EQ", "AMZN_US_EQ", "NVDA_US_EQ",
        "META_US_EQ", "BAC_US_EQ", "JPM_US_EQ", "TSLA_US_EQ", "VODl_EQ",
        "AZNl_EQ", "SHELl_EQ", "BMW_DE_EQ", "ASMLa_EQ", "SUp_EQ"
    }

    df.loc[df["trading212_ticker"].isin(core_popular), "active"] = True

    # If fewer than active_count active, activate additional US stocks
    current_active = df["active"].sum()
    if current_active < active_count:
        needed = active_count - current_active
        candidates = df[~df["active"] & df["trading212_ticker"].str.endswith("_US_EQ")].index[:needed]
        df.loc[candidates, "active"] = True

    df.to_csv(target_csv, index=False)
    logger.info(f"Saved {len(df)} mapped instruments ({df['active'].sum()} active) to {target_csv}")
    return df


if __name__ == "__main__":
    df = sync_active_universe_from_trading212()
    print("Active universe:")
    print(df[df["active"]][["name", "trading212_ticker", "yfinance_ticker"]])