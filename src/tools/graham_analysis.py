"""
Ben Graham-style financial analysis tools.
Implements his classic value investing methodologies as Google ADK tools.
"""

from typing import Dict, List, Optional, Any
import json
import math
from loguru import logger


def analyze_earnings_stability(financial_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze earnings stability following Benjamin Graham's criteria.

    Graham requires at least several years of consistently positive earnings (ideally 5+).
    Scoring criteria:
    - +3 points: EPS positive in all available periods
    - +2 points: EPS positive in most periods (80%+)
    - +1 point: EPS growth from earliest to latest period

    Args:
        financial_data: Dictionary containing earnings_per_share history

    Returns:
        Dict with stability score, max_score, and detailed analysis
    """
    score = 0
    details = []
    max_score = 4

    try:
        eps_history = financial_data.get("eps_history", [])

        if len(eps_history) < 2:
            return {
                "score": score,
                "max_score": max_score,
                "details": "Insufficient multi-year EPS data for stability analysis",
                "positive_eps_years": 0,
                "total_years": len(eps_history),
                "eps_growth": None,
            }

        # Count positive EPS years
        positive_eps_years = sum(1 for eps in eps_history if eps > 0)
        total_eps_years = len(eps_history)
        positive_ratio = positive_eps_years / total_eps_years

        # Score for consistency of positive earnings
        if positive_eps_years == total_eps_years:
            score += 3
            details.append(f"Excellent: EPS positive in all {total_eps_years} periods")
        elif positive_ratio >= 0.8:
            score += 2
            details.append(
                f"Good: EPS positive in {positive_eps_years}/{total_eps_years} periods ({positive_ratio:.1%})"
            )
        else:
            details.append(
                f"Weak: EPS positive in only {positive_eps_years}/{total_eps_years} periods ({positive_ratio:.1%})"
            )

        # Check for EPS growth from earliest to latest
        eps_growth = None
        if eps_history[0] > 0 and eps_history[-1] > 0:
            eps_growth = (eps_history[-1] / eps_history[0]) - 1
            if eps_growth > 0:
                score += 1
                details.append(
                    f"EPS grew {eps_growth:.1%} from earliest to latest period"
                )
            else:
                details.append(
                    f"EPS declined {eps_growth:.1%} from earliest to latest period"
                )
        else:
            details.append("Cannot calculate EPS growth (negative values present)")

    except Exception as e:
        logger.warning(f"Error in earnings stability analysis: {e}")
        details.append(f"Analysis error: {str(e)}")

    return {
        "score": score,
        "max_score": max_score,
        "details": "; ".join(details),
        "positive_eps_years": (
            positive_eps_years if "positive_eps_years" in locals() else 0
        ),
        "total_years": len(eps_history),
        "eps_growth": eps_growth if "eps_growth" in locals() else None,
        "eps_history": eps_history,
    }


def analyze_financial_strength(financial_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze financial strength using Graham's conservative criteria.

    Graham's requirements:
    - +2 points: Current ratio >= 2.0 (excellent liquidity)
    - +1 point: Current ratio >= 1.5 (adequate liquidity)
    - +2 points: Debt ratio < 50% (conservative leverage)
    - +1 point: Debt ratio < 80% (acceptable leverage)
    - +1 point: Consistent dividend payments (financial stability)

    Args:
        financial_data: Dictionary containing balance sheet and dividend data

    Returns:
        Dict with financial strength score and detailed metrics
    """
    score = 0
    details = []
    max_score = 5

    try:
        current_assets = financial_data.get("current_assets", 0)
        current_liabilities = financial_data.get("current_liabilities", 0)
        total_assets = financial_data.get("total_assets", 0)
        total_liabilities = financial_data.get("total_liabilities", 0)
        dividend_history = financial_data.get("dividend_history", [])

        # Current Ratio Analysis
        current_ratio = None
        if current_liabilities > 0:
            current_ratio = current_assets / current_liabilities
            if current_ratio >= 2.0:
                score += 2
                details.append(
                    f"Excellent liquidity: Current ratio {current_ratio:.2f} >= 2.0"
                )
            elif current_ratio >= 1.5:
                score += 1
                details.append(
                    f"Adequate liquidity: Current ratio {current_ratio:.2f} >= 1.5"
                )
            else:
                details.append(
                    f"Weak liquidity: Current ratio {current_ratio:.2f} < 1.5"
                )
        else:
            details.append(
                "Cannot calculate current ratio (missing current liabilities)"
            )

        # Debt Ratio Analysis
        debt_ratio = None
        if total_assets > 0:
            debt_ratio = total_liabilities / total_assets
            if debt_ratio < 0.5:
                score += 2
                details.append(f"Conservative debt: Debt ratio {debt_ratio:.2f} < 50%")
            elif debt_ratio < 0.8:
                score += 1
                details.append(f"Acceptable debt: Debt ratio {debt_ratio:.2f} < 80%")
            else:
                details.append(f"High debt: Debt ratio {debt_ratio:.2f} >= 80%")
        else:
            details.append("Cannot calculate debt ratio (missing total assets)")

        # Dividend Consistency Analysis
        dividend_paying_years = 0
        if dividend_history:
            # Dividends often reported as negative (cash outflow to shareholders)
            dividend_paying_years = sum(1 for div in dividend_history if div < 0)
            dividend_consistency = dividend_paying_years / len(dividend_history)

            if dividend_consistency >= 0.5:  # Majority of years paid dividends
                score += 1
                details.append(
                    f"Dividend consistency: Paid dividends in {dividend_paying_years}/{len(dividend_history)} years"
                )
            else:
                details.append(
                    f"Inconsistent dividends: Only {dividend_paying_years}/{len(dividend_history)} years"
                )
        else:
            details.append("No dividend data available")

    except Exception as e:
        logger.warning(f"Error in financial strength analysis: {e}")
        details.append(f"Analysis error: {str(e)}")

    return {
        "score": score,
        "max_score": max_score,
        "details": "; ".join(details),
        "current_ratio": current_ratio,
        "debt_ratio": debt_ratio,
        "dividend_paying_years": (
            dividend_paying_years if "dividend_paying_years" in locals() else 0
        ),
        "dividend_total_years": len(dividend_history) if dividend_history else 0,
    }


def analyze_valuation_graham(
    financial_data: Dict[str, Any], market_cap: float
) -> Dict[str, Any]:
    """
    Perform Graham's classic valuation analysis using Net-Net and Graham Number methods.

    Graham valuation criteria:
    - +4 points: Net Current Asset Value > Market Cap (classic net-net)
    - +2 points: NCAV per share >= 2/3 of price (moderate net-net discount)
    - +3 points: Price well below Graham Number (>=50% margin of safety)
    - +1 point: Some margin of safety vs Graham Number (>=20%)

    Args:
        financial_data: Dictionary with balance sheet and per-share metrics
        market_cap: Current market capitalization

    Returns:
        Dict with valuation score and Graham-specific metrics
    """
    score = 0
    details = []
    max_score = 7

    try:
        current_assets = financial_data.get("current_assets", 0)
        total_liabilities = financial_data.get("total_liabilities", 0)
        book_value_per_share = financial_data.get("book_value_per_share", 0)
        earnings_per_share = financial_data.get("earnings_per_share", 0)
        shares_outstanding = financial_data.get("shares_outstanding", 0)

        if (
            not market_cap
            or market_cap <= 0
            or not shares_outstanding
            or shares_outstanding <= 0
        ):
            return {
                "score": 0,
                "max_score": max_score,
                "details": "Insufficient market cap or shares outstanding data",
                "net_current_asset_value": None,
                "graham_number": None,
                "margin_of_safety": None,
            }

        price_per_share = market_cap / shares_outstanding

        # Net Current Asset Value Analysis (Net-Net)
        net_current_asset_value = current_assets - total_liabilities
        ncav_per_share = (
            net_current_asset_value / shares_outstanding
            if shares_outstanding > 0
            else 0
        )

        details.append(f"Net Current Asset Value: ${net_current_asset_value:,.0f}")
        details.append(f"NCAV per share: ${ncav_per_share:.2f}")
        details.append(f"Current price per share: ${price_per_share:.2f}")

        # Classic Net-Net Analysis
        if net_current_asset_value > market_cap:
            score += 4
            details.append(
                "Exceptional value: NCAV > Market Cap (classic Graham net-net)"
            )
        elif ncav_per_share >= (price_per_share * 0.67):
            score += 2
            details.append("Good value: NCAV per share >= 2/3 of price")
        else:
            details.append("No significant net-net discount available")

        # Graham Number Analysis
        graham_number = None
        margin_of_safety = None

        if earnings_per_share > 0 and book_value_per_share > 0:
            # Graham Number = sqrt(22.5 * EPS * Book Value per Share)
            graham_number = math.sqrt(22.5 * earnings_per_share * book_value_per_share)
            margin_of_safety = (graham_number - price_per_share) / price_per_share

            details.append(f"Graham Number: ${graham_number:.2f}")
            details.append(f"Margin of Safety: {margin_of_safety:.1%}")

            if margin_of_safety >= 0.5:
                score += 3
                details.append("Excellent value: Price >= 50% below Graham Number")
            elif margin_of_safety >= 0.2:
                score += 1
                details.append("Moderate value: Price >= 20% below Graham Number")
            else:
                details.append("Limited value: Price near or above Graham Number")
        else:
            details.append("Cannot calculate Graham Number (EPS or BVPS <= 0)")

    except Exception as e:
        logger.warning(f"Error in Graham valuation analysis: {e}")
        details.append(f"Valuation analysis error: {str(e)}")

    return {
        "score": score,
        "max_score": max_score,
        "details": "; ".join(details),
        "net_current_asset_value": (
            net_current_asset_value if "net_current_asset_value" in locals() else None
        ),
        "ncav_per_share": ncav_per_share if "ncav_per_share" in locals() else None,
        "graham_number": graham_number,
        "margin_of_safety": margin_of_safety,
        "price_per_share": price_per_share if "price_per_share" in locals() else None,
    }


def calculate_graham_score(
    earnings_analysis: Dict[str, Any],
    strength_analysis: Dict[str, Any],
    valuation_analysis: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Calculate overall Graham investment score and generate signal.

    Graham signal criteria:
    - Bullish: Total score >= 70% of maximum possible (strong Graham characteristics)
    - Bearish: Total score <= 30% of maximum possible (fails Graham tests)
    - Neutral: Score between 30-70% (mixed or insufficient Graham characteristics)

    Args:
        earnings_analysis: Earnings stability results
        strength_analysis: Financial strength results
        valuation_analysis: Valuation analysis results

    Returns:
        Dict with overall score, signal, and detailed breakdown
    """
    try:
        earnings_score = earnings_analysis.get("score", 0)
        strength_score = strength_analysis.get("score", 0)
        valuation_score = valuation_analysis.get("score", 0)

        earnings_max = earnings_analysis.get("max_score", 4)
        strength_max = strength_analysis.get("max_score", 5)
        valuation_max = valuation_analysis.get("max_score", 7)

        total_score = earnings_score + strength_score + valuation_score
        max_possible_score = earnings_max + strength_max + valuation_max
        score_percentage = (
            (total_score / max_possible_score) if max_possible_score > 0 else 0
        )

        # Determine Graham signal based on score thresholds
        if score_percentage >= 0.7:
            signal = "bullish"
            signal_strength = (
                "Strong Graham characteristics - meets conservative value criteria"
            )
        elif score_percentage <= 0.3:
            signal = "bearish"
            signal_strength = (
                "Fails Graham tests - insufficient safety margin or quality"
            )
        else:
            signal = "neutral"
            signal_strength = "Mixed Graham signals - some positive but not compelling"

        breakdown = {
            "earnings": f"{earnings_score}/{earnings_max}",
            "financial_strength": f"{strength_score}/{strength_max}",
            "valuation": f"{valuation_score}/{valuation_max}",
        }

    except Exception as e:
        logger.warning(f"Error calculating Graham score: {e}")
        return {
            "total_score": 0,
            "max_possible_score": 16,
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
