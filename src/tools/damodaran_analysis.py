"""
Financial analysis tools for Aswath Damodaran-style investment analysis.
Implements his core valuation methodologies as Google ADK tools.
"""

from typing import Dict, List, Optional, Any
import json
from loguru import logger


def analyze_growth_and_reinvestment(
    financial_data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Analyze growth patterns and reinvestment efficiency following Damodaran's framework.

    Growth score (0-4 points):
    - +2 for 5-year revenue CAGR > 8%
    - +1 for 5-year revenue CAGR > 3%
    - +1 for positive FCFF growth over 5 years
    - +1 for ROIC > 10% (reinvestment efficiency hurdle)

    Args:
        financial_data: Dictionary containing historical financial metrics including
                       revenue_history, fcff_history, and return_on_invested_capital

    Returns:
        Dict with score, max_score, details, and key metrics
    """
    max_score = 4
    score = 0
    details = []

    try:
        # Extract revenue data for CAGR calculation
        revenue_history = financial_data.get("revenue_history", [])
        if (
            len(revenue_history) >= 5
            and revenue_history[0] > 0
            and revenue_history[-1] > 0
        ):
            revenue_cagr = (revenue_history[-1] / revenue_history[0]) ** (
                1 / (len(revenue_history) - 1)
            ) - 1

            if revenue_cagr > 0.08:
                score += 2
                details.append(f"Strong revenue CAGR {revenue_cagr:.1%} (>8%)")
            elif revenue_cagr > 0.03:
                score += 1
                details.append(f"Moderate revenue CAGR {revenue_cagr:.1%} (>3%)")
            else:
                details.append(f"Weak revenue CAGR {revenue_cagr:.1%}")
        else:
            details.append("Insufficient revenue history for CAGR analysis")

        # Analyze FCFF growth trend
        fcff_history = financial_data.get("fcff_history", [])
        if len(fcff_history) >= 5:
            if fcff_history[-1] > fcff_history[0]:
                score += 1
                fcff_growth = (
                    (fcff_history[-1] / fcff_history[0])
                    ** (1 / (len(fcff_history) - 1))
                    - 1
                    if fcff_history[0] > 0
                    else 0
                )
                details.append(f"Positive FCFF growth {fcff_growth:.1%}")
            else:
                details.append("Declining or flat FCFF trend")
        else:
            details.append("Insufficient FCFF history")

        # Check reinvestment efficiency (ROIC)
        roic = financial_data.get("return_on_invested_capital")
        if roic is not None and roic > 0.10:
            score += 1
            details.append(f"Efficient reinvestment: ROIC {roic:.1%} > 10%")
        elif roic is not None:
            details.append(f"Poor reinvestment efficiency: ROIC {roic:.1%}")
        else:
            details.append("ROIC data unavailable")

    except Exception as e:
        logger.warning(f"Error in growth analysis: {e}")
        details.append(f"Analysis error: {str(e)}")

    return {
        "score": score,
        "max_score": max_score,
        "details": "; ".join(details),
        "revenue_cagr": revenue_history,
        "fcff_trend": fcff_history,
        "roic": financial_data.get("return_on_invested_capital"),
    }


def analyze_risk_profile(
    financial_data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Assess financial and business risk following Damodaran's risk framework.

    Risk score (0-3 points):
    - +1 for Beta < 1.3 (lower systematic risk)
    - +1 for Debt/Equity < 1.0 (conservative leverage)

    Args:
        financial_data: Dictionary containing risk-related financial metrics including
                       beta, debt_to_equity, ebit, and interest_expense
    - +1 for Interest Coverage > 3x (adequate debt service ability)

    Args:
        financial_data: Dictionary containing risk-related financial metrics

    Returns:
        Dict with risk score, cost of equity estimate, and risk details
    """
    max_score = 3
    score = 0
    details = []
    interest_coverage = None

    try:
        # Beta analysis (systematic risk)
        beta = financial_data.get("beta")
        if beta is not None:
            if beta < 1.3:
                score += 1
                details.append(f"Moderate systematic risk: Beta {beta:.2f}")
            else:
                details.append(f"High systematic risk: Beta {beta:.2f}")
        else:
            details.append("Beta unavailable")
            beta = 1.0  # Market beta as default

        # Leverage analysis
        debt_to_equity = financial_data.get("debt_to_equity")
        if debt_to_equity is not None:
            if debt_to_equity < 1.0:
                score += 1
                details.append(f"Conservative leverage: D/E {debt_to_equity:.2f}")
            else:
                details.append(f"High leverage: D/E {debt_to_equity:.2f}")
        else:
            details.append("Debt/Equity ratio unavailable")

        # Interest coverage (debt service ability)
        ebit = financial_data.get("ebit")
        interest_expense = financial_data.get("interest_expense")

        if ebit and interest_expense and interest_expense != 0:
            interest_coverage = abs(ebit / interest_expense)
            if interest_coverage > 3.0:
                score += 1
                details.append(f"Strong debt coverage: {interest_coverage:.1f}x")
            else:
                details.append(f"Weak debt coverage: {interest_coverage:.1f}x")
        else:
            details.append("Interest coverage unavailable")

        # Calculate cost of equity using CAPM
        cost_of_equity = estimate_cost_of_equity(beta)

    except Exception as e:
        logger.warning(f"Error in risk analysis: {e}")
        details.append(f"Risk analysis error: {str(e)}")
        cost_of_equity = 0.09  # Default cost of equity

    return {
        "score": score,
        "max_score": max_score,
        "details": "; ".join(details),
        "beta": beta,
        "debt_to_equity": debt_to_equity,
        "cost_of_equity": cost_of_equity,
        "interest_coverage": interest_coverage,
    }


def analyze_relative_valuation(
    financial_data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Perform relative valuation analysis using P/E ratios vs historical medians.

    Simple PE check vs. historical median:
    - +1 if current P/E < 70% of 5-year median (undervalued)
    - 0 if between 70%-130% of median (fairly valued)
    - -1 if > 130% of median (overvalued)

    Args:
        financial_data: Dictionary containing valuation metrics including
                       pe_history and current_pe

    Args:
        financial_data: Dictionary containing valuation metrics

    Returns:
        Dict with relative valuation score and analysis
    """
    max_score = 1

    try:
        pe_history = financial_data.get("pe_history", [])
        current_pe = financial_data.get("current_pe")

        if not pe_history or len(pe_history) < 5 or current_pe is None:
            return {
                "score": 0,
                "max_score": max_score,
                "details": "Insufficient P/E data for relative analysis",
                "current_pe": current_pe,
                "historical_median": None,
            }

        # Calculate 5-year median P/E
        valid_pes = [pe for pe in pe_history if pe > 0]  # Filter out negative P/Es
        if len(valid_pes) < 3:
            return {
                "score": 0,
                "max_score": max_score,
                "details": "Insufficient valid P/E history",
                "current_pe": current_pe,
                "historical_median": None,
            }

        historical_median = sorted(valid_pes)[len(valid_pes) // 2]

        # Compare current P/E to historical median
        if current_pe < 0.7 * historical_median:
            score = 1
            valuation_desc = (
                f"Undervalued: P/E {current_pe:.1f} vs median {historical_median:.1f}"
            )
        elif current_pe > 1.3 * historical_median:
            score = -1
            valuation_desc = (
                f"Overvalued: P/E {current_pe:.1f} vs median {historical_median:.1f}"
            )
        else:
            score = 0
            valuation_desc = (
                f"Fair value: P/E {current_pe:.1f} vs median {historical_median:.1f}"
            )

    except Exception as e:
        logger.warning(f"Error in relative valuation: {e}")
        return {
            "score": 0,
            "max_score": max_score,
            "details": f"Relative valuation error: {str(e)}",
            "current_pe": None,
            "historical_median": None,
        }

    return {
        "score": score,
        "max_score": max_score,
        "details": valuation_desc,
        "current_pe": current_pe,
        "historical_median": historical_median,
    }


def calculate_intrinsic_value_dcf(
    financial_data: Dict[str, Any],
    risk_analysis: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Calculate intrinsic value using FCFF DCF model (Damodaran methodology).

    DCF Approach:
    - Base FCFF from most recent period
    - Growth rate derived from historical revenue CAGR (capped at 12%)
    - Linear fade to terminal growth of 2.5% over 10 years
    - Discount at cost of equity from risk analysis

    Args:
        financial_data: Dictionary with cash flow and share data including
                       free_cash_flow, shares_outstanding, revenue_history
        risk_analysis: Dictionary with cost of equity estimate from risk analysis
        financial_data: Dictionary with cash flow and share data
        risk_analysis: Dictionary with cost of equity estimate

    Returns:
        Dict with intrinsic value estimate and key assumptions
    """
    try:
        # Extract base data
        current_fcff = financial_data.get("free_cash_flow")
        shares_outstanding = financial_data.get("shares_outstanding")
        revenue_history = financial_data.get("revenue_history", [])

        if not current_fcff or not shares_outstanding:
            return {
                "intrinsic_value": None,
                "intrinsic_per_share": None,
                "details": ["Missing FCFF or share count data"],
                "assumptions": {},
            }

        # Estimate growth rate from revenue CAGR (capped at 12%)
        if (
            len(revenue_history) >= 5
            and revenue_history[0] > 0
            and revenue_history[-1] > 0
        ):
            revenue_cagr = (revenue_history[-1] / revenue_history[0]) ** (
                1 / (len(revenue_history) - 1)
            ) - 1
            base_growth = min(revenue_cagr, 0.12)  # Cap at 12%
        else:
            base_growth = 0.04  # Conservative default

        # DCF parameters
        terminal_growth = 0.025  # 2.5% terminal growth
        projection_years = 10
        discount_rate = risk_analysis.get("cost_of_equity", 0.09)

        # Project and discount FCFFs
        pv_sum = 0.0
        growth_rate = base_growth
        growth_decline = (base_growth - terminal_growth) / (projection_years - 1)

        for year in range(1, projection_years + 1):
            projected_fcff = current_fcff * (1 + growth_rate)
            present_value = projected_fcff / (1 + discount_rate) ** year
            pv_sum += present_value
            growth_rate -= growth_decline  # Linear fade to terminal

        # Terminal value calculation
        terminal_fcff = current_fcff * (1 + terminal_growth)
        terminal_value = terminal_fcff / (discount_rate - terminal_growth)
        terminal_pv = terminal_value / (1 + discount_rate) ** projection_years

        # Total firm value and per-share value
        firm_value = pv_sum + terminal_pv
        intrinsic_per_share = firm_value / shares_outstanding

        assumptions = {
            "base_fcff": current_fcff,
            "base_growth_rate": base_growth,
            "terminal_growth_rate": terminal_growth,
            "discount_rate": discount_rate,
            "projection_years": projection_years,
            "shares_outstanding": shares_outstanding,
        }

    except Exception as e:
        logger.warning(f"Error in DCF calculation: {e}")
        return {
            "intrinsic_value": None,
            "intrinsic_per_share": None,
            "details": [f"DCF calculation error: {str(e)}"],
            "assumptions": {},
        }

    return {
        "intrinsic_value": firm_value,
        "intrinsic_per_share": intrinsic_per_share,
        "details": ["DCF valuation completed"],
        "assumptions": assumptions,
        "terminal_value": terminal_pv,
        "pv_projections": pv_sum,
    }


def calculate_margin_of_safety(
    intrinsic_value: float,
    market_value: float,
) -> Optional[float]:
    """
    Calculate margin of safety as percentage difference between intrinsic and market value.

    Args:
        intrinsic_value: DCF-derived intrinsic value
        market_value: Current market capitalization or price

    Returns:
        Margin of safety as decimal (e.g., 0.25 for 25% undervalued)
    """
    if not intrinsic_value or not market_value or market_value <= 0:
        return None

    return (intrinsic_value - market_value) / market_value


def estimate_cost_of_equity(beta: Optional[float] = None) -> float:
    """
    Estimate cost of equity using CAPM with Damodaran's long-term market parameters.

    CAPM: Cost of Equity = Risk-free Rate + Beta × Equity Risk Premium

    Args:
        beta: Stock's systematic risk measure (defaults to 1.0 if None)

    Returns:
        Estimated cost of equity as decimal (e.g., 0.09 for 9%)
    """
    # Use Damodaran's long-term US market estimates
    risk_free_rate = 0.04  # 10-year US Treasury approximation
    equity_risk_premium = 0.05  # Long-run US equity risk premium

    beta = beta if beta is not None else 1.0

    return risk_free_rate + beta * equity_risk_premium
