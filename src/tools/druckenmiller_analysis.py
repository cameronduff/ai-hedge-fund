import json
import math
import statistics
from typing import Dict, Any, List, Optional, Tuple


def analyze_growth_momentum(financial_data: str) -> str:
    """
    Analyze growth and momentum using Stanley Druckenmiller's approach:
    - Revenue acceleration and CAGR
    - EPS growth and margin expansion
    - Price momentum confirmation

    Args:
        financial_data: JSON string containing financial metrics and price data

    Returns:
        JSON string with growth and momentum analysis
    """
    try:
        data = json.loads(financial_data)
        financial_metrics = data.get("financial_metrics", [])
        prices = data.get("prices", [])

        if not financial_metrics or len(financial_metrics) < 2:
            return json.dumps(
                {
                    "score": 0,
                    "revenue_growth": None,
                    "eps_growth": None,
                    "price_momentum": None,
                    "details": "Insufficient financial data for growth analysis",
                }
            )

        details = []
        raw_score = 0  # Max 9 points (3 each for revenue, EPS, momentum)

        # 1. Revenue Growth (CAGR)
        revenues = [
            fm.get("revenue")
            for fm in financial_metrics
            if fm.get("revenue") is not None
        ]
        revenue_growth = None
        if len(revenues) >= 2:
            latest_rev = revenues[0]
            older_rev = revenues[-1]
            num_years = len(revenues) - 1
            if older_rev > 0 and latest_rev > 0:
                revenue_growth = (latest_rev / older_rev) ** (1 / num_years) - 1
                if revenue_growth > 0.08:  # 8% CAGR
                    raw_score += 3
                    details.append(f"Strong revenue growth: {revenue_growth:.1%} CAGR")
                elif revenue_growth > 0.04:  # 4% CAGR
                    raw_score += 2
                    details.append(
                        f"Moderate revenue growth: {revenue_growth:.1%} CAGR"
                    )
                elif revenue_growth > 0.01:  # 1% CAGR
                    raw_score += 1
                    details.append(f"Slight revenue growth: {revenue_growth:.1%} CAGR")
                else:
                    details.append(f"Declining revenue: {revenue_growth:.1%} CAGR")
            else:
                details.append("Invalid revenue data for growth calculation")
        else:
            details.append("Insufficient revenue data points")

        # 2. EPS Growth (CAGR)
        eps_values = [
            fm.get("earnings_per_share")
            for fm in financial_metrics
            if fm.get("earnings_per_share") is not None
        ]
        eps_growth = None
        if len(eps_values) >= 2:
            latest_eps = eps_values[0]
            older_eps = eps_values[-1]
            num_years = len(eps_values) - 1
            if older_eps > 0 and latest_eps > 0:
                eps_growth = (latest_eps / older_eps) ** (1 / num_years) - 1
                if eps_growth > 0.08:  # 8% CAGR
                    raw_score += 3
                    details.append(f"Strong EPS growth: {eps_growth:.1%} CAGR")
                elif eps_growth > 0.04:  # 4% CAGR
                    raw_score += 2
                    details.append(f"Moderate EPS growth: {eps_growth:.1%} CAGR")
                elif eps_growth > 0.01:  # 1% CAGR
                    raw_score += 1
                    details.append(f"Slight EPS growth: {eps_growth:.1%} CAGR")
                else:
                    details.append(f"Declining EPS: {eps_growth:.1%} CAGR")
            else:
                details.append("EPS data not suitable for growth calculation")
        else:
            details.append("Insufficient EPS data points")

        # 3. Price Momentum
        price_momentum = None
        if prices and len(prices) > 30:
            sorted_prices = sorted(prices, key=lambda p: p.get("time", ""))
            close_prices = [
                p.get("close") for p in sorted_prices if p.get("close") is not None
            ]
            if len(close_prices) >= 2:
                start_price = close_prices[0]
                end_price = close_prices[-1]
                if start_price > 0:
                    price_momentum = (end_price - start_price) / start_price
                    if price_momentum > 0.50:  # 50%+ momentum
                        raw_score += 3
                        details.append(f"Very strong momentum: {price_momentum:.1%}")
                    elif price_momentum > 0.20:  # 20%+ momentum
                        raw_score += 2
                        details.append(f"Moderate momentum: {price_momentum:.1%}")
                    elif price_momentum > 0:
                        raw_score += 1
                        details.append(f"Positive momentum: {price_momentum:.1%}")
                    else:
                        details.append(f"Negative momentum: {price_momentum:.1%}")
                else:
                    details.append("Invalid starting price for momentum calculation")
            else:
                details.append("Insufficient price data for momentum")
        else:
            details.append("Not enough price data for momentum analysis")

        # Scale to 0-10
        final_score = min(10, (raw_score / 9) * 10)

        return json.dumps(
            {
                "score": round(final_score, 2),
                "revenue_growth": revenue_growth,
                "eps_growth": eps_growth,
                "price_momentum": price_momentum,
                "details": "; ".join(details),
            }
        )

    except Exception as e:
        return json.dumps(
            {
                "score": 0,
                "revenue_growth": None,
                "eps_growth": None,
                "price_momentum": None,
                "details": f"Error in growth analysis: {str(e)}",
            }
        )


def assess_risk_reward(financial_data: str) -> str:
    """
    Assess risk-reward profile focusing on capital preservation:
    - Debt-to-equity analysis
    - Price volatility assessment
    - Upside/downside scenario mapping

    Args:
        financial_data: JSON string containing financial and price data

    Returns:
        JSON string with risk-reward analysis
    """
    try:
        data = json.loads(financial_data)
        financial_metrics = data.get("financial_metrics", [])
        prices = data.get("prices", [])

        if not financial_metrics or not prices:
            return json.dumps(
                {
                    "score": 0,
                    "debt_to_equity": None,
                    "volatility": None,
                    "upside_potential": None,
                    "downside_risk": None,
                    "details": "Insufficient data for risk-reward analysis",
                }
            )

        details = []
        raw_score = 0  # Max 6 points (3 for debt, 3 for volatility)

        # 1. Debt-to-Equity Analysis
        debt_to_equity = None
        recent_debt = (
            financial_metrics[0].get("total_debt", 0) if financial_metrics else 0
        )
        recent_equity = (
            financial_metrics[0].get("shareholders_equity", 1)
            if financial_metrics
            else 1
        )

        if recent_equity and recent_equity > 0:
            debt_to_equity = recent_debt / recent_equity
            if debt_to_equity < 0.3:  # Low debt
                raw_score += 3
                details.append(f"Low debt-to-equity: {debt_to_equity:.2f}")
            elif debt_to_equity < 0.7:  # Moderate debt
                raw_score += 2
                details.append(f"Moderate debt-to-equity: {debt_to_equity:.2f}")
            elif debt_to_equity < 1.5:  # High debt
                raw_score += 1
                details.append(f"High debt-to-equity: {debt_to_equity:.2f}")
            else:
                details.append(f"Very high debt-to-equity: {debt_to_equity:.2f}")
        else:
            details.append("No equity data for debt analysis")

        # 2. Volatility Analysis
        volatility = None
        if len(prices) > 10:
            close_prices = [
                p.get("close") for p in prices if p.get("close") is not None
            ]
            if len(close_prices) > 10:
                daily_returns = []
                for i in range(1, len(close_prices)):
                    prev_close = close_prices[i - 1]
                    if prev_close > 0:
                        daily_returns.append(
                            (close_prices[i] - prev_close) / prev_close
                        )

                if daily_returns:
                    volatility = statistics.pstdev(daily_returns)
                    if volatility < 0.01:  # Low vol <1%
                        raw_score += 3
                        details.append(f"Low volatility: {volatility:.2%} daily")
                    elif volatility < 0.02:  # Moderate vol <2%
                        raw_score += 2
                        details.append(f"Moderate volatility: {volatility:.2%} daily")
                    elif volatility < 0.04:  # High vol <4%
                        raw_score += 1
                        details.append(f"High volatility: {volatility:.2%} daily")
                    else:
                        details.append(f"Very high volatility: {volatility:.2%} daily")
                else:
                    details.append("Unable to calculate daily returns")
            else:
                details.append("Insufficient close price data")
        else:
            details.append("Not enough price data for volatility")

        # Estimate upside/downside based on fundamentals
        upside_potential = None
        downside_risk = None

        # Simple heuristic based on growth and debt levels
        if debt_to_equity is not None and volatility is not None:
            # Lower debt + lower vol = better risk/reward
            if debt_to_equity < 0.5 and volatility < 0.02:
                upside_potential = 0.5  # 50% upside
                downside_risk = 0.15  # 15% downside
            elif debt_to_equity < 1.0 and volatility < 0.03:
                upside_potential = 0.3  # 30% upside
                downside_risk = 0.25  # 25% downside
            else:
                upside_potential = 0.2  # 20% upside
                downside_risk = 0.4  # 40% downside

        # Scale to 0-10
        final_score = min(10, (raw_score / 6) * 10)

        return json.dumps(
            {
                "score": round(final_score, 2),
                "debt_to_equity": debt_to_equity,
                "volatility": volatility,
                "upside_potential": upside_potential,
                "downside_risk": downside_risk,
                "details": "; ".join(details),
            }
        )

    except Exception as e:
        return json.dumps(
            {
                "score": 0,
                "debt_to_equity": None,
                "volatility": None,
                "upside_potential": None,
                "downside_risk": None,
                "details": f"Error in risk-reward analysis: {str(e)}",
            }
        )


def analyze_druckenmiller_valuation(financial_data: str) -> str:
    """
    Analyze valuation with growth context:
    - P/E, P/FCF, EV/EBIT, EV/EBITDA
    - Growth-adjusted metrics
    - Multiple expansion potential

    Args:
        financial_data: JSON string containing financial metrics and market cap

    Returns:
        JSON string with valuation analysis
    """
    try:
        data = json.loads(financial_data)
        financial_metrics = data.get("financial_metrics", [])
        market_cap = data.get("market_cap")

        if not financial_metrics or market_cap is None:
            return json.dumps(
                {
                    "score": 0,
                    "pe_ratio": None,
                    "pfcf_ratio": None,
                    "ev_ebit": None,
                    "ev_ebitda": None,
                    "details": "Insufficient data for valuation analysis",
                }
            )

        details = []
        raw_score = 0  # Max 8 points (2 each for 4 metrics)

        recent_metrics = financial_metrics[0]

        # Calculate enterprise value
        recent_debt = recent_metrics.get("total_debt", 0) or 0
        recent_cash = recent_metrics.get("cash_and_equivalents", 0) or 0
        enterprise_value = market_cap + recent_debt - recent_cash

        # 1. P/E Ratio
        pe_ratio = None
        net_income = recent_metrics.get("net_income")
        if net_income and net_income > 0:
            pe_ratio = market_cap / net_income
            if pe_ratio < 15:
                raw_score += 2
                details.append(f"Attractive P/E: {pe_ratio:.1f}")
            elif pe_ratio < 25:
                raw_score += 1
                details.append(f"Fair P/E: {pe_ratio:.1f}")
            else:
                details.append(f"High P/E: {pe_ratio:.1f}")
        else:
            details.append("No positive net income for P/E")

        # 2. P/FCF Ratio
        pfcf_ratio = None
        fcf = recent_metrics.get("free_cash_flow")
        if fcf and fcf > 0:
            pfcf_ratio = market_cap / fcf
            if pfcf_ratio < 15:
                raw_score += 2
                details.append(f"Attractive P/FCF: {pfcf_ratio:.1f}")
            elif pfcf_ratio < 25:
                raw_score += 1
                details.append(f"Fair P/FCF: {pfcf_ratio:.1f}")
            else:
                details.append(f"High P/FCF: {pfcf_ratio:.1f}")
        else:
            details.append("No positive FCF for P/FCF")

        # 3. EV/EBIT
        ev_ebit = None
        ebit = recent_metrics.get("ebit")
        if enterprise_value > 0 and ebit and ebit > 0:
            ev_ebit = enterprise_value / ebit
            if ev_ebit < 15:
                raw_score += 2
                details.append(f"Attractive EV/EBIT: {ev_ebit:.1f}")
            elif ev_ebit < 25:
                raw_score += 1
                details.append(f"Fair EV/EBIT: {ev_ebit:.1f}")
            else:
                details.append(f"High EV/EBIT: {ev_ebit:.1f}")
        else:
            details.append("Invalid EV/EBIT calculation")

        # 4. EV/EBITDA
        ev_ebitda = None
        ebitda = recent_metrics.get("ebitda")
        if enterprise_value > 0 and ebitda and ebitda > 0:
            ev_ebitda = enterprise_value / ebitda
            if ev_ebitda < 10:
                raw_score += 2
                details.append(f"Attractive EV/EBITDA: {ev_ebitda:.1f}")
            elif ev_ebitda < 18:
                raw_score += 1
                details.append(f"Fair EV/EBITDA: {ev_ebitda:.1f}")
            else:
                details.append(f"High EV/EBITDA: {ev_ebitda:.1f}")
        else:
            details.append("Invalid EV/EBITDA calculation")

        # Scale to 0-10
        final_score = min(10, (raw_score / 8) * 10)

        return json.dumps(
            {
                "score": round(final_score, 2),
                "pe_ratio": pe_ratio,
                "pfcf_ratio": pfcf_ratio,
                "ev_ebit": ev_ebit,
                "ev_ebitda": ev_ebitda,
                "details": "; ".join(details),
            }
        )

    except Exception as e:
        return json.dumps(
            {
                "score": 0,
                "pe_ratio": None,
                "pfcf_ratio": None,
                "ev_ebit": None,
                "ev_ebitda": None,
                "details": f"Error in valuation analysis: {str(e)}",
            }
        )


def evaluate_sentiment_catalysts(news_data: str) -> str:
    """
    Evaluate market sentiment and potential catalysts:
    - News sentiment analysis
    - Catalyst identification
    - Market positioning insights

    Args:
        news_data: JSON string containing company news

    Returns:
        JSON string with sentiment and catalyst analysis
    """
    try:
        data = json.loads(news_data)
        news_items = data.get("news", [])

        if not news_items:
            return json.dumps(
                {
                    "score": 5,  # Neutral
                    "positive_signals": 0,
                    "negative_signals": 0,
                    "overall_sentiment": "neutral",
                    "details": "No news data available for sentiment analysis",
                }
            )

        # Keyword analysis
        positive_keywords = [
            "growth",
            "expansion",
            "beat",
            "exceed",
            "strong",
            "positive",
            "partnership",
            "innovation",
            "acquisition",
            "breakthrough",
            "record",
        ]
        negative_keywords = [
            "lawsuit",
            "fraud",
            "decline",
            "miss",
            "weak",
            "negative",
            "investigation",
            "recall",
            "downgrade",
            "loss",
            "bankruptcy",
        ]

        positive_count = 0
        negative_count = 0

        for news in news_items:
            title = (news.get("title", "") or "").lower()
            if any(word in title for word in positive_keywords):
                positive_count += 1
            if any(word in title for word in negative_keywords):
                negative_count += 1

        total_news = len(news_items)
        positive_ratio = positive_count / total_news if total_news > 0 else 0
        negative_ratio = negative_count / total_news if total_news > 0 else 0

        # Determine sentiment score
        if positive_ratio > 0.4:
            score = 8  # Positive sentiment
            overall_sentiment = "positive"
        elif negative_ratio > 0.3:
            score = 3  # Negative sentiment
            overall_sentiment = "negative"
        else:
            score = 6  # Neutral sentiment
            overall_sentiment = "neutral"

        details = f"Analyzed {total_news} articles: {positive_count} positive, {negative_count} negative signals"

        return json.dumps(
            {
                "score": score,
                "positive_signals": positive_count,
                "negative_signals": negative_count,
                "overall_sentiment": overall_sentiment,
                "details": details,
            }
        )

    except Exception as e:
        return json.dumps(
            {
                "score": 5,
                "positive_signals": 0,
                "negative_signals": 0,
                "overall_sentiment": "neutral",
                "details": f"Error in sentiment analysis: {str(e)}",
            }
        )


def analyze_insider_signals(insider_data: str) -> str:
    """
    Analyze insider trading activity for management confidence signals:
    - Buy vs sell transaction analysis
    - Net insider activity trends
    - Management alignment assessment

    Args:
        insider_data: JSON string containing insider trading data

    Returns:
        JSON string with insider activity analysis
    """
    try:
        data = json.loads(insider_data)
        insider_trades = data.get("insider_trades", [])

        if not insider_trades:
            return json.dumps(
                {
                    "score": 5,  # Neutral
                    "buy_transactions": 0,
                    "sell_transactions": 0,
                    "net_activity": "neutral",
                    "details": "No insider trading data available",
                }
            )

        buy_count = 0
        sell_count = 0

        for trade in insider_trades:
            transaction_shares = trade.get("transaction_shares", 0)
            if transaction_shares > 0:
                buy_count += 1
            elif transaction_shares < 0:
                sell_count += 1

        total_transactions = buy_count + sell_count
        if total_transactions == 0:
            return json.dumps(
                {
                    "score": 5,
                    "buy_transactions": 0,
                    "sell_transactions": 0,
                    "net_activity": "neutral",
                    "details": "No clear buy/sell transactions found",
                }
            )

        buy_ratio = buy_count / total_transactions

        # Determine score and activity
        if buy_ratio > 0.7:
            score = 8  # Heavy buying
            net_activity = "buying"
        elif buy_ratio > 0.4:
            score = 6  # Moderate buying
            net_activity = "neutral"
        else:
            score = 4  # Mostly selling
            net_activity = "selling"

        details = f"Analyzed {total_transactions} transactions: {buy_count} buys vs {sell_count} sells"

        return json.dumps(
            {
                "score": score,
                "buy_transactions": buy_count,
                "sell_transactions": sell_count,
                "net_activity": net_activity,
                "details": details,
            }
        )

    except Exception as e:
        return json.dumps(
            {
                "score": 5,
                "buy_transactions": 0,
                "sell_transactions": 0,
                "net_activity": "neutral",
                "details": f"Error in insider analysis: {str(e)}",
            }
        )
