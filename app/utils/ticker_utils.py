import pandas as pd
from app.models.quants_models import Ticker

def load_watchlist():
    tickers = pd.read_csv("app/tickers.csv")
    active_tickers = tickers.loc[tickers['active'] == True]

    return [
        Ticker(
            name = row.name,
            trading212_ticker=row.trading212_ticker,
            yfinance_ticker=row.yfinance_ticker
        ) for row in active_tickers.itertuples()
    ]


if __name__ == "__main__":
    print(load_watchlist())