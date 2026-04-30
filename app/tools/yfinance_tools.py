from datetime import date, datetime

from app.clients.yfinance_client import YFinanceClient

yfinance_client = YFinanceClient()

def _to_json_safe(value):
    """Recursively convert values to JSON-serializable primitives."""
    if isinstance(value, dict):
        return {str(k): _to_json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_to_json_safe(v) for v in value]
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if hasattr(value, "isoformat"):
        try:
            return value.isoformat()
        except (TypeError, ValueError):
            pass
    if hasattr(value, "item"):
        try:
            return _to_json_safe(value.item())
        except (ValueError, TypeError):
            pass
    return value


def get_info_by_ticker(ticker: str):
    """
    Fetches general information and summary metrics for a specific company.
    Use this to get an overview of the company's business, sector, industry, and key statistical ratios.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    return _to_json_safe(yfinance_client.get_info_by_ticker(ticker))


def get_balance_sheet_by_ticker(ticker: str):
    """
    Retrieves the company's most recent annual balance sheet.
    Use this to analyze the company's financial health, including total assets, liabilities, and shareholder equity.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    return yfinance_client.get_balance_sheet_by_ticker(ticker).to_json()


def get_historical_data(ticker: str, period: str = "1mo"):
    """
    Fetches historical price and volume data for a given ticker over a specified period.
    Use this for technical analysis, calculating moving averages, or analyzing price action.

    Args:
        ticker (str): The stock ticker symbol.
        period (str): The time period to fetch data for. Valid periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max. Defaults to "1mo".
    """
    return yfinance_client.get_historical_data(ticker, period).to_json()


def get_options_chain(ticker: str):
    """
    Retrieves the call options data for the nearest expiration date.
    Use this to gauge short-term market sentiment, speculative interest, and implied volatility.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    return yfinance_client.get_options_chain(ticker).to_json()


def get_quarterly_income_statement(ticker: str):
    """
    Retrieves the company's quarterly income statement.
    Use this to evaluate recent short-term trends in revenue, operating expenses, and net income.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    return yfinance_client.get_quarterly_income_statement(ticker).to_json()


def get_calendar(ticker: str):
    """
    Fetches the earnings calendar and upcoming corporate events for the specified ticker.
    Use this to check when the next earnings report is due, which could introduce high volatility.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    return _to_json_safe(yfinance_client.get_calendar(ticker))


def get_analyst_price_targets(ticker: str):
    """
    Retrieves current Wall Street analyst price targets, including the low, mean, median, and high estimates.
    Use this to gauge professional consensus and potential upside/downside expectations.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    return _to_json_safe(yfinance_client.get_analyst_price_targets(ticker))


if __name__ == "__main__":
    print(get_calendar("AAPL"))
    print(type(get_calendar("AAPL")))
    print(get_analyst_price_targets("AAPL"))
    print(type(get_analyst_price_targets("AAPL")))
    print(get_info_by_ticker("AAPL"))
    print(type(get_info_by_ticker("AAPL")))