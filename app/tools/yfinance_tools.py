from app.clients.yfinance_client import YFinanceClient

yfinance_client = YFinanceClient()


def get_info_by_ticker(ticker: str):
    """
    Fetches general information and summary metrics for a specific company.
    Use this to get an overview of the company's business, sector, industry, and key statistical ratios.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    return yfinance_client.get_info_by_ticker(ticker)


def get_balance_sheet_by_ticket(ticker: str):
    """
    Retrieves the company's most recent annual balance sheet.
    Use this to analyze the company's financial health, including total assets, liabilities, and shareholder equity.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    return yfinance_client.get_balance_sheet_by_ticket(ticker)


def get_historical_data(ticker: str, period: str = "1mo"):
    """
    Fetches historical price and volume data for a given ticker over a specified period.
    Use this for technical analysis, calculating moving averages, or analyzing price action.

    Args:
        ticker (str): The stock ticker symbol.
        period (str): The time period to fetch data for. Valid periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max. Defaults to "1mo".
    """
    return yfinance_client.get_historical_data(ticker, period)


def get_options_chain(ticker: str):
    """
    Retrieves the call options data for the nearest expiration date.
    Use this to gauge short-term market sentiment, speculative interest, and implied volatility.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    return yfinance_client.get_options_chain(ticker)


def get_quarterly_income_statement(ticker: str):
    """
    Retrieves the company's quarterly income statement.
    Use this to evaluate recent short-term trends in revenue, operating expenses, and net income.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    return yfinance_client.get_quarterly_income_statement(ticker)


def get_calendar(ticker: str):
    """
    Fetches the earnings calendar and upcoming corporate events for the specified ticker.
    Use this to check when the next earnings report is due, which could introduce high volatility.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    return yfinance_client.get_calendar(ticker)


def get_analyst_price_targets(ticker: str):
    """
    Retrieves current Wall Street analyst price targets, including the low, mean, median, and high estimates.
    Use this to gauge professional consensus and potential upside/downside expectations.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    return yfinance_client.get_analyst_price_targets(ticker)
