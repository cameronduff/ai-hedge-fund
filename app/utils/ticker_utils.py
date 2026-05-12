import csv

import pandas as pd
from loguru import logger

from app.clients.trading212_client import Trading212Client
from app.clients.yfinance_client import YFinanceClient
from app.models.quants_models import Ticker


def load_watchlist():
    tickers = pd.read_csv("app/tickers.csv")
    active_tickers = tickers.loc[tickers['active']]

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
    
    if instruments is not None:
        return [
            {
                "name": instrument.get('name'),
                "trading212_ticker": instrument.get('ticker')
            } for instrument in instruments
        ]
    else:
        raise ValueError("Instruments cannot be empty")

def find_yfinance_ticker_from_trading212_ticker(trading212_stocks):
    yfinance_client = YFinanceClient()
    
    valid_matches = [] 
    
    for index, stock in enumerate(trading212_stocks):
        logger.info(f"Processing stock {index+1}/{len(trading212_stocks)}")
        try:
            t212_ticker = stock.get('trading212_ticker')
            yfinance_ticker = t212_ticker.split("_")[0]
            info = yfinance_client.get_info_by_ticker(yfinance_ticker)
            
            if(len(info) > 2):
                stock.update({'yfinance_ticker':yfinance_ticker})
                valid_matches.append(stock)
        except Exception as e:
            logger.error(str(e))
        
    return valid_matches

def save_tickers_to_csv(stocks):
    filename = "app/tickers.csv"
    
    # Clear file
    f = open(filename, "w")
    f.truncate()
    f.close()
    
    # Make all stocks not active
    for stock in stocks:
        stock.update({"active": False})
    
    # Save CSV
    df = pd.DataFrame(stocks)
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    trading212_stocks = get_all_trading212_instrument_ids()
    stocks = find_yfinance_ticker_from_trading212_ticker(trading212_stocks)
    save_tickers_to_csv(stocks)