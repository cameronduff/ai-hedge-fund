import pandas as pd
import numpy as np

from app.clients.trading212_client import Trading212Client
from app.clients.yfinance_client import YFinanceClient


class WatchlistService():
    def __init__(self):
        """
        Initializes the WatchlistService and loads the watchlist from a CSV file.
        """
        self.watchlist = pd.read_csv("app/tickers.csv")
        self.watchlist = self.watchlist.dropna()
    
    def get_existing_traded_instruments(self):
        """
        Fetches all currently traded instruments and pending orders from Trading212.

        Returns:
            set: A set of tickers for instruments that are either held or have pending orders.
        """
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
        Calculates the percentage deviation of the current price from its moving average.

        Target: >15% (TBC)

        Args:
            yfinance_ticker (str): The Yahoo Finance ticker symbol.
            period (str): The period for calculating the moving average (default "50d").

        Returns:
            float: The percentage deviation.
        """
        yfinance_client = YFinanceClient()
        historical_data = yfinance_client.get_historical_data(ticker=yfinance_ticker, period=period)
        ma = historical_data['Close'].mean()
        current_price = yfinance_client.get_current_price(ticker=yfinance_ticker)

        return round((current_price - ma) / ma * 100, 2)

    def get_rsi(self, yfinance_ticker: str, period: int = 14) -> float:
        """
        Calculates the Relative Strength Index (RSI) using Wilder's smoothed moving average.

        Overbought (>70) or oversold (<30).
        Target: RSI 30-70.

        Args:
            yfinance_ticker (str): The Yahoo Finance ticker symbol.
            period (int): The period for RSI calculation (default 14).

        Returns:
            float: The current RSI value.
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
        Fetches the trailing Price-to-Earnings (P/E) ratio for a ticker.

        Target: P/E < 35.

        Args:
            yfinance_ticker (str): The Yahoo Finance ticker symbol.

        Returns:
            float: The trailing P/E ratio.
        """
        yfinance_client = YFinanceClient()
        info = yfinance_client.get_info_by_ticker(ticker=yfinance_ticker)

        pe_ratio = round(info.get("trailingPE"), 2)
        return pe_ratio
    
    def get_debt_equity_ratio(self, yfinance_ticker: str):
        """
        Calculates the Debt-to-Equity (D/E) ratio for a ticker.

        - D/E < 1: Company is majority equity-financed, generally lower risk.
        - D/E 1–2: Common and acceptable in most sectors.
        - D/E > 2: Warrants scrutiny.
        Target: D/E < 2.

        Args:
            yfinance_ticker (str): The Yahoo Finance ticker symbol.

        Returns:
            float | None: The Debt-to-Equity ratio, or None if equity is zero.
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
        Calculates the percentage upside based on analyst price targets.

        Target: > 10%.

        Args:
            yfinance_ticker (str): The Yahoo Finance ticker symbol.

        Returns:
            float | None: The percentage upside, or None if targets or price are unavailable.
        """
        yfinance_client = YFinanceClient()

        targets = yfinance_client.get_analyst_price_targets(ticker=yfinance_ticker)
        mean_target = targets.get("mean")

        current_price = yfinance_client.get_current_price(ticker=yfinance_ticker)

        if not mean_target or not current_price:
            return None
        
        return round(((mean_target - current_price) / current_price) * 100, 2)
    
    def get_revenue_growth(self, yfinance_ticker: str):
        """
        Calculates the year-over-year quarterly revenue growth.

        Target: > 5%.

        Args:
            yfinance_ticker (str): The Yahoo Finance ticker symbol.

        Returns:
            float | None: The percentage revenue growth, or None if prior year data is unavailable.
        """
        yfinance_client = YFinanceClient()
        income_stmt = yfinance_client.get_quarterly_income_statement(ticker=yfinance_ticker)
        
        revenue = income_stmt.loc["Total Revenue"]
        
        current_quarter = revenue.iloc[0]       # most recent
        prior_year_quarter = revenue.iloc[4]    # same quarter last year
        
        if prior_year_quarter == 0:
            return None
            
        return round(((current_quarter - prior_year_quarter) / abs(prior_year_quarter)) * 100, 2)

    def get_earnings_date(self, yfinance_ticker: str):
        """
        Calculates the number of days until the next expected earnings date.

        Target: Earnings > 14 days away.

        Args:
            yfinance_ticker (str): The Yahoo Finance ticker symbol.

        Returns:
            int | None: Days until earnings, or None if no earnings date is found.
        """
        yfinance_client = YFinanceClient()
        calendar = yfinance_client.get_calendar(ticker=yfinance_ticker)
        earnings_dates = calendar.get("Earnings Date")

        if not earnings_dates:
            return None

        # Take the first date (start of the expected window)
        next_earnings = pd.Timestamp(earnings_dates[0])
        today = pd.Timestamp.now(tz=next_earnings.tz)
        days_until = (next_earnings - today).days

        return days_until

if __name__ == "__main__":
    yfinance_ticker = "AAPL"