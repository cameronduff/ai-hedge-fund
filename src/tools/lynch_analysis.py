from typing import Annotated, Dict, Any, Optional, List
import math


def analyze_garp_metrics(
    financial_data: Annotated[
        Dict[str, Any],
        "Financial data including earnings, growth, and market cap for GARP analysis",
    ],
) -> Annotated[
    Dict[str, Any],
    "Growth at Reasonable Price analysis with PEG ratio focus and growth assessment",
]:
    """
    Analyze Growth at a Reasonable Price (GARP) using Peter Lynch's signature PEG ratio methodology.
    Focus on sustainable earnings growth combined with reasonable valuation multiples.

    Key metrics:
    - PEG ratio (P/E divided by growth rate) - Lynch's favorite metric
    - Earnings per share growth consistency and trajectory
    - Price-to-earnings ratio evaluation
    - Revenue growth supporting earnings expansion
    """
    try:
        analysis = {
            "peg_ratio": None,
            "pe_ratio": None,
            "eps_growth_rate": None,
            "revenue_growth_rate": None,
            "garp_score": 0,
            "score": 0,
            "max_score": 10,
            "details": [],
        }

        line_items = financial_data.get("line_items", [])
        market_cap = financial_data.get("market_cap")

        if not line_items or not market_cap:
            analysis["details"].append("Insufficient data for GARP analysis")
            return analysis

        # Extract EPS and earnings data
        eps_values = [
            item.get("earnings_per_share")
            for item in line_items
            if item.get("earnings_per_share") is not None
        ]
        net_incomes = [
            item.get("net_income")
            for item in line_items
            if item.get("net_income") is not None
        ]
        revenues = [
            item.get("revenue")
            for item in line_items
            if item.get("revenue") is not None
        ]

        # Calculate P/E ratio
        if net_incomes and net_incomes[0] and net_incomes[0] > 0:
            pe_ratio = market_cap / net_incomes[0]
            analysis["pe_ratio"] = pe_ratio
            analysis["details"].append(f"P/E ratio: {pe_ratio:.2f}")
        else:
            analysis["details"].append("Cannot calculate P/E - no positive earnings")

        # Calculate EPS growth rate (annualized)
        eps_growth_rate = None
        if len(eps_values) >= 3:  # Need at least 3 years for reliable growth
            latest_eps = eps_values[0]
            oldest_eps = eps_values[-1]

            if oldest_eps and oldest_eps > 0 and latest_eps and latest_eps > 0:
                years = len(eps_values) - 1
                eps_growth_rate = ((latest_eps / oldest_eps) ** (1 / years)) - 1
                analysis["eps_growth_rate"] = eps_growth_rate
                analysis["details"].append(
                    f"EPS CAGR: {eps_growth_rate:.1%} over {years} years"
                )
            elif len(eps_values) >= 2:
                # Simple growth if data is mixed
                recent_eps = eps_values[0]
                older_eps = eps_values[1]
                if older_eps and older_eps != 0:
                    simple_growth = (recent_eps - older_eps) / abs(older_eps)
                    eps_growth_rate = simple_growth
                    analysis["eps_growth_rate"] = eps_growth_rate
                    analysis["details"].append(
                        f"EPS simple growth: {eps_growth_rate:.1%}"
                    )

        # Calculate Revenue Growth
        if len(revenues) >= 2:
            latest_rev = revenues[0]
            oldest_rev = revenues[-1]
            if oldest_rev and oldest_rev > 0:
                years = len(revenues) - 1
                rev_growth_rate = ((latest_rev / oldest_rev) ** (1 / years)) - 1
                analysis["revenue_growth_rate"] = rev_growth_rate
                analysis["details"].append(f"Revenue CAGR: {rev_growth_rate:.1%}")

        # Calculate PEG Ratio - Lynch's signature metric
        if pe_ratio and eps_growth_rate and eps_growth_rate > 0:
            # PEG = P/E / (Growth Rate as percentage)
            peg_ratio = pe_ratio / (eps_growth_rate * 100)
            analysis["peg_ratio"] = peg_ratio

            # Score PEG ratio (6 points max)
            if peg_ratio < 0.5:  # Exceptional value
                analysis["score"] += 6
                analysis["garp_score"] = 10
                analysis["details"].append(
                    f"Exceptional PEG {peg_ratio:.2f} - potential ten-bagger"
                )
            elif peg_ratio < 1.0:  # Lynch's sweet spot
                analysis["score"] += 5
                analysis["garp_score"] = 9
                analysis["details"].append(
                    f"Excellent PEG {peg_ratio:.2f} - classic Lynch opportunity"
                )
            elif peg_ratio < 1.5:  # Good value
                analysis["score"] += 4
                analysis["garp_score"] = 7
                analysis["details"].append(
                    f"Good PEG {peg_ratio:.2f} - growth at reasonable price"
                )
            elif peg_ratio < 2.0:  # Fair value
                analysis["score"] += 2
                analysis["garp_score"] = 5
                analysis["details"].append(
                    f"Fair PEG {peg_ratio:.2f} - moderately attractive"
                )
            else:  # Expensive
                analysis["garp_score"] = 2
                analysis["details"].append(
                    f"High PEG {peg_ratio:.2f} - growth too expensive"
                )
        else:
            analysis["details"].append(
                "Cannot calculate PEG - missing P/E or growth data"
            )

        # Additional P/E scoring (2 points max)
        if pe_ratio:
            if pe_ratio < 15:  # Attractive multiple
                analysis["score"] += 2
                analysis["details"].append("Attractive P/E multiple")
            elif pe_ratio < 25:  # Reasonable multiple
                analysis["score"] += 1
                analysis["details"].append("Reasonable P/E multiple")
            else:
                analysis["details"].append("High P/E multiple")

        # Growth consistency check (2 points max)
        if eps_growth_rate:
            if eps_growth_rate > 0.20:  # >20% growth
                analysis["score"] += 2
                analysis["details"].append(
                    "Strong earnings growth - ten-bagger potential"
                )
            elif eps_growth_rate > 0.10:  # 10-20% growth
                analysis["score"] += 2
                analysis["details"].append("Solid earnings growth")
            elif eps_growth_rate > 0.05:  # 5-10% growth
                analysis["score"] += 1
                analysis["details"].append("Moderate earnings growth")
            else:
                analysis["details"].append("Weak earnings growth")

        return analysis

    except Exception as e:
        return {
            "error": f"GARP analysis failed: {str(e)}",
            "score": 0,
            "max_score": 10,
            "details": ["Error in GARP analysis"],
        }


def analyze_business_simplicity(
    financial_data: Annotated[
        Dict[str, Any],
        "Financial data for assessing business model simplicity and understandability",
    ],
) -> Annotated[
    Dict[str, Any],
    "Business simplicity analysis following Lynch's 'invest in what you know' philosophy",
]:
    """
    Analyze business simplicity and understandability using Lynch's preference for
    straightforward, easy-to-understand business models with predictable operations.

    Key factors:
    - Revenue and margin consistency (predictable business model)
    - Operating leverage and scalability
    - Balance sheet simplicity (low debt, strong fundamentals)
    - Cash flow predictability and quality
    """
    try:
        analysis = {
            "revenue_consistency": None,
            "margin_stability": None,
            "balance_sheet_health": None,
            "cash_flow_quality": None,
            "score": 0,
            "max_score": 8,
            "details": [],
        }

        line_items = financial_data.get("line_items", [])
        if not line_items:
            analysis["details"].append("No financial data for business analysis")
            return analysis

        # Revenue Consistency Analysis (2 points max)
        revenues = [item.get("revenue") for item in line_items if item.get("revenue")]
        if len(revenues) >= 3:
            # Calculate revenue volatility
            growth_rates = []
            for i in range(1, len(revenues)):
                if revenues[i] > 0:
                    growth = (revenues[i - 1] / revenues[i]) - 1
                    growth_rates.append(growth)

            if growth_rates:
                avg_growth = sum(growth_rates) / len(growth_rates)
                volatility = sum(abs(g - avg_growth) for g in growth_rates) / len(
                    growth_rates
                )

                analysis["revenue_consistency"] = {
                    "avg_growth": avg_growth,
                    "volatility": volatility,
                }

                if volatility < 0.10:  # Low volatility
                    analysis["score"] += 2
                    analysis["details"].append(
                        "Highly predictable revenue - simple business model"
                    )
                elif volatility < 0.20:  # Moderate volatility
                    analysis["score"] += 1
                    analysis["details"].append("Moderately predictable revenue")
                else:
                    analysis["details"].append(
                        "Volatile revenue - complex or cyclical business"
                    )
        else:
            analysis["details"].append(
                "Insufficient revenue history for consistency analysis"
            )

        # Margin Stability Analysis (2 points max)
        operating_margins = [
            item.get("operating_margin")
            for item in line_items
            if item.get("operating_margin")
        ]
        gross_margins = [
            item.get("gross_margin") for item in line_items if item.get("gross_margin")
        ]

        margins_to_check = operating_margins if operating_margins else gross_margins
        if len(margins_to_check) >= 3:
            margin_range = max(margins_to_check) - min(margins_to_check)
            avg_margin = sum(margins_to_check) / len(margins_to_check)

            analysis["margin_stability"] = {
                "avg_margin": avg_margin,
                "margin_range": margin_range,
            }

            if margin_range < 0.05 and avg_margin > 0.15:  # Stable + good margins
                analysis["score"] += 2
                analysis["details"].append(
                    f"Excellent margin stability - avg {avg_margin:.1%}"
                )
            elif margin_range < 0.10:  # Decent stability
                analysis["score"] += 1
                analysis["details"].append(f"Good margin consistency")
            else:
                analysis["details"].append(
                    "Volatile margins - business complexity or pricing pressure"
                )

        # Balance Sheet Health (2 points max)
        latest = line_items[0]
        debt = latest.get("total_debt", 0)
        equity = latest.get("shareholders_equity", 1)
        cash = latest.get("cash_and_equivalents", 0)

        if equity > 0:
            debt_to_equity = debt / equity
            net_cash = cash - debt

            analysis["balance_sheet_health"] = {
                "debt_to_equity": debt_to_equity,
                "net_cash": net_cash,
            }

            if debt_to_equity < 0.3 or net_cash > 0:  # Conservative balance sheet
                analysis["score"] += 2
                analysis["details"].append(
                    "Strong balance sheet - simple capital structure"
                )
            elif debt_to_equity < 0.7:  # Moderate leverage
                analysis["score"] += 1
                analysis["details"].append("Reasonable balance sheet")
            else:
                analysis["details"].append("High leverage - complex financing")

        # Cash Flow Quality (2 points max)
        fcf_values = [
            item.get("free_cash_flow")
            for item in line_items
            if item.get("free_cash_flow") is not None
        ]
        net_incomes = [
            item.get("net_income")
            for item in line_items
            if item.get("net_income") is not None
        ]

        if fcf_values and net_incomes and len(fcf_values) >= 2:
            # FCF conversion rate and consistency
            fcf_positive_years = sum(1 for fcf in fcf_values if fcf > 0)
            fcf_conversion_rates = []

            for i in range(min(len(fcf_values), len(net_incomes))):
                if net_incomes[i] and net_incomes[i] > 0:
                    conversion = fcf_values[i] / net_incomes[i]
                    fcf_conversion_rates.append(conversion)

            analysis["cash_flow_quality"] = {
                "positive_fcf_years": fcf_positive_years,
                "total_years": len(fcf_values),
                "avg_conversion": (
                    sum(fcf_conversion_rates) / len(fcf_conversion_rates)
                    if fcf_conversion_rates
                    else 0
                ),
            }

            if (
                fcf_positive_years == len(fcf_values)
                and fcf_conversion_rates
                and sum(fcf_conversion_rates) / len(fcf_conversion_rates) > 0.8
            ):
                analysis["score"] += 2
                analysis["details"].append(
                    "Excellent cash conversion - high quality earnings"
                )
            elif fcf_positive_years >= len(fcf_values) * 0.8:  # 80%+ positive FCF years
                analysis["score"] += 1
                analysis["details"].append("Good cash flow quality")
            else:
                analysis["details"].append("Inconsistent cash generation")

        return analysis

    except Exception as e:
        return {
            "error": f"Business simplicity analysis failed: {str(e)}",
            "score": 0,
            "max_score": 8,
            "details": ["Error in business simplicity analysis"],
        }


def analyze_ten_bagger_potential(
    financial_data: Annotated[
        Dict[str, Any], "Financial and market data for assessing ten-bagger potential"
    ],
) -> Annotated[
    Dict[str, Any], "Ten-bagger potential analysis for companies capable of 10x returns"
]:
    """
    Analyze ten-bagger potential using Lynch's criteria for identifying companies
    capable of generating 10x returns over 3-7 years through sustained growth.

    Key factors:
    - Sustained high growth rates (earnings and revenue)
    - Market expansion opportunity (addressable market size)
    - Competitive positioning and moat strength
    - Management execution track record
    - Reasonable starting valuation allowing for multiple expansion
    """
    try:
        analysis = {
            "growth_sustainability": None,
            "market_opportunity": None,
            "execution_track_record": None,
            "valuation_starting_point": None,
            "ten_bagger_score": 0,
            "score": 0,
            "max_score": 10,
            "details": [],
        }

        line_items = financial_data.get("line_items", [])
        market_cap = financial_data.get("market_cap")

        if not line_items:
            analysis["details"].append("No financial data for ten-bagger analysis")
            return analysis

        # Growth Sustainability Analysis (4 points max)
        revenues = [item.get("revenue") for item in line_items if item.get("revenue")]
        eps_values = [
            item.get("earnings_per_share")
            for item in line_items
            if item.get("earnings_per_share")
        ]

        if len(revenues) >= 3 and len(eps_values) >= 3:
            # Calculate multi-year growth rates
            revenue_cagr = (
                ((revenues[0] / revenues[-1]) ** (1 / (len(revenues) - 1))) - 1
                if revenues[-1] > 0
                else 0
            )

            # Check for positive EPS in recent years
            positive_eps_years = sum(1 for eps in eps_values[:3] if eps and eps > 0)

            analysis["growth_sustainability"] = {
                "revenue_cagr": revenue_cagr,
                "positive_eps_years": positive_eps_years,
                "consistency": positive_eps_years / min(3, len(eps_values)),
            }

            # Score based on growth quality
            if (
                revenue_cagr > 0.25 and positive_eps_years >= 2
            ):  # >25% revenue growth + profitable
                analysis["score"] += 4
                analysis["ten_bagger_score"] += 4
                analysis["details"].append(
                    f"Exceptional growth {revenue_cagr:.1%} CAGR - strong ten-bagger candidate"
                )
            elif (
                revenue_cagr > 0.15 and positive_eps_years >= 2
            ):  # 15-25% growth + profitable
                analysis["score"] += 3
                analysis["ten_bagger_score"] += 3
                analysis["details"].append(
                    f"Strong growth {revenue_cagr:.1%} CAGR - ten-bagger potential"
                )
            elif revenue_cagr > 0.10:  # 10-15% growth
                analysis["score"] += 2
                analysis["ten_bagger_score"] += 2
                analysis["details"].append(
                    f"Solid growth {revenue_cagr:.1%} - moderate potential"
                )
            else:
                analysis["details"].append(
                    f"Modest growth {revenue_cagr:.1%} - limited ten-bagger potential"
                )

        # Execution Track Record (3 points max)
        # Analyze operating leverage and efficiency improvements
        operating_margins = [
            item.get("operating_margin")
            for item in line_items
            if item.get("operating_margin")
        ]

        if len(operating_margins) >= 3:
            margin_trend = (
                operating_margins[0] - operating_margins[-1]
            )  # Recent - oldest
            avg_margin = sum(operating_margins) / len(operating_margins)

            analysis["execution_track_record"] = {
                "margin_trend": margin_trend,
                "avg_margin": avg_margin,
                "improving_efficiency": margin_trend > 0,
            }

            if (
                margin_trend > 0.05 and avg_margin > 0.15
            ):  # Improving margins + good profitability
                analysis["score"] += 3
                analysis["ten_bagger_score"] += 3
                analysis["details"].append(
                    "Excellent execution - expanding margins and profitability"
                )
            elif (
                margin_trend > 0 or avg_margin > 0.10
            ):  # Either improving or decent margins
                analysis["score"] += 2
                analysis["ten_bagger_score"] += 2
                analysis["details"].append("Good execution track record")
            else:
                analysis["details"].append(
                    "Mixed execution - margin pressure or low profitability"
                )

        # Valuation Starting Point (3 points max)
        if market_cap:
            # Assess if valuation allows for multiple expansion
            net_incomes = [
                item.get("net_income") for item in line_items if item.get("net_income")
            ]

            if net_incomes and net_incomes[0] and net_incomes[0] > 0:
                current_pe = market_cap / net_incomes[0]

                analysis["valuation_starting_point"] = {
                    "current_pe": current_pe,
                    "market_cap_billions": market_cap / 1e9,
                }

                # Ten-baggers often start from reasonable valuations
                if (
                    current_pe < 20 and market_cap < 10e9
                ):  # P/E <20 and <$10B market cap
                    analysis["score"] += 3
                    analysis["ten_bagger_score"] += 3
                    analysis["details"].append(
                        f"Attractive starting point - P/E {current_pe:.1f}, ${market_cap/1e9:.1f}B market cap"
                    )
                elif (
                    current_pe < 30 and market_cap < 50e9
                ):  # Moderate valuation and size
                    analysis["score"] += 2
                    analysis["ten_bagger_score"] += 2
                    analysis["details"].append(
                        f"Reasonable starting point - P/E {current_pe:.1f}"
                    )
                elif current_pe < 40:  # Still reasonable for growth
                    analysis["score"] += 1
                    analysis["ten_bagger_score"] += 1
                    analysis["details"].append(
                        f"Fair starting valuation - P/E {current_pe:.1f}"
                    )
                else:
                    analysis["details"].append(
                        f"High starting valuation - P/E {current_pe:.1f} limits upside"
                    )

        # Overall Ten-Bagger Assessment
        if analysis["ten_bagger_score"] >= 8:
            analysis["ten_bagger_probability"] = "high"
            analysis["details"].append(
                "HIGH ten-bagger potential - exceptional growth + execution + valuation"
            )
        elif analysis["ten_bagger_score"] >= 6:
            analysis["ten_bagger_probability"] = "moderate"
            analysis["details"].append(
                "MODERATE ten-bagger potential - good fundamentals with upside"
            )
        elif analysis["ten_bagger_score"] >= 3:
            analysis["ten_bagger_probability"] = "low"
            analysis["details"].append(
                "LIMITED ten-bagger potential - some positives but missing key elements"
            )
        else:
            analysis["ten_bagger_probability"] = "minimal"
            analysis["details"].append(
                "MINIMAL ten-bagger potential - lacks growth, execution, or valuation appeal"
            )

        return analysis

    except Exception as e:
        return {
            "error": f"Ten-bagger analysis failed: {str(e)}",
            "score": 0,
            "max_score": 10,
            "details": ["Error in ten-bagger analysis"],
        }


def analyze_lynch_sentiment(
    market_data: Annotated[
        Dict[str, Any],
        "News and market sentiment data for Lynch-style sentiment analysis",
    ],
) -> Annotated[
    Dict[str, Any],
    "Sentiment analysis focusing on market overreaction and contrarian opportunities",
]:
    """
    Analyze market sentiment using Lynch's approach of finding opportunities
    in temporarily out-of-favor stocks with strong fundamentals.

    Key factors:
    - News sentiment and media coverage tone
    - Market overreaction to temporary setbacks
    - Insider buying during negative sentiment periods
    - Disconnect between short-term sentiment and long-term prospects
    """
    try:
        analysis = {
            "news_sentiment": None,
            "insider_conviction": None,
            "market_overreaction": None,
            "score": 0,
            "max_score": 6,
            "details": [],
        }

        news_data = market_data.get("news", [])
        insider_data = market_data.get("insider_trades", [])

        # News Sentiment Analysis (3 points max)
        if news_data:
            negative_keywords = [
                "lawsuit",
                "fraud",
                "investigation",
                "decline",
                "downturn",
                "loss",
                "warning",
                "concern",
                "risk",
                "challenge",
            ]
            positive_keywords = [
                "growth",
                "expansion",
                "success",
                "beat",
                "strong",
                "increase",
                "improvement",
                "opportunity",
                "innovation",
            ]

            negative_count = 0
            positive_count = 0

            for news_item in news_data:
                title = (news_item.get("title") or "").lower()
                if any(keyword in title for keyword in negative_keywords):
                    negative_count += 1
                if any(keyword in title for keyword in positive_keywords):
                    positive_count += 1

            total_articles = len(news_data)
            negative_ratio = (
                negative_count / total_articles if total_articles > 0 else 0
            )
            positive_ratio = (
                positive_count / total_articles if total_articles > 0 else 0
            )

            analysis["news_sentiment"] = {
                "negative_ratio": negative_ratio,
                "positive_ratio": positive_ratio,
                "total_articles": total_articles,
            }

            # Lynch likes buying when others are pessimistic (contrarian)
            if negative_ratio > 0.6:  # >60% negative - potential overreaction
                analysis["score"] += 3
                analysis["details"].append(
                    f"Heavy negative sentiment {negative_ratio:.0%} - potential Lynch opportunity"
                )
            elif negative_ratio > 0.4:  # 40-60% negative - moderate pessimism
                analysis["score"] += 2
                analysis["details"].append(
                    f"Moderate negative sentiment {negative_ratio:.0%} - some opportunity"
                )
            elif positive_ratio > 0.6:  # Too much optimism
                analysis["score"] += 1
                analysis["details"].append(
                    f"Heavy positive sentiment {positive_ratio:.0%} - potential overvaluation"
                )
            else:  # Balanced sentiment
                analysis["score"] += 2
                analysis["details"].append("Balanced news sentiment")
        else:
            analysis["score"] += 2  # Neutral if no news
            analysis["details"].append("No recent news - neutral sentiment")

        # Insider Activity Analysis (3 points max)
        if insider_data:
            buys = sum(
                1 for trade in insider_data if trade.get("transaction_shares", 0) > 0
            )
            sells = sum(
                1 for trade in insider_data if trade.get("transaction_shares", 0) < 0
            )
            total_trades = buys + sells

            if total_trades > 0:
                buy_ratio = buys / total_trades

                analysis["insider_conviction"] = {
                    "buy_ratio": buy_ratio,
                    "total_trades": total_trades,
                    "buys": buys,
                    "sells": sells,
                }

                if buy_ratio > 0.7:  # Heavy insider buying
                    analysis["score"] += 3
                    analysis["details"].append(
                        f"Strong insider buying {buys} vs {sells} - management conviction"
                    )
                elif buy_ratio > 0.5:  # Net insider buying
                    analysis["score"] += 2
                    analysis["details"].append(f"Net insider buying {buys} vs {sells}")
                elif buy_ratio > 0.3:  # Some insider buying
                    analysis["score"] += 1
                    analysis["details"].append(
                        f"Mixed insider activity {buys} vs {sells}"
                    )
                else:  # Mostly selling
                    analysis["details"].append(
                        f"Heavy insider selling {buys} vs {sells}"
                    )
            else:
                analysis["score"] += 1  # Neutral if no meaningful trades
                analysis["details"].append("No significant insider trading activity")
        else:
            analysis["score"] += 1  # Neutral if no insider data
            analysis["details"].append("No insider trading data available")

        return analysis

    except Exception as e:
        return {
            "error": f"Lynch sentiment analysis failed: {str(e)}",
            "score": 0,
            "max_score": 6,
            "details": ["Error in sentiment analysis"],
        }


def calculate_lynch_score(
    analysis_results: Annotated[
        Dict[str, Any], "Combined analysis results from all Lynch methodology tools"
    ],
) -> Annotated[
    Dict[str, Any],
    "Overall Peter Lynch investment score and GARP assessment with ten-bagger evaluation",
]:
    """
    Calculate overall Peter Lynch investment score emphasizing his GARP methodology
    and ten-bagger identification with practical, understandable business focus.

    Scoring weights (reflecting Lynch priorities):
    - GARP Metrics (PEG focus): 35% weight
    - Ten-bagger Potential: 30% weight
    - Business Simplicity: 20% weight
    - Market Sentiment: 15% weight

    Lynch's approach favors growth companies at reasonable prices with clear ten-bagger potential.
    """
    try:
        # Extract individual analysis scores
        garp_analysis = analysis_results.get("garp_analysis", {})
        simplicity_analysis = analysis_results.get("simplicity_analysis", {})
        ten_bagger_analysis = analysis_results.get("ten_bagger_analysis", {})
        sentiment_analysis = analysis_results.get("sentiment_analysis", {})

        # Calculate weighted score based on Lynch's priorities
        garp_score = garp_analysis.get("score", 0)  # max 10
        simplicity_score = simplicity_analysis.get("score", 0)  # max 8
        ten_bagger_score = ten_bagger_analysis.get("score", 0)  # max 10
        sentiment_score = sentiment_analysis.get("score", 0)  # max 6

        # Weighted calculation reflecting Lynch's emphasis
        weighted_score = (
            (garp_score / 10) * 35  # 35% weight on GARP metrics
            + (ten_bagger_score / 10) * 30  # 30% weight on ten-bagger potential
            + (simplicity_score / 8) * 20  # 20% weight on business simplicity
            + (sentiment_score / 6) * 15  # 15% weight on sentiment
        )

        score_percentage = weighted_score

        # Lynch's criteria for investment signals
        peg_ratio = garp_analysis.get("peg_ratio")
        ten_bagger_probability = ten_bagger_analysis.get(
            "ten_bagger_probability", "minimal"
        )

        # Signal determination with Lynch's preferences
        if (
            score_percentage >= 75
            and peg_ratio
            and peg_ratio < 1.5
            and ten_bagger_probability in ["high", "moderate"]
        ):
            signal = "bullish"
            conviction = "high"
        elif score_percentage >= 65 and (
            (peg_ratio and peg_ratio < 2.0) or ten_bagger_probability == "moderate"
        ):
            signal = "bullish"
            conviction = "moderate"
        elif score_percentage <= 35 or (peg_ratio and peg_ratio > 3.0):
            signal = "bearish"
            conviction = "high"
        else:
            signal = "neutral"
            conviction = "low"

        # Assess key Lynch criteria
        strengths = []
        concerns = []
        lynch_checklist = []

        # PEG ratio assessment
        if peg_ratio:
            if peg_ratio < 1.0:
                strengths.append("Excellent PEG ratio")
                lynch_checklist.append(
                    f"✓ PEG {peg_ratio:.2f} - Growth at reasonable price"
                )
            elif peg_ratio < 2.0:
                lynch_checklist.append(f"✓ PEG {peg_ratio:.2f} - Acceptable GARP")
            else:
                concerns.append("High PEG ratio")
                lynch_checklist.append(f"✗ PEG {peg_ratio:.2f} - Growth too expensive")
        else:
            lynch_checklist.append("? PEG ratio unavailable")

        # Ten-bagger potential
        if ten_bagger_probability == "high":
            strengths.append("Strong ten-bagger potential")
            lynch_checklist.append("✓ High ten-bagger potential")
        elif ten_bagger_probability == "moderate":
            lynch_checklist.append("✓ Moderate ten-bagger potential")
        else:
            lynch_checklist.append("✗ Limited ten-bagger potential")

        # Business simplicity
        if simplicity_score >= 6:
            strengths.append("Simple, understandable business")
            lynch_checklist.append("✓ Simple business model")
        elif simplicity_score >= 4:
            lynch_checklist.append("~ Moderately complex business")
        else:
            concerns.append("Complex business model")
            lynch_checklist.append("✗ Complex or unpredictable business")

        # Growth assessment
        eps_growth = garp_analysis.get("eps_growth_rate")
        if eps_growth and eps_growth > 0.15:
            strengths.append("Strong earnings growth")
        elif eps_growth and eps_growth > 0.05:
            lynch_checklist.append("✓ Reasonable earnings growth")
        else:
            concerns.append("Weak earnings growth")

        # Market sentiment
        news_sentiment = sentiment_analysis.get("news_sentiment", {})
        negative_ratio = news_sentiment.get("negative_ratio", 0)
        if negative_ratio > 0.5:
            strengths.append("Contrarian opportunity (negative sentiment)")

        # Overall Lynch assessment
        analysis_summary = {
            "total_score": weighted_score,
            "max_score": 100,
            "score_percentage": score_percentage,
            "signal": signal,
            "conviction": conviction,
            "strengths": strengths,
            "concerns": concerns,
            "lynch_checklist": lynch_checklist,
            "component_scores": {
                "garp_metrics": f"{garp_score:.1f}/10",
                "ten_bagger_potential": f"{ten_bagger_score:.1f}/10",
                "business_simplicity": f"{simplicity_score:.1f}/8",
                "market_sentiment": f"{sentiment_score:.1f}/6",
            },
            "key_metrics": {
                "peg_ratio": peg_ratio,
                "pe_ratio": garp_analysis.get("pe_ratio"),
                "eps_growth_rate": eps_growth,
                "ten_bagger_probability": ten_bagger_probability,
                "revenue_growth": garp_analysis.get("revenue_growth_rate"),
                "insider_conviction": sentiment_analysis.get("insider_conviction"),
            },
            "lynch_philosophy": {
                "garp_criteria_met": peg_ratio and peg_ratio < 2.0,
                "ten_bagger_potential": ten_bagger_probability in ["high", "moderate"],
                "understandable_business": simplicity_score >= 4,
                "overall_lynch_appeal": score_percentage >= 65
                and (peg_ratio is None or peg_ratio < 2.5),
            },
        }

        return analysis_summary

    except Exception as e:
        return {
            "error": f"Lynch score calculation failed: {str(e)}",
            "total_score": 0,
            "max_score": 100,
            "score_percentage": 0,
            "signal": "neutral",
            "conviction": "none",
            "lynch_checklist": ["Error in analysis"],
        }
