import pandas as pd

from app.clients.trading212_client import Trading212Client
from app.clients.yfinance_client import YFinanceClient


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
    
    def get_50_day_moving_average_devation_percentage(yfinance_ticker: str):
        yfinance_client = YFinanceClient()
        historical_data = yfinance_client.get_historical_data(ticker="AAPL", period="50d")
        ma50 = historical_data['Close'].mean()
        current_price = yfinance_client.get_current_price(ticker="AAPL")

        return round((current_price - ma50) / ma50 * 100, 2)


if __name__ == "__main__":
    yfinance_client = YFinanceClient()
    current_price = yfinance_client.get_current_price(ticker="AAPL")

    print(current_price)