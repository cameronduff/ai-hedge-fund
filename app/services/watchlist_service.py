import numpy as np
import pandas as pd
from loguru import logger

from app.clients.trading212_client import Trading212Client
from app.clients.yfinance_client import YFinanceClient
from app.models.quants_models import Ticker


class WatchlistService:
    def __init__(self, tickers_path: str = "app/tickers.csv"):
        """
        Initializes the WatchlistService and loads the watchlist from a CSV file.
        """
        self.tickers_path = tickers_path
        try:
            self.watchlist = pd.read_csv(tickers_path)
            self.watchlist = self.watchlist.dropna()
        except Exception as e:
            logger.error(f"Error loading watchlist from {tickers_path}: {e}")
            self.watchlist = pd.DataFrame(
                columns=["name", "trading212_ticker", "yfinance_ticker", "active"]
            )
        self.yfinance_client = YFinanceClient()
        self.trading212_client = Trading212Client()

    def get_existing_traded_instruments(self) -> set[str]:
        """
        Fetches all currently traded instruments and pending orders from Trading212.

        Returns:
            set: A set of tickers for instruments that are either held or have pending orders.
        """
        current_stock_interest = set()

        try:
            instruments = self.trading212_client.fetch_all_open_positions()
            if isinstance(instruments, list):
                for stock in instruments:
                    if isinstance(stock, dict):
                        instrument = stock.get("instrument")
                        ticker = (
                            instrument.get("ticker")
                            if isinstance(instrument, dict)
                            else stock.get("ticker")
                        )
                        if ticker:
                            current_stock_interest.add(ticker)
        except Exception as e:
            logger.error(f"Error fetching open positions from Trading212: {e}")

        try:
            pending_orders = self.trading212_client.get_all_pending_orders()
            if isinstance(pending_orders, list):
                for order in pending_orders:
                    if isinstance(order, dict):
                        ticker = order.get("ticker")
                        if ticker:
                            current_stock_interest.add(ticker)
        except Exception as e:
            logger.error(f"Error fetching pending orders from Trading212: {e}")

        return current_stock_interest

    def get_day_moving_average_devation_percentage(
        self, yfinance_ticker: str, period: str = "50d"
    ) -> float | None:
        """
        Calculates the percentage deviation of the current price from its moving average.

        Target: >15% (TBC)

        Args:
            yfinance_ticker (str): The Yahoo Finance ticker symbol.
            period (str): The period for calculating the moving average (default "50d").

        Returns:
            float | None: The percentage deviation, or None if calculation fails.
        """
        try:
            historical_data = self.yfinance_client.get_historical_data(
                ticker=yfinance_ticker, period=period
            )
            if (
                historical_data is None
                or historical_data.empty
                or "Close" not in historical_data
            ):
                return None

            ma = historical_data["Close"].mean()
            current_price = self.yfinance_client.get_current_price(
                ticker=yfinance_ticker
            )

            if current_price is None or pd.isna(ma) or ma == 0:
                return None

            return round((float(current_price) - float(ma)) / float(ma) * 100, 2)
        except Exception as e:
            logger.warning(
                f"Failed to calculate MA deviation for {yfinance_ticker}: {e}"
            )
            return None

    def get_rsi(self, yfinance_ticker: str, period: int = 14) -> float | None:
        """
        Calculates the Relative Strength Index (RSI) using Wilder's smoothed moving average.

        Overbought (>70) or oversold (<30).
        Target: RSI 30-70.

        Args:
            yfinance_ticker (str): The Yahoo Finance ticker symbol.
            period (int): The period for RSI calculation (default 14).

        Returns:
            float | None: The current RSI value, or None if calculation fails.
        """
        try:
            historical_data = self.yfinance_client.get_historical_data(
                ticker=yfinance_ticker, period="3mo"
            )
            if (
                historical_data is None
                or historical_data.empty
                or "Close" not in historical_data
            ):
                return None

            close = historical_data["Close"].dropna().values
            if len(close) <= period:
                return None

            delta = np.diff(close, prepend=np.nan)
            gain = np.where(delta > 0, delta, 0.0)
            loss = np.where(delta < 0, -delta, 0.0)

            avg_gain = np.full(len(close), np.nan)
            avg_loss = np.full(len(close), np.nan)

            # Seed at position period with simple mean of first 'period' deltas
            avg_gain[period] = gain[1 : period + 1].mean()
            avg_loss[period] = loss[1 : period + 1].mean()

            # Wilder smoothing from period+1 onwards
            for i in range(period + 1, len(close)):
                avg_gain[i] = (avg_gain[i - 1] * (period - 1) + gain[i]) / period
                avg_loss[i] = (avg_loss[i - 1] * (period - 1) + loss[i]) / period

            last_gain = avg_gain[-1]
            last_loss = avg_loss[-1]

            if pd.isna(last_gain) or pd.isna(last_loss):
                return None
            if last_loss == 0:
                return 100.0 if last_gain > 0 else 50.0

            rs = last_gain / last_loss
            rsi = 100.0 - (100.0 / (1.0 + rs))

            return round(float(rsi), 1)
        except Exception as e:
            logger.warning(f"Failed to calculate RSI for {yfinance_ticker}: {e}")
            return None

    def get_price_to_earnings_ratio(self, yfinance_ticker: str) -> float | None:
        """
        Fetches the trailing Price-to-Earnings (P/E) ratio for a ticker.

        Target: P/E < 35.

        Args:
            yfinance_ticker (str): The Yahoo Finance ticker symbol.

        Returns:
            float | None: The trailing P/E ratio, or None if unavailable.
        """
        try:
            info = self.yfinance_client.get_info_by_ticker(ticker=yfinance_ticker)
            if not isinstance(info, dict):
                return None
            pe_ratio = info.get("trailingPE")
            if pe_ratio is None or pd.isna(pe_ratio):
                return None
            return round(float(pe_ratio), 2)
        except Exception as e:
            logger.warning(f"Failed to fetch P/E for {yfinance_ticker}: {e}")
            return None

    def get_debt_equity_ratio(self, yfinance_ticker: str) -> float | None:
        """
        Calculates the Debt-to-Equity (D/E) ratio for a ticker.

        - D/E < 1: Company is majority equity-financed, generally lower risk.
        - D/E 1–2: Common and acceptable in most sectors.
        - D/E > 2: Warrants scrutiny.
        Target: D/E < 2.

        Args:
            yfinance_ticker (str): The Yahoo Finance ticker symbol.

        Returns:
            float | None: The Debt-to-Equity ratio, or None if unavailable or equity is zero.
        """
        try:
            balance_sheet = self.yfinance_client.get_balance_sheet_by_ticker(
                yfinance_ticker
            )
            if balance_sheet is None or balance_sheet.empty:
                return None
            if (
                "Total Debt" not in balance_sheet.index
                or "Stockholders Equity" not in balance_sheet.index
            ):
                return None

            total_debt = balance_sheet.loc["Total Debt"].iloc[0]
            equity = balance_sheet.loc["Stockholders Equity"].iloc[0]

            if pd.isna(total_debt) or pd.isna(equity) or equity == 0:
                return None

            return round(float(total_debt / equity), 2)
        except Exception as e:
            logger.warning(f"Failed to calculate D/E for {yfinance_ticker}: {e}")
            return None

    def get_analyst_upside(self, yfinance_ticker: str) -> float | None:
        """
        Calculates the percentage upside based on analyst price targets.

        Target: > 10%.

        Args:
            yfinance_ticker (str): The Yahoo Finance ticker symbol.

        Returns:
            float | None: The percentage upside, or None if targets or price are unavailable.
        """
        try:
            targets = self.yfinance_client.get_analyst_price_targets(
                ticker=yfinance_ticker
            )
            if not isinstance(targets, dict):
                return None
            mean_target = targets.get("mean")
            current_price = self.yfinance_client.get_current_price(
                ticker=yfinance_ticker
            )

            if (
                not mean_target
                or not current_price
                or pd.isna(mean_target)
                or pd.isna(current_price)
            ):
                return None

            return round(
                ((float(mean_target) - float(current_price)) / float(current_price))
                * 100,
                2,
            )
        except Exception as e:
            logger.warning(
                f"Failed to calculate analyst upside for {yfinance_ticker}: {e}"
            )
            return None

    def get_revenue_growth(self, yfinance_ticker: str) -> float | None:
        """
        Calculates the year-over-year quarterly revenue growth.

        Target: > 5%.

        Args:
            yfinance_ticker (str): The Yahoo Finance ticker symbol.

        Returns:
            float | None: The percentage revenue growth, or None if prior year data is unavailable.
        """
        try:
            income_stmt = self.yfinance_client.get_quarterly_income_statement(
                ticker=yfinance_ticker
            )
            if (
                income_stmt is None
                or income_stmt.empty
                or "Total Revenue" not in income_stmt.index
            ):
                return None

            revenue = income_stmt.loc["Total Revenue"]
            if len(revenue) < 5:
                return None

            current_quarter = revenue.iloc[0]
            prior_year_quarter = revenue.iloc[4]

            if (
                pd.isna(current_quarter)
                or pd.isna(prior_year_quarter)
                or prior_year_quarter == 0
            ):
                return None

            return round(
                (
                    (float(current_quarter) - float(prior_year_quarter))
                    / abs(float(prior_year_quarter))
                )
                * 100,
                2,
            )
        except Exception as e:
            logger.warning(
                f"Failed to calculate revenue growth for {yfinance_ticker}: {e}"
            )
            return None

    def get_earnings_date(self, yfinance_ticker: str) -> int | None:
        """
        Calculates the number of days until the next expected earnings date.

        Target: Earnings > 14 days away.

        Args:
            yfinance_ticker (str): The Yahoo Finance ticker symbol.

        Returns:
            int | None: Days until earnings, or None if no earnings date is found.
        """
        try:
            calendar = self.yfinance_client.get_calendar(ticker=yfinance_ticker)
            if calendar is None:
                return None

            earnings_dates = None
            if isinstance(calendar, dict):
                earnings_dates = calendar.get("Earnings Date")
            elif hasattr(calendar, "loc") and "Earnings Date" in calendar.index:
                earnings_dates = calendar.loc["Earnings Date"].tolist()

            if not earnings_dates or len(earnings_dates) == 0:
                return None

            next_earnings = pd.Timestamp(earnings_dates[0])
            if pd.isna(next_earnings):
                return None

            today = (
                pd.Timestamp.now(tz=next_earnings.tz)
                if next_earnings.tz is not None
                else pd.Timestamp.now()
            )
            return int((next_earnings - today).days)
        except Exception as e:
            logger.warning(
                f"Failed to calculate earnings date for {yfinance_ticker}: {e}"
            )
            return None

    def evaluate_ticker(
        self,
        yfinance_ticker: str,
        min_rsi: float = 30.0,
        max_rsi: float = 70.0,
        max_pe: float = 35.0,
        max_debt_equity: float = 2.0,
        min_analyst_upside: float = 10.0,
        min_revenue_growth: float = 5.0,
        min_earnings_days: int = 14,
        min_ma_deviation: float | None = None,
        strict: bool = False,
    ) -> dict:
        """
        Evaluates a ticker against quantitative and fundamental screening criteria.

        Args:
            yfinance_ticker (str): The Yahoo Finance ticker symbol.
            min_rsi (float): Minimum acceptable RSI (default 30.0).
            max_rsi (float): Maximum acceptable RSI (default 70.0).
            max_pe (float): Maximum trailing P/E ratio (default 35.0).
            max_debt_equity (float): Maximum Debt-to-Equity ratio (default 2.0).
            min_analyst_upside (float): Minimum analyst target upside percentage (default 10.0).
            min_revenue_growth (float): Minimum YoY quarterly revenue growth percentage (default 5.0).
            min_earnings_days (int): Minimum days until next earnings release (default 14).
            min_ma_deviation (float | None): Optional minimum MA deviation percentage.
            strict (bool): If True, requires all metrics to be present. If False, requires available metrics to pass.

        Returns:
            dict: Dictionary with keys 'passed', 'metrics', 'passed_checks', 'failed_checks'.
        """
        rsi = self.get_rsi(yfinance_ticker)
        pe_ratio = self.get_price_to_earnings_ratio(yfinance_ticker)
        debt_equity = self.get_debt_equity_ratio(yfinance_ticker)
        analyst_upside = self.get_analyst_upside(yfinance_ticker)
        revenue_growth = self.get_revenue_growth(yfinance_ticker)
        earnings_days = self.get_earnings_date(yfinance_ticker)
        ma_deviation = self.get_day_moving_average_devation_percentage(yfinance_ticker)

        metrics = {
            "rsi": rsi,
            "pe_ratio": pe_ratio,
            "debt_equity": debt_equity,
            "analyst_upside": analyst_upside,
            "revenue_growth": revenue_growth,
            "earnings_days": earnings_days,
            "ma_deviation": ma_deviation,
        }

        passed_checks = []
        failed_checks = []

        # 1. RSI (30 <= rsi <= 70)
        if rsi is not None:
            if min_rsi <= rsi <= max_rsi:
                passed_checks.append(f"RSI {rsi} in [{min_rsi}, {max_rsi}]")
            else:
                failed_checks.append(f"RSI {rsi} not in [{min_rsi}, {max_rsi}]")
        elif strict:
            failed_checks.append("RSI missing")

        # 2. P/E (0 < pe <= 35)
        if pe_ratio is not None:
            if 0 < pe_ratio <= max_pe:
                passed_checks.append(f"P/E {pe_ratio} <= {max_pe}")
            else:
                failed_checks.append(f"P/E {pe_ratio} > {max_pe} or <= 0")
        elif strict:
            failed_checks.append("P/E missing")

        # 3. Debt to Equity (d/e <= 2)
        if debt_equity is not None:
            if 0 <= debt_equity <= max_debt_equity:
                passed_checks.append(f"D/E {debt_equity} <= {max_debt_equity}")
            else:
                failed_checks.append(f"D/E {debt_equity} > {max_debt_equity}")
        elif strict:
            failed_checks.append("D/E missing")

        # 4. Analyst Upside (upside >= 10%)
        if analyst_upside is not None:
            if analyst_upside >= min_analyst_upside:
                passed_checks.append(
                    f"Analyst Upside {analyst_upside}% >= {min_analyst_upside}%"
                )
            else:
                failed_checks.append(
                    f"Analyst Upside {analyst_upside}% < {min_analyst_upside}%"
                )
        elif strict:
            failed_checks.append("Analyst Upside missing")

        # 5. Revenue Growth (growth >= 5%)
        if revenue_growth is not None:
            if revenue_growth >= min_revenue_growth:
                passed_checks.append(
                    f"Revenue Growth {revenue_growth}% >= {min_revenue_growth}%"
                )
            else:
                failed_checks.append(
                    f"Revenue Growth {revenue_growth}% < {min_revenue_growth}%"
                )
        elif strict:
            failed_checks.append("Revenue Growth missing")

        # 6. Earnings Date (> 14 days away)
        if earnings_days is not None:
            if earnings_days < 0 or earnings_days > min_earnings_days:
                passed_checks.append(
                    f"Earnings {earnings_days} days away (> {min_earnings_days}d)"
                )
            else:
                failed_checks.append(
                    f"Earnings in {earnings_days} days (<= {min_earnings_days}d)"
                )
        elif strict:
            failed_checks.append("Earnings Date missing")

        # 7. MA Deviation (optional)
        if min_ma_deviation is not None:
            if ma_deviation is not None:
                if ma_deviation >= min_ma_deviation:
                    passed_checks.append(
                        f"MA Deviation {ma_deviation}% >= {min_ma_deviation}%"
                    )
                else:
                    failed_checks.append(
                        f"MA Deviation {ma_deviation}% < {min_ma_deviation}%"
                    )
            elif strict:
                failed_checks.append("MA Deviation missing")

        passed = len(failed_checks) == 0 and len(passed_checks) > 0

        return {
            "ticker": yfinance_ticker,
            "passed": passed,
            "metrics": metrics,
            "passed_checks": passed_checks,
            "failed_checks": failed_checks,
        }

    def score_ticker(self, yfinance_ticker: str) -> tuple[float, dict]:
        """
        Calculates a multi-factor score (0-100) combining valuation, momentum,
        analyst consensus, and balance sheet safety.

        Returns:
            tuple[float, dict]: The composite score and the underlying metrics dictionary.
        """
        eval_result = self.evaluate_ticker(yfinance_ticker)
        metrics = eval_result["metrics"]
        score = 50.0  # neutral starting point

        rsi = metrics.get("rsi")
        if rsi is not None:
            if 40 <= rsi <= 60:
                score += 15
            elif 30 <= rsi <= 70:
                score += 5
            elif rsi > 75 or rsi < 25:
                score -= 15

        pe = metrics.get("pe_ratio")
        if pe is not None:
            if 0 < pe <= 20:
                score += 15
            elif 20 < pe <= 35:
                score += 5
            elif pe > 50 or pe <= 0:
                score -= 15

        de = metrics.get("debt_equity")
        if de is not None:
            if 0 <= de <= 1.0:
                score += 10
            elif de > 2.5:
                score -= 10

        upside = metrics.get("analyst_upside")
        if upside is not None:
            if upside >= 20.0:
                score += 15
            elif upside >= 10.0:
                score += 8
            elif upside < 0:
                score -= 10

        rev_growth = metrics.get("revenue_growth")
        if rev_growth is not None:
            if rev_growth >= 15.0:
                score += 10
            elif rev_growth >= 5.0:
                score += 5
            elif rev_growth < 0:
                score -= 5

        earnings_days = metrics.get("earnings_days")
        if earnings_days is not None and 0 <= earnings_days <= 14:
            score -= 10

        final_score = max(0.0, min(100.0, score))
        return final_score, metrics

    def filter_watchlist(
        self,
        candidates: list[Ticker] | None = None,
        max_tickers: int | None = None,
        include_traded_instruments: bool = True,
        min_score: float = 40.0,
        **filter_kwargs,
    ) -> list[Ticker]:
        """
        Filters and ranks candidate tickers down based on multi-factor quantitative
        and fundamental screening criteria before passing to quants.

        Guarantees that currently held or pending Trading 212 instruments are always included.

        Args:
            candidates (list[Ticker] | None): Optional list of candidate Tickers. Defaults to watchlist CSV.
            max_tickers (int | None): Maximum number of filtered tickers to return.
            include_traded_instruments (bool): Whether to include currently open positions / pending orders from Trading212.
            min_score (float): Minimum composite score required for non-held candidate stocks.
            **filter_kwargs: Threshold overrides for screening criteria.

        Returns:
            list[Ticker]: Filtered, ranked list of Ticker objects ready for quant analysis.
        """
        from app.core.config import settings

        if max_tickers is None:
            max_tickers = settings.MAX_CANDIDATES

        if candidates is None:
            from app.utils.ticker_utils import load_watchlist
            candidates = load_watchlist(self.tickers_path)

        traded_tickers: set[str] = set()
        if include_traded_instruments:
            traded_tickers = self.get_existing_traded_instruments()
            logger.info(
                f"Retrieved {len(traded_tickers)} currently traded/pending instruments from Trading212: {traded_tickers}"
            )

        # 1. First include any actively held or pending orders
        selected_stocks: list[Ticker] = []
        seen_t212: set[str] = set()

        for ticker in candidates:
            if ticker.trading212_ticker in traded_tickers:
                logger.info(f"Retaining existing traded instrument: {ticker.trading212_ticker} ({ticker.name})")
                selected_stocks.append(ticker)
                seen_t212.add(ticker.trading212_ticker)

        # Also add traded instruments that might not have been in candidates CSV
        if include_traded_instruments:
            from app.utils.ticker_utils import map_trading212_to_yfinance
            for t_sym in traded_tickers:
                if t_sym not in seen_t212:
                    yf_sym = map_trading212_to_yfinance(t_sym)
                    logger.info(f"Adding held instrument missing from candidates: {t_sym} -> {yf_sym}")
                    selected_stocks.append(Ticker(name=t_sym, trading212_ticker=t_sym, yfinance_ticker=yf_sym))
                    seen_t212.add(t_sym)

        # 2. Score remaining candidate stocks to fill remaining slots up to max_tickers
        remaining_slots = max(0, max_tickers - len(selected_stocks))
        if remaining_slots > 0:
            scored_candidates: list[tuple[float, Ticker]] = []
            for ticker in candidates:
                if ticker.trading212_ticker in seen_t212:
                    continue
                try:
                    score, metrics = self.score_ticker(ticker.yfinance_ticker)
                    logger.debug(f"Candidate {ticker.yfinance_ticker} score: {score:.1f}")
                    if score >= min_score:
                        scored_candidates.append((score, ticker))
                except Exception as e:
                    logger.warning(f"Error scoring {ticker.yfinance_ticker}: {e}")

            # Sort descending by composite score
            scored_candidates.sort(key=lambda x: x[0], reverse=True)

            for score, ticker in scored_candidates[:remaining_slots]:
                logger.info(f"Selected candidate by score {score:.1f}: {ticker.name} ({ticker.yfinance_ticker})")
                selected_stocks.append(ticker)
                seen_t212.add(ticker.trading212_ticker)

        logger.info(
            f"Screening complete: {len(selected_stocks)} tickers selected for Quants ({len(traded_tickers)} held/pending + {len(selected_stocks) - len(traded_tickers)} candidates)"
        )
        return selected_stocks

    def get_filtered_watchlist(self, **kwargs) -> list[Ticker]:
        """
        Convenience alias for filter_watchlist.
        """
        return self.filter_watchlist(**kwargs)


if __name__ == "__main__":
    service = WatchlistService()
    results = service.filter_watchlist(max_tickers=4)
    for stock in results:
        print(f"Selected: {stock.name} ({stock.yfinance_ticker})")