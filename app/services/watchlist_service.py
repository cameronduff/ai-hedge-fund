import pandas as pd

from app.clients.trading212_client import Trading212Client


class WatchlistService():
    def __init__(self):
        self.watchlist = pd.read_csv("app/tickers.csv")
        self.watchlist = self.watchlist.dropna()
    
    def get_existing_traded_instruments(self):
        current_stock_interest = set()
    
        trading212_client = Trading212Client()
        instruments = trading212_client.fetch_all_open_positions()
        
        for stock in instruments:
            instrument = stock.get('instrument')
            ticker = instrument.get('ticker')
            if ticker:
                current_stock_interest.add(ticker)
        
        pending_orders = trading212_client.get_all_pending_orders()
        
        for order in pending_orders:
            ticker = order.get('ticker')
            if ticker:
                current_stock_interest.add(ticker)
        
        return current_stock_interest

if __name__ == "__main__":
    pass