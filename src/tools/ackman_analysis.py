"""
Bill Ackman-style financial analysis tools.
Implements his business quality assessment, activism potential evaluation, and concentrated investment approach.
"""

from typing import Dict, List, Optional, Any, Annotated
import json
from loguru import logger


def analyze_business_quality(
    financial_data: Annotated[
        Dict[str, Any],
        "Dictionary containing multiple periods of financial metrics including revenue_history, operating_margin, return_on_equity, free_cash_flow",
    ],
) -> Dict[str, Any]:
    """
    Analyze business quality following Bill Ackman's criteria for high-quality businesses.

    Ackman focuses on businesses with durable competitive advantages, consistent cash flow generation,
    and strong brand moats. Scoring criteria:
    - +2 points: Strong revenue growth (>50% cumulative over period)
    - +1 point: Moderate revenue growth (positive but <50%)
    - +2 points: Operating margins consistently >15% (indicates pricing power/moat)
    - +1 point: Consistently positive free cash flow (cash generation ability)
    - +2 points: High ROE >15% (efficient capital deployment, competitive advantage)

    Args:
        financial_data: Dictionary containing revenue_history, operating_margin, free_cash_flow, return_on_equity

    Returns:
        Dict with business quality score and detailed analysis
    """
    score = 0
    details = []
    max_score = 7

    try:
        revenue_history = financial_data.get("revenue_history", [])
        operating_margins = financial_data.get("operating_margin_history", [])
        fcf_history = financial_data.get("free_cash_flow_history", [])
        return_on_equity = financial_data.get("return_on_equity", 0)

        # 1. Revenue Growth Analysis (Ackman likes sustainable growth)
        if len(revenue_history) >= 2:
            initial_revenue = revenue_history[-1]  # Oldest
            final_revenue = revenue_history[0]  # Newest

            if initial_revenue and final_revenue and initial_revenue > 0:
                growth_rate = (final_revenue - initial_revenue) / abs(initial_revenue)
                if growth_rate > 0.5:  # 50%+ cumulative growth
                    score += 2
                    details.append(
                        f"Excellent revenue growth: {growth_rate:.1%} cumulative growth demonstrates market expansion"
                    )
                elif growth_rate > 0:
                    score += 1
                    details.append(
                        f"Positive revenue growth: {growth_rate:.1%} shows business stability"
                    )
                else:
                    details.append(
                        f"Revenue declined {growth_rate:.1%} - concerning for Ackman's growth criteria"
                    )
            else:
                details.append("Revenue growth analysis limited by data quality")
        else:
            details.append(
                "Insufficient revenue history for multi-period growth analysis"
            )

        # 2. Operating Margin Consistency (indicates pricing power/moat)
        if operating_margins:
            high_margin_periods = sum(
                1 for margin in operating_margins if margin and margin > 0.15
            )
            margin_consistency = high_margin_periods / len(operating_margins)

            if margin_consistency >= 0.5:  # Majority of periods above 15%
                score += 2
                details.append(
                    f"Strong operating margins: {high_margin_periods}/{len(operating_margins)} periods >15% indicates pricing power"
                )
            else:
                avg_margin = (
                    sum(m for m in operating_margins if m)
                    / len([m for m in operating_margins if m])
                    if operating_margins
                    else 0
                )
                details.append(
                    f"Operating margins inconsistent: avg {avg_margin:.1%}, only {high_margin_periods}/{len(operating_margins)} periods >15%"
                )
        else:
            details.append("No operating margin data for pricing power assessment")

        # 3. Free Cash Flow Consistency (Ackman prioritizes cash generation)
        if fcf_history:
            positive_fcf_periods = sum(1 for fcf in fcf_history if fcf and fcf > 0)
            fcf_consistency = positive_fcf_periods / len(fcf_history)

            if fcf_consistency >= 0.5:  # Majority positive
                score += 1
                details.append(
                    f"Consistent cash generation: {positive_fcf_periods}/{len(fcf_history)} periods positive FCF"
                )
            else:
                details.append(
                    f"Inconsistent cash generation: only {positive_fcf_periods}/{len(fcf_history)} periods positive FCF"
                )
        else:
            details.append("No free cash flow data for cash generation assessment")

        # 4. Return on Equity (indicates competitive advantage and efficient capital use)
        if return_on_equity and return_on_equity > 0.15:
            score += 2
            details.append(
                f"Exceptional ROE of {return_on_equity:.1%} indicates strong competitive advantage and capital efficiency"
            )
        elif return_on_equity and return_on_equity > 0.10:
            score += 1
            details.append(
                f"Good ROE of {return_on_equity:.1%} shows decent capital efficiency"
            )
        elif return_on_equity:
            details.append(
                f"Moderate ROE of {return_on_equity:.1%} - below Ackman's high-quality standards"
            )
        else:
            details.append("No ROE data available for competitive advantage assessment")

    except Exception as e:
        logger.warning(f"Error in business quality analysis: {e}")
        details.append(f"Analysis error: {str(e)}")

    return {
        "score": score,
        "max_score": max_score,
        "details": "; ".join(details),
        "revenue_growth": growth_rate if "growth_rate" in locals() else None,
        "margin_consistency": (
            margin_consistency if "margin_consistency" in locals() else None
        ),
        "fcf_consistency": fcf_consistency if "fcf_consistency" in locals() else None,
    }


def analyze_financial_discipline(
    financial_data: Annotated[
        Dict[str, Any],
        "Dictionary containing balance sheet data including debt_to_equity, total_liabilities, total_assets, dividends, outstanding_shares",
    ],
) -> Dict[str, Any]:
    """
    Analyze financial discipline following Ackman's emphasis on strong balance sheets and efficient capital allocation.

    Ackman prefers companies with:
    - Conservative leverage (reasonable debt levels)
    - Active capital returns (dividends, buybacks)
    - Disciplined capital allocation

    Scoring criteria:
    - +2 points: Debt-to-equity <1.0 consistently (conservative leverage)
    - +1 point: Capital returns via dividends (shareholder-friendly)
    - +1 point: Share count reduction (buyback discipline)

    Args:
        financial_data: Dictionary containing debt ratios, dividend history, share counts

    Returns:
        Dict with financial discipline score and analysis
    """
    score = 0
    details = []
    max_score = 4

    try:
        debt_to_equity_history = financial_data.get("debt_to_equity_history", [])
        total_liabilities_history = financial_data.get("total_liabilities_history", [])
        total_assets_history = financial_data.get("total_assets_history", [])
        dividend_history = financial_data.get("dividend_history", [])
        shares_outstanding_history = financial_data.get(
            "shares_outstanding_history", []
        )

        # 1. Leverage Analysis (Ackman prefers conservative debt levels)
        leverage_ratios = []
        if debt_to_equity_history:
            leverage_ratios = [de for de in debt_to_equity_history if de is not None]
        elif total_liabilities_history and total_assets_history:
            # Calculate debt ratios from liabilities/assets
            for i in range(
                min(len(total_liabilities_history), len(total_assets_history))
            ):
                if (
                    total_liabilities_history[i]
                    and total_assets_history[i]
                    and total_assets_history[i] > 0
                ):
                    ratio = total_liabilities_history[i] / total_assets_history[i]
                    leverage_ratios.append(ratio)

        if leverage_ratios:
            # Use different thresholds based on data type
            threshold = 1.0 if debt_to_equity_history else 0.5
            conservative_periods = sum(
                1 for ratio in leverage_ratios if ratio < threshold
            )
            if (
                conservative_periods >= len(leverage_ratios) // 2 + 1
            ):  # Majority of periods
                score += 2
                details.append(
                    f"Conservative leverage: {conservative_periods}/{len(leverage_ratios)} periods with reasonable debt levels"
                )
            else:
                details.append(
                    f"High leverage concern: only {conservative_periods}/{len(leverage_ratios)} periods with conservative debt"
                )
        else:
            details.append("No leverage data available for balance sheet assessment")

        # 2. Dividend Policy Analysis (Ackman values capital returns)
        if dividend_history:
            dividend_paying_periods = sum(
                1 for div in dividend_history if div and div < 0
            )  # Negative = cash outflow
            if (
                dividend_paying_periods >= len(dividend_history) // 2
            ):  # Majority pay dividends
                score += 1
                details.append(
                    f"Consistent capital returns: {dividend_paying_periods}/{len(dividend_history)} periods paid dividends"
                )
            else:
                details.append(
                    f"Inconsistent dividends: only {dividend_paying_periods}/{len(dividend_history)} periods paid"
                )
        else:
            details.append("No dividend data for capital allocation assessment")

        # 3. Share Buyback Analysis (indicates disciplined capital allocation)
        if len(shares_outstanding_history) >= 2:
            latest_shares = shares_outstanding_history[0]  # Newest
            earliest_shares = shares_outstanding_history[-1]  # Oldest

            if latest_shares and earliest_shares and latest_shares < earliest_shares:
                reduction_pct = (earliest_shares - latest_shares) / earliest_shares
                score += 1
                details.append(
                    f"Share count reduction: {reduction_pct:.1%} indicates disciplined buybacks"
                )
            else:
                details.append("No significant share count reduction observed")
        else:
            details.append("Insufficient share count data for buyback analysis")

    except Exception as e:
        logger.warning(f"Error in financial discipline analysis: {e}")
        details.append(f"Analysis error: {str(e)}")

    return {
        "score": score,
        "max_score": max_score,
        "details": "; ".join(details),
        "leverage_periods": (
            len(leverage_ratios) if "leverage_ratios" in locals() else 0
        ),
        "dividend_periods": len(dividend_history) if dividend_history else 0,
    }


def analyze_activism_potential(
    financial_data: Annotated[
        Dict[str, Any],
        "Dictionary containing revenue and margin data to assess operational improvement opportunities",
    ],
) -> Dict[str, Any]:
    """
    Analyze activism potential following Ackman's approach to operational improvements.

    Ackman often targets companies with strong brands/market position but suboptimal operations.
    He looks for situations where activist engagement can unlock value through:
    - Margin expansion opportunities
    - Cost structure improvements
    - Strategic repositioning

    Scoring criteria:
    - +2 points: Revenue growth >15% but margins <10% (operational leverage opportunity)
    - +1 point: Declining margins despite revenue growth (efficiency opportunity)

    Args:
        financial_data: Dictionary containing revenue and operating margin histories

    Returns:
        Dict with activism potential score and opportunities identified
    """
    score = 0
    details = []
    max_score = 3

    try:
        revenue_history = financial_data.get("revenue_history", [])
        operating_margin_history = financial_data.get("operating_margin_history", [])

        if len(revenue_history) < 2 or not operating_margin_history:
            return {
                "score": 0,
                "max_score": max_score,
                "details": "Insufficient data for activism potential assessment",
                "revenue_growth": None,
                "avg_margin": None,
            }

        # Calculate revenue growth
        initial_revenue = revenue_history[-1]  # Oldest
        final_revenue = revenue_history[0]  # Newest
        revenue_growth = (
            (final_revenue - initial_revenue) / abs(initial_revenue)
            if initial_revenue
            else 0
        )

        # Calculate average operating margin
        valid_margins = [m for m in operating_margin_history if m is not None]
        avg_margin = sum(valid_margins) / len(valid_margins) if valid_margins else 0

        # Identify activism opportunities
        if revenue_growth > 0.15 and avg_margin < 0.10:  # Strong growth, weak margins
            score += 2
            details.append(
                f"Strong activism opportunity: {revenue_growth:.1%} revenue growth but only {avg_margin:.1%} avg margins - significant operational leverage potential"
            )
        elif revenue_growth > 0.05 and avg_margin < 0.08:  # Moderate opportunity
            score += 1
            details.append(
                f"Moderate activism potential: {revenue_growth:.1%} growth with {avg_margin:.1%} margins suggests efficiency improvements possible"
            )
        else:
            details.append(
                f"Limited activism upside: {revenue_growth:.1%} growth and {avg_margin:.1%} margins - operations may already be optimized"
            )

        # Check for margin deterioration (another activism signal)
        if len(valid_margins) >= 3:
            recent_margin = valid_margins[0]  # Most recent
            earlier_margin = valid_margins[-1]  # Earliest

            if recent_margin < earlier_margin * 0.8:  # 20%+ margin decline
                score += 1
                details.append(
                    f"Margin deterioration detected: {recent_margin:.1%} vs {earlier_margin:.1%} - operational turnaround opportunity"
                )

    except Exception as e:
        logger.warning(f"Error in activism potential analysis: {e}")
        details.append(f"Analysis error: {str(e)}")

    return {
        "score": score,
        "max_score": max_score,
        "details": "; ".join(details),
        "revenue_growth": revenue_growth if "revenue_growth" in locals() else None,
        "avg_margin": avg_margin if "avg_margin" in locals() else None,
    }


def analyze_ackman_valuation(
    financial_data: Annotated[
        Dict[str, Any], "Dictionary containing free cash flow data for DCF analysis"
    ],
    market_cap: Annotated[
        float, "Current market capitalization for valuation comparison"
    ],
) -> Dict[str, Any]:
    """
    Perform Ackman-style valuation analysis using simplified DCF methodology.

    Ackman focuses on intrinsic value with margin of safety, using conservative assumptions:
    - Free cash flow based DCF
    - Moderate growth assumptions (6%)
    - Appropriate discount rate (10%)
    - Terminal value multiple approach

    Scoring criteria:
    - +3 points: >30% margin of safety (strong undervaluation)
    - +1 point: >10% margin of safety (moderate undervaluation)

    Args:
        financial_data: Dictionary containing latest free_cash_flow
        market_cap: Current market capitalization

    Returns:
        Dict with valuation score and DCF analysis results
    """
    score = 0
    details = []
    max_score = 3

    try:
        latest_fcf = financial_data.get("free_cash_flow", 0)

        if not latest_fcf or latest_fcf <= 0:
            return {
                "score": 0,
                "max_score": max_score,
                "details": f"No positive free cash flow for valuation: FCF = {latest_fcf}",
                "intrinsic_value": None,
                "margin_of_safety": None,
            }

        if not market_cap or market_cap <= 0:
            return {
                "score": 0,
                "max_score": max_score,
                "details": "Invalid market cap for valuation comparison",
                "intrinsic_value": None,
                "margin_of_safety": None,
            }

        # Ackman-style DCF assumptions (conservative)
        growth_rate = 0.06  # 6% long-term growth
        discount_rate = 0.10  # 10% discount rate
        terminal_multiple = 15  # 15x terminal FCF multiple
        projection_years = 5  # 5-year explicit forecast

        # Calculate present value of projected FCF
        present_value = 0
        for year in range(1, projection_years + 1):
            future_fcf = latest_fcf * (1 + growth_rate) ** year
            pv = future_fcf / ((1 + discount_rate) ** year)
            present_value += pv

        # Terminal value calculation
        terminal_fcf = latest_fcf * (1 + growth_rate) ** projection_years
        terminal_value = (terminal_fcf * terminal_multiple) / (
            (1 + discount_rate) ** projection_years
        )

        # Total intrinsic value
        intrinsic_value = present_value + terminal_value

        # Margin of safety calculation
        margin_of_safety = (
            (intrinsic_value - market_cap) / market_cap if market_cap > 0 else 0
        )

        # Score based on margin of safety
        if margin_of_safety > 0.3:  # 30%+ undervaluation
            score += 3
            details.append(
                f"Excellent value: {margin_of_safety:.1%} margin of safety - significant undervaluation"
            )
        elif margin_of_safety > 0.1:  # 10%+ undervaluation
            score += 1
            details.append(
                f"Moderate value: {margin_of_safety:.1%} margin of safety - some undervaluation"
            )
        else:
            details.append(
                f"Limited value: {margin_of_safety:.1%} margin of safety - fairly valued or overvalued"
            )

        details.append(
            f"DCF intrinsic value: ${intrinsic_value:,.0f} vs market cap: ${market_cap:,.0f}"
        )
        details.append(
            f"Assumptions: {growth_rate:.1%} growth, {discount_rate:.1%} discount rate, {terminal_multiple}x terminal multiple"
        )

    except Exception as e:
        logger.warning(f"Error in Ackman valuation analysis: {e}")
        details.append(f"Valuation analysis error: {str(e)}")
        intrinsic_value = None
        margin_of_safety = None

    return {
        "score": score,
        "max_score": max_score,
        "details": "; ".join(details),
        "intrinsic_value": intrinsic_value,
        "margin_of_safety": margin_of_safety,
        "dcf_assumptions": {
            "growth_rate": growth_rate if "growth_rate" in locals() else None,
            "discount_rate": discount_rate if "discount_rate" in locals() else None,
            "terminal_multiple": (
                terminal_multiple if "terminal_multiple" in locals() else None
            ),
        },
    }


def calculate_ackman_score(
    quality_analysis: Annotated[
        Dict[str, Any], "Results from business quality analysis"
    ],
    discipline_analysis: Annotated[
        Dict[str, Any], "Results from financial discipline analysis"
    ],
    activism_analysis: Annotated[
        Dict[str, Any], "Results from activism potential analysis"
    ],
    valuation_analysis: Annotated[
        Dict[str, Any], "Results from Ackman valuation analysis"
    ],
) -> Dict[str, Any]:
    """
    Calculate overall Ackman investment score and generate signal.

    Ackman signal criteria:
    - Bullish: Total score >= 70% of maximum (strong business quality + attractive valuation)
    - Bearish: Total score <= 30% of maximum (poor quality or overvalued)
    - Neutral: Score between 30-70% (mixed signals or moderate opportunity)

    Args:
        quality_analysis: Business quality assessment results
        discipline_analysis: Financial discipline assessment results
        activism_analysis: Activism potential assessment results
        valuation_analysis: Valuation analysis results

    Returns:
        Dict with overall score, signal, and detailed breakdown
    """
    try:
        quality_score = quality_analysis.get("score", 0)
        discipline_score = discipline_analysis.get("score", 0)
        activism_score = activism_analysis.get("score", 0)
        valuation_score = valuation_analysis.get("score", 0)

        quality_max = quality_analysis.get("max_score", 7)
        discipline_max = discipline_analysis.get("max_score", 4)
        activism_max = activism_analysis.get("max_score", 3)
        valuation_max = valuation_analysis.get("max_score", 3)

        total_score = (
            quality_score + discipline_score + activism_score + valuation_score
        )
        max_possible_score = quality_max + discipline_max + activism_max + valuation_max
        score_percentage = (
            (total_score / max_possible_score) if max_possible_score > 0 else 0
        )

        # Determine Ackman signal
        if score_percentage >= 0.7:
            signal = "bullish"
            signal_strength = "Strong Ackman characteristics - high-quality business with attractive valuation"
        elif score_percentage <= 0.3:
            signal = "bearish"
            signal_strength = (
                "Fails Ackman criteria - weak business quality or poor valuation"
            )
        else:
            signal = "neutral"
            signal_strength = (
                "Mixed Ackman signals - some positive attributes but not compelling"
            )

        breakdown = {
            "business_quality": f"{quality_score}/{quality_max}",
            "financial_discipline": f"{discipline_score}/{discipline_max}",
            "activism_potential": f"{activism_score}/{activism_max}",
            "valuation": f"{valuation_score}/{valuation_max}",
        }

    except Exception as e:
        logger.warning(f"Error calculating Ackman score: {e}")
        return {
            "total_score": 0,
            "max_possible_score": 17,
            "score_percentage": 0,
            "signal": "neutral",
            "signal_strength": f"Scoring error: {str(e)}",
            "breakdown": {},
        }

    return {
        "total_score": total_score,
        "max_possible_score": max_possible_score,
        "score_percentage": score_percentage,
        "signal": signal,
        "signal_strength": signal_strength,
        "breakdown": breakdown,
    }
