from typing import Annotated, Dict, Any, Optional
import json


def analyze_deep_value_metrics(
    financial_data: Annotated[
        Dict[str, Any], "Financial metrics and market data for the company"
    ],
) -> Annotated[
    Dict[str, Any],
    "Deep value analysis including FCF yield, EV/EBIT, and value scoring",
]:
    """
    Analyze deep value metrics using Michael Burry's approach focusing on free cash flow yield,
    EV/EBIT ratios, and other classic value indicators.

    Key metrics:
    - Free Cash Flow Yield (FCF/Market Cap) - Burry's preferred metric
    - EV/EBIT ratio for operational efficiency
    - Price-to-Book ratio for asset backing
    - Working capital efficiency
    """
    try:
        analysis = {
            "fcf_yield": None,
            "ev_ebit": None,
            "price_to_book": None,
            "score": 0,
            "max_score": 6,
            "details": [],
        }

        # Extract key financial metrics
        market_cap = financial_data.get("market_cap")
        metrics = financial_data.get("metrics", [])
        line_items = financial_data.get("line_items", [])

        # Get latest financial data
        latest_metrics = metrics[0] if metrics else {}
        latest_item = line_items[0] if line_items else {}

        # Free Cash Flow Yield Analysis (4 points max)
        fcf = latest_item.get("free_cash_flow")
        if fcf and market_cap and market_cap > 0:
            fcf_yield = fcf / market_cap
            analysis["fcf_yield"] = fcf_yield

            if fcf_yield >= 0.15:  # 15%+ FCF yield
                analysis["score"] += 4
                analysis["details"].append(
                    f"Extraordinary FCF yield {fcf_yield:.1%} - classic Burry territory"
                )
            elif fcf_yield >= 0.12:  # 12-15% FCF yield
                analysis["score"] += 3
                analysis["details"].append(
                    f"Very high FCF yield {fcf_yield:.1%} - deep value opportunity"
                )
            elif fcf_yield >= 0.08:  # 8-12% FCF yield
                analysis["score"] += 2
                analysis["details"].append(
                    f"Respectable FCF yield {fcf_yield:.1%} - moderate value"
                )
            else:
                analysis["details"].append(
                    f"Low FCF yield {fcf_yield:.1%} - insufficient value"
                )
        else:
            analysis["details"].append(
                "FCF data unavailable - cannot assess primary value metric"
            )

        # EV/EBIT Analysis (2 points max)
        ev_ebit = latest_metrics.get("ev_to_ebit")
        if ev_ebit:
            analysis["ev_ebit"] = ev_ebit

            if ev_ebit < 6:  # Very cheap operational multiple
                analysis["score"] += 2
                analysis["details"].append(
                    f"EV/EBIT {ev_ebit:.1f} - significantly undervalued operations"
                )
            elif ev_ebit < 10:  # Reasonable operational multiple
                analysis["score"] += 1
                analysis["details"].append(
                    f"EV/EBIT {ev_ebit:.1f} - moderately valued operations"
                )
            else:
                analysis["details"].append(
                    f"High EV/EBIT {ev_ebit:.1f} - expensive operations"
                )
        else:
            analysis["details"].append(
                "EV/EBIT unavailable - missing operational valuation metric"
            )

        # Additional value context
        pb_ratio = latest_metrics.get("price_to_book")
        if pb_ratio:
            analysis["price_to_book"] = pb_ratio
            if pb_ratio < 1.0:
                analysis["details"].append(
                    f"Trading below book value (P/B {pb_ratio:.2f}) - asset backing"
                )
            elif pb_ratio < 2.0:
                analysis["details"].append(f"Reasonable P/B ratio {pb_ratio:.2f}")
            else:
                analysis["details"].append(
                    f"High P/B ratio {pb_ratio:.2f} - limited asset backing"
                )

        return analysis

    except Exception as e:
        return {
            "error": f"Value analysis failed: {str(e)}",
            "score": 0,
            "max_score": 6,
            "details": ["Error in value analysis - data processing failed"],
        }


def analyze_balance_sheet_strength(
    financial_data: Annotated[
        Dict[str, Any], "Balance sheet and financial strength data"
    ],
) -> Annotated[
    Dict[str, Any], "Balance sheet analysis focusing on leverage and liquidity risks"
]:
    """
    Analyze balance sheet strength with Burry's focus on avoiding leverage traps and
    identifying companies with financial fortress characteristics.

    Key checks:
    - Debt-to-equity ratios (avoid overleveraged companies)
    - Cash vs debt position (net cash preferred)
    - Interest coverage ratios
    - Working capital adequacy
    """
    try:
        analysis = {
            "debt_to_equity": None,
            "net_cash_position": None,
            "interest_coverage": None,
            "score": 0,
            "max_score": 4,
            "details": [],
        }

        metrics = financial_data.get("metrics", [])
        line_items = financial_data.get("line_items", [])

        latest_metrics = metrics[0] if metrics else {}
        latest_item = line_items[0] if line_items else {}

        # Debt-to-Equity Analysis (2 points max)
        debt_to_equity = latest_metrics.get("debt_to_equity")
        if debt_to_equity is not None:
            analysis["debt_to_equity"] = debt_to_equity

            if debt_to_equity < 0.3:  # Very conservative leverage
                analysis["score"] += 2
                analysis["details"].append(
                    f"Exceptional balance sheet - D/E {debt_to_equity:.2f}"
                )
            elif debt_to_equity < 0.5:  # Low leverage
                analysis["score"] += 2
                analysis["details"].append(
                    f"Strong balance sheet - D/E {debt_to_equity:.2f}"
                )
            elif debt_to_equity < 1.0:  # Moderate leverage
                analysis["score"] += 1
                analysis["details"].append(
                    f"Acceptable leverage - D/E {debt_to_equity:.2f}"
                )
            else:  # High leverage - Burry avoids
                analysis["details"].append(
                    f"High leverage risk - D/E {debt_to_equity:.2f}"
                )
        else:
            analysis["details"].append(
                "Debt-to-equity unavailable - cannot assess leverage risk"
            )

        # Cash vs Debt Position (2 points max)
        cash = latest_item.get("cash_and_equivalents")
        total_debt = latest_item.get("total_debt")

        if cash is not None and total_debt is not None:
            net_cash = cash - total_debt
            analysis["net_cash_position"] = net_cash

            if net_cash > 0:
                net_cash_ratio = cash / max(total_debt, 1)
                if net_cash_ratio > 2.0:  # Cash > 2x debt
                    analysis["score"] += 2
                    analysis["details"].append(
                        f"Fortress balance sheet - net cash ${net_cash/1e9:.1f}B"
                    )
                else:
                    analysis["score"] += 1
                    analysis["details"].append(
                        f"Net cash position - ${net_cash/1e9:.1f}B cushion"
                    )
            else:
                analysis["details"].append(
                    f"Net debt position - ${abs(net_cash)/1e9:.1f}B"
                )
        else:
            analysis["details"].append(
                "Cash/debt data unavailable - cannot assess liquidity"
            )

        # Interest Coverage Context
        interest_coverage = latest_metrics.get("interest_coverage_ratio")
        if interest_coverage:
            analysis["interest_coverage"] = interest_coverage
            if interest_coverage > 10:
                analysis["details"].append(
                    f"Excellent interest coverage {interest_coverage:.1f}x"
                )
            elif interest_coverage > 5:
                analysis["details"].append(
                    f"Adequate interest coverage {interest_coverage:.1f}x"
                )
            else:
                analysis["details"].append(
                    f"Weak interest coverage {interest_coverage:.1f}x - risk"
                )

        return analysis

    except Exception as e:
        return {
            "error": f"Balance sheet analysis failed: {str(e)}",
            "score": 0,
            "max_score": 4,
            "details": ["Error in balance sheet analysis"],
        }


def analyze_insider_activity(
    insider_data: Annotated[
        Dict[str, Any], "Insider trading activity data over past 12 months"
    ],
) -> Annotated[
    Dict[str, Any],
    "Analysis of insider buying/selling patterns as hard catalyst indicator",
]:
    """
    Analyze insider trading activity focusing on net insider buying as a hard catalyst.
    Burry looks for insider conviction through significant purchases by key executives.

    Key indicators:
    - Net insider buying vs selling
    - Size and frequency of insider purchases
    - Executive level of insider activity
    - Timing relative to stock performance
    """
    try:
        analysis = {
            "net_insider_shares": 0,
            "insider_conviction": "none",
            "score": 0,
            "max_score": 3,
            "details": [],
        }

        insider_trades = insider_data.get("insider_trades", [])

        if not insider_trades:
            analysis["details"].append("No insider trading data available")
            return analysis

        # Calculate net insider activity
        shares_bought = sum(
            trade.get("transaction_shares", 0)
            for trade in insider_trades
            if (trade.get("transaction_shares", 0) or 0) > 0
        )

        shares_sold = abs(
            sum(
                trade.get("transaction_shares", 0)
                for trade in insider_trades
                if (trade.get("transaction_shares", 0) or 0) < 0
            )
        )

        net_shares = shares_bought - shares_sold
        analysis["net_insider_shares"] = net_shares

        # Score based on insider activity
        if net_shares > 0:
            buy_sell_ratio = shares_bought / max(shares_sold, 1)

            if buy_sell_ratio > 3.0:  # Heavy buying vs selling
                analysis["score"] += 3
                analysis["insider_conviction"] = "strong"
                analysis["details"].append(
                    f"Strong insider conviction - net buying {net_shares:,} shares"
                )
            elif buy_sell_ratio > 1.5:  # Moderate buying bias
                analysis["score"] += 2
                analysis["insider_conviction"] = "moderate"
                analysis["details"].append(
                    f"Moderate insider buying - net {net_shares:,} shares"
                )
            else:  # Light buying
                analysis["score"] += 1
                analysis["insider_conviction"] = "weak"
                analysis["details"].append(
                    f"Light insider buying - net {net_shares:,} shares"
                )
        else:
            analysis["insider_conviction"] = "negative"
            analysis["details"].append(
                f"Net insider selling - {abs(net_shares):,} shares"
            )

        # Additional context on insider activity
        total_trades = len(insider_trades)
        buy_trades = len(
            [t for t in insider_trades if (t.get("transaction_shares", 0) or 0) > 0]
        )

        if total_trades > 0:
            buy_percentage = (buy_trades / total_trades) * 100
            analysis["details"].append(
                f"{buy_percentage:.0f}% of insider trades were purchases ({buy_trades}/{total_trades})"
            )

        return analysis

    except Exception as e:
        return {
            "error": f"Insider analysis failed: {str(e)}",
            "score": 0,
            "max_score": 3,
            "details": ["Error analyzing insider activity"],
        }


def analyze_contrarian_sentiment(
    market_data: Annotated[Dict[str, Any], "News sentiment and market perception data"],
) -> Annotated[
    Dict[str, Any],
    "Contrarian sentiment analysis - negative news as opportunity indicator",
]:
    """
    Analyze contrarian sentiment opportunities where excessive negative sentiment
    creates value opportunities. Burry profits from being early and contrarian.

    Key factors:
    - Volume of negative news coverage
    - Sentiment extremes in recent coverage
    - Market overreaction indicators
    - Disconnect between fundamentals and sentiment
    """
    try:
        analysis = {
            "negative_sentiment_count": 0,
            "contrarian_opportunity": False,
            "sentiment_extreme": False,
            "score": 0,
            "max_score": 2,
            "details": [],
        }

        news_data = market_data.get("news", [])

        if not news_data:
            analysis["details"].append("No recent news data for sentiment analysis")
            return analysis

        # Count negative sentiment articles
        negative_articles = [
            article
            for article in news_data
            if article.get("sentiment", "").lower()
            in ["negative", "bearish", "very negative"]
        ]

        neutral_articles = [
            article
            for article in news_data
            if article.get("sentiment", "").lower() in ["neutral", "mixed"]
        ]

        positive_articles = [
            article
            for article in news_data
            if article.get("sentiment", "").lower()
            in ["positive", "bullish", "very positive"]
        ]

        total_articles = len(news_data)
        negative_count = len(negative_articles)
        analysis["negative_sentiment_count"] = negative_count

        if total_articles == 0:
            analysis["details"].append("No sentiment data available")
            return analysis

        negative_percentage = (negative_count / total_articles) * 100

        # Score contrarian opportunities
        if negative_count >= 10 and negative_percentage > 70:  # Extreme negativity
            analysis["score"] += 2
            analysis["contrarian_opportunity"] = True
            analysis["sentiment_extreme"] = True
            analysis["details"].append(
                f"Extreme negativity - {negative_count} negative articles ({negative_percentage:.0f}%) - major contrarian opportunity"
            )
        elif negative_count >= 5 and negative_percentage > 60:  # High negativity
            analysis["score"] += 1
            analysis["contrarian_opportunity"] = True
            analysis["details"].append(
                f"High negativity - {negative_count} negative articles ({negative_percentage:.0f}%) - contrarian opportunity"
            )
        elif negative_percentage > 50:  # Moderate negativity
            analysis["contrarian_opportunity"] = True
            analysis["details"].append(
                f"Moderate negativity - {negative_count} negative articles ({negative_percentage:.0f}%) - potential opportunity"
            )
        else:  # Limited negative sentiment
            analysis["details"].append(
                f"Limited negative sentiment - {negative_count} negative articles ({negative_percentage:.0f}%)"
            )

        # Additional sentiment context
        if len(positive_articles) > len(negative_articles):
            analysis["details"].append(
                "Positive sentiment dominates - limited contrarian appeal"
            )
        elif len(negative_articles) > 2 * len(positive_articles):
            analysis["details"].append(
                "Overwhelmingly negative sentiment - classic Burry setup if fundamentals hold"
            )

        return analysis

    except Exception as e:
        return {
            "error": f"Sentiment analysis failed: {str(e)}",
            "score": 0,
            "max_score": 2,
            "details": ["Error analyzing contrarian sentiment"],
        }


def calculate_burry_score(
    analysis_results: Annotated[
        Dict[str, Any], "Combined analysis results from all Burry methodology tools"
    ],
) -> Annotated[
    Dict[str, Any], "Overall Burry investment score and recommendation synthesis"
]:
    """
    Calculate overall Michael Burry investment score by combining deep value metrics,
    balance sheet strength, insider activity, and contrarian sentiment analysis.

    Scoring methodology:
    - Deep Value Metrics: 40% weight (6/15 points)
    - Balance Sheet Strength: 27% weight (4/15 points)
    - Insider Activity: 20% weight (3/15 points)
    - Contrarian Sentiment: 13% weight (2/15 points)

    Returns overall score, signal recommendation, and key supporting factors.
    """
    try:
        # Extract individual analysis scores
        value_analysis = analysis_results.get("value_analysis", {})
        balance_sheet_analysis = analysis_results.get("balance_sheet_analysis", {})
        insider_analysis = analysis_results.get("insider_analysis", {})
        sentiment_analysis = analysis_results.get("sentiment_analysis", {})

        # Calculate total score
        total_score = (
            value_analysis.get("score", 0)
            + balance_sheet_analysis.get("score", 0)
            + insider_analysis.get("score", 0)
            + sentiment_analysis.get("score", 0)
        )

        max_total_score = (
            value_analysis.get("max_score", 6)
            + balance_sheet_analysis.get("max_score", 4)
            + insider_analysis.get("max_score", 3)
            + sentiment_analysis.get("max_score", 2)
        )

        # Calculate percentage score
        score_percentage = (
            (total_score / max_total_score) * 100 if max_total_score > 0 else 0
        )

        # Determine signal based on Burry's high standards
        if score_percentage >= 75:  # 75%+ = Strong conviction
            signal = "bullish"
            conviction = "high"
        elif score_percentage >= 60:  # 60-75% = Moderate opportunity
            signal = "bullish"
            conviction = "moderate"
        elif score_percentage <= 25:  # 25% or less = Clear avoid
            signal = "bearish"
            conviction = "high"
        else:  # 25-60% = Neutral/wait
            signal = "neutral"
            conviction = "low"

        # Key strengths and concerns
        strengths = []
        concerns = []

        # Analyze key factors
        if value_analysis.get("score", 0) >= 4:
            strengths.append("Exceptional deep value metrics")
        elif value_analysis.get("score", 0) >= 2:
            strengths.append("Solid value characteristics")
        else:
            concerns.append("Insufficient value pricing")

        if balance_sheet_analysis.get("score", 0) >= 3:
            strengths.append("Fortress balance sheet")
        elif balance_sheet_analysis.get("score", 0) <= 1:
            concerns.append("Balance sheet risks")

        if insider_analysis.get("score", 0) >= 2:
            strengths.append("Strong insider conviction")

        if sentiment_analysis.get("contrarian_opportunity"):
            strengths.append("Contrarian opportunity setup")

        # Compile analysis summary
        analysis_summary = {
            "total_score": total_score,
            "max_score": max_total_score,
            "score_percentage": score_percentage,
            "signal": signal,
            "conviction": conviction,
            "strengths": strengths,
            "concerns": concerns,
            "component_scores": {
                "deep_value": f"{value_analysis.get('score', 0)}/{value_analysis.get('max_score', 6)}",
                "balance_sheet": f"{balance_sheet_analysis.get('score', 0)}/{balance_sheet_analysis.get('max_score', 4)}",
                "insider_activity": f"{insider_analysis.get('score', 0)}/{insider_analysis.get('max_score', 3)}",
                "contrarian_sentiment": f"{sentiment_analysis.get('score', 0)}/{sentiment_analysis.get('max_score', 2)}",
            },
            "key_metrics": {
                "fcf_yield": value_analysis.get("fcf_yield"),
                "ev_ebit": value_analysis.get("ev_ebit"),
                "debt_to_equity": balance_sheet_analysis.get("debt_to_equity"),
                "net_insider_shares": insider_analysis.get("net_insider_shares"),
                "negative_sentiment_count": sentiment_analysis.get(
                    "negative_sentiment_count"
                ),
            },
        }

        return analysis_summary

    except Exception as e:
        return {
            "error": f"Burry score calculation failed: {str(e)}",
            "total_score": 0,
            "max_score": 15,
            "score_percentage": 0,
            "signal": "neutral",
            "conviction": "none",
        }
