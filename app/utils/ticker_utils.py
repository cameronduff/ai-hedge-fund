import pandas as pd
from app.models.quants_models import Ticker
from app.clients.trading212_client import Trading212Client

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

def get_all_trading212_instrument_ids():
    t212_client = Trading212Client()

    instruments = t212_client.get_all_available_instruments()

    return [
        {
            "name": instrument.get('name'),
            "trading212_ticker": instrument.get('ticker')
        } for instrument in instruments
    ]

if __name__ == "__main__":
    print(get_all_trading212_instrument_ids())