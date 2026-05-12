import pandas as pd
import numpy as np

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
    
    def get_day_moving_average_devation_percentage(self, yfinance_ticker: str, period: str = "50d") -> float:
        """
        Target >15% (TBC)
        """
        yfinance_client = YFinanceClient()
        historical_data = yfinance_client.get_historical_data(ticker=yfinance_ticker, period=period)
        ma = historical_data['Close'].mean()
        current_price = yfinance_client.get_current_price(ticker=yfinance_ticker)

        return round((current_price - ma) / ma * 100, 2)

    def get_rsi(self, yfinance_ticker: str, period: int = 14) -> float:
        """
        Wilder's smoothed moving average:
        Overbought (>70) or oversold (<30)
        Target RSI 30-70
        """
        yfinance_client = YFinanceClient()
        historical_data = yfinance_client.get_historical_data(ticker=yfinance_ticker, period="3mo")
        close = historical_data["Close"].values

        delta = np.diff(close, prepend=np.nan)
        gain = np.where(delta > 0, delta, 0.0)
        loss = np.where(delta < 0, -delta, 0.0)

        avg_gain = np.full(len(close), np.nan)
        avg_loss = np.full(len(close), np.nan)

        # Seed at position 14 with simple mean of first 14 periods
        avg_gain[period] = gain[1:period + 1].mean()
        avg_loss[period] = loss[1:period + 1].mean()

        # Wilder smoothing from period+1 onwards
        for i in range(period + 1, len(close)):
            avg_gain[i] = (avg_gain[i - 1] * (period - 1) + gain[i]) / period
            avg_loss[i] = (avg_loss[i - 1] * (period - 1) + loss[i]) / period

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return round(rsi[-1], 1)
    
    def get_price_to_earnings_ratio(self, yfinance_ticker: str):
        """
        Target P/E < 35
        """
        yfinance_client = YFinanceClient()
        info = yfinance_client.get_info_by_ticker(ticker=yfinance_ticker)

        pe_ratio = round(info.get("trailingPE"), 2)
        return pe_ratio
    
    def get_debt_equity_ratio(self, yfinance_ticker: str):
        """
        D/E < 1 means the company is majority equity-financed, generally lower risk
        D/E 1–2 is common and acceptable in most sectors
        D/E > 2 warrants scrutiny, though capital-intensive sectors like utilities or airlines routinely run higher

        Target D/E < 2
        """

        yfinance_client = YFinanceClient()
        balance_sheet = yfinance_client.get_balance_sheet_by_ticker(yfinance_ticker)

        total_debt = balance_sheet.loc["Total Debt"].iloc[0]
        equity = balance_sheet.loc["Stockholders Equity"].iloc[0]

        if equity == 0:
            return None

        return round(total_debt / equity, 2)
    
    def get_analyst_upside(self, yfinance_ticker: str) -> float | None:
        """
        Target > 10%
        """
        yfinance_client = YFinanceClient()

        targets = yfinance_client.get_analyst_price_targets(ticker=yfinance_ticker)
        mean_target = targets.get("mean")

        current_price = yfinance_client.get_current_price(ticker=yfinance_ticker)

        if not mean_target or not current_price:
            return None
        
        return round(((mean_target - current_price) / current_price) * 100, 2)
    
    def get_revenue_growth():
        """
        Target > 5%
        """
        pass

    def get_earnings_date():
        """
        Earnings > 14 days
        """
        pass

if __name__ == "__main__":
    yfinance_ticker = "AAPL"