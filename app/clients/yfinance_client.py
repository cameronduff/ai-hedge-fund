import yfinance as yf


class YFinanceClient:
    def __init__(self):
        # Add rate limiting logic
        pass

    def get_info_by_ticker(self, ticker: str):
        data = yf.Ticker(ticker)
        return data.info

    def get_balance_sheet_by_ticker(self, ticker: str):
        data = yf.Ticker(ticker)
        return data.balance_sheet

    def get_historical_data(self, ticker: str, period: str = "1mo"):
        data = yf.Ticker(ticker)
        return data.history(period=period)

    def get_options_chain(self, ticker: str):
        data = yf.Ticker(ticker)
        return data.option_chain(data.options[0]).calls

    def get_quarterly_income_statement(self, ticker: str):
        data = yf.Ticker(ticker)
        return data.quarterly_income_stmt

    def get_calendar(self, ticker: str):
        data = yf.Ticker(ticker)
        return data.calendar

    def get_analyst_price_targets(self, ticker: str):
        data = yf.Ticker(ticker)
        return data.analyst_price_targets


if __name__ == "__main__":
    tfinance_client = YFinanceClient()

    data = tfinance_client.get_options_chain("MSFT")

    print(data)
