"""
Charlie Munger-style investment analysis tools.
Implements his mental models focusing on moat strength, management quality, predictability, and rational valuation.
"""

from typing import Dict, List, Optional, Any, Annotated
import json
from loguru import logger


def analyze_moat_strength(
    financial_data: Annotated[
        Dict[str, Any],
        "Dictionary containing ROIC, margins, capital requirements, and intangible assets data",
    ],
) -> Dict[str, Any]:
    """
    Analyze competitive moat strength using Munger's criteria for durable competitive advantages.

    Munger focuses on businesses with sustainable competitive advantages that protect returns:
    - High and consistent Return on Invested Capital (ROIC >15%)
    - Pricing power evidenced by stable/improving gross margins
    - Low capital requirements (asset-light business models)
    - Intangible assets (R&D, brand value, intellectual property)

    Scoring criteria:
    - +3 points: ROIC >15% in 80%+ of periods (exceptional capital efficiency)
    - +2 points: ROIC >15% in 50%+ of periods (good capital efficiency)
    - +2 points: Stable/improving gross margins (pricing power)
    - +2 points: Low capital intensity <5% of revenue (asset-light model)
    - +1 point each: R&D investment and goodwill/intangible assets (moat sources)

    Args:
        financial_data: Dictionary containing ROIC, gross margins, capex, R&D, goodwill data

    Returns:
        Dict with moat strength score and competitive advantage analysis
    """
    score = 0
    details = []
    max_score = 9

    try:
        roic_history = financial_data.get("roic_history", [])
        gross_margin_history = financial_data.get("gross_margin_history", [])
        revenue_history = financial_data.get("revenue_history", [])
        capex_history = financial_data.get("capex_history", [])
        rd_investment = financial_data.get("research_and_development", 0)
        goodwill_intangibles = financial_data.get("goodwill_and_intangible_assets", 0)

        # 1. Return on Invested Capital Analysis (Munger's favorite metric)
        if roic_history:
            high_roic_periods = sum(1 for roic in roic_history if roic and roic > 0.15)
            roic_consistency = high_roic_periods / len(roic_history)

            if roic_consistency >= 0.8:  # 80%+ periods with high ROIC
                score += 3
                details.append(
                    f"Exceptional ROIC consistency: {high_roic_periods}/{len(roic_history)} periods >15% - strong competitive moat"
                )
            elif roic_consistency >= 0.5:  # 50%+ periods with high ROIC
                score += 2
                details.append(
                    f"Good ROIC performance: {high_roic_periods}/{len(roic_history)} periods >15% - moderate competitive advantage"
                )
            elif high_roic_periods > 0:
                score += 1
                details.append(
                    f"Mixed ROIC results: only {high_roic_periods}/{len(roic_history)} periods >15% - limited moat evidence"
                )
            else:
                details.append(
                    "Poor ROIC performance: never exceeds 15% - no clear competitive advantage"
                )
        else:
            details.append(
                "No ROIC data available for competitive advantage assessment"
            )

        # 2. Pricing Power Analysis (stable/improving gross margins)
        if len(gross_margin_history) >= 3:
            # Calculate margin trend - Munger likes stable or improving margins
            improving_periods = 0
            for i in range(1, len(gross_margin_history)):
                if gross_margin_history[i - 1] and gross_margin_history[i]:
                    if (
                        gross_margin_history[i - 1] >= gross_margin_history[i]
                    ):  # Current >= previous
                        improving_periods += 1

            trend_consistency = improving_periods / (len(gross_margin_history) - 1)
            avg_margin = sum(m for m in gross_margin_history if m) / len(
                [m for m in gross_margin_history if m]
            )

            if trend_consistency >= 0.7:  # Improving in 70%+ of periods
                score += 2
                details.append(
                    f"Strong pricing power: margins stable/improving in {improving_periods}/{len(gross_margin_history)-1} periods"
                )
            elif avg_margin > 0.3:  # High absolute margin level
                score += 1
                details.append(
                    f"Good pricing power: average gross margin of {avg_margin:.1%} indicates differentiation"
                )
            else:
                details.append("Limited pricing power: margins declining or low levels")
        else:
            details.append("Insufficient margin data for pricing power assessment")

        # 3. Capital Intensity Analysis (Munger prefers asset-light businesses)
        if capex_history and revenue_history and len(capex_history) >= 3:
            capex_ratios = []
            for i in range(min(len(capex_history), len(revenue_history))):
                if capex_history[i] and revenue_history[i] and revenue_history[i] > 0:
                    # Capex typically negative, so use absolute value
                    capex_ratio = abs(capex_history[i]) / revenue_history[i]
                    capex_ratios.append(capex_ratio)

            if capex_ratios:
                avg_capex_intensity = sum(capex_ratios) / len(capex_ratios)
                if avg_capex_intensity < 0.05:  # <5% of revenue
                    score += 2
                    details.append(
                        f"Excellent capital efficiency: avg capex {avg_capex_intensity:.1%} of revenue - asset-light model"
                    )
                elif avg_capex_intensity < 0.10:  # <10% of revenue
                    score += 1
                    details.append(
                        f"Good capital efficiency: avg capex {avg_capex_intensity:.1%} of revenue - moderate requirements"
                    )
                else:
                    details.append(
                        f"High capital requirements: avg capex {avg_capex_intensity:.1%} of revenue - capital intensive"
                    )
            else:
                details.append("Cannot calculate capex intensity ratios")
        else:
            details.append("Insufficient capex data for capital intensity analysis")

        # 4. R&D Investment (intellectual property and innovation moat)
        if rd_investment and revenue_history and revenue_history[0]:
            rd_intensity = rd_investment / revenue_history[0]
            if rd_investment > 0:
                score += 1
                details.append(
                    f"R&D investment: {rd_intensity:.1%} of revenue - building intellectual property moat"
                )
            else:
                details.append(
                    "No R&D investment - limited innovation-based competitive advantage"
                )
        else:
            details.append("No R&D data available")

        # 5. Intangible Assets (brand value, acquired IP, goodwill)
        if goodwill_intangibles and goodwill_intangibles > 0:
            score += 1
            details.append(
                "Significant goodwill/intangible assets - indicates brand value or acquired competitive advantages"
            )
        else:
            details.append("Limited intangible assets on balance sheet")

    except Exception as e:
        logger.warning(f"Error in moat strength analysis: {e}")
        details.append(f"Analysis error: {str(e)}")

    return {
        "score": score,
        "max_score": max_score,
        "details": "; ".join(details),
        "roic_consistency": (
            roic_consistency if "roic_consistency" in locals() else None
        ),
        "avg_capex_intensity": (
            avg_capex_intensity if "avg_capex_intensity" in locals() else None
        ),
        "rd_intensity": rd_intensity if "rd_intensity" in locals() else None,
    }


def analyze_management_quality(
    financial_data: Annotated[
        Dict[str, Any],
        "Dictionary containing FCF, net income, debt, equity, cash, shares data",
    ],
    insider_data: Annotated[
        Dict[str, Any],
        "Dictionary containing insider trading activity and ownership data",
    ],
) -> Dict[str, Any]:
    """
    Analyze management quality using Munger's criteria for rational capital allocation and shareholder alignment.

    Munger values management that demonstrates:
    - Honest accounting (FCF conversion from earnings)
    - Conservative financial management (low debt, appropriate cash levels)
    - Shareholder alignment (insider ownership, rational buybacks)
    - Long-term focus (stable share count, reinvestment over excessive dividends)

    Scoring criteria:
    - +3 points: Excellent cash conversion (FCF/NI >1.1)
    - +3 points: Conservative debt management (D/E <0.3)
    - +2 points: Prudent cash management (10-25% of revenue)
    - +2 points: Strong insider buying activity (>70% buys)
    - +2 points: Shareholder-friendly share count reduction

    Args:
        financial_data: Dictionary containing FCF, net income, debt, equity, cash, share data
        insider_data: Dictionary containing insider trading patterns

    Returns:
        Dict with management quality score and capital allocation assessment
    """
    score = 0
    details = []
    max_score = 12

    try:
        fcf_history = financial_data.get("fcf_history", [])
        net_income_history = financial_data.get("net_income_history", [])
        debt_history = financial_data.get("debt_history", [])
        equity_history = financial_data.get("equity_history", [])
        cash_history = financial_data.get("cash_history", [])
        revenue_history = financial_data.get("revenue_history", [])
        shares_history = financial_data.get("shares_history", [])
        insider_buys = insider_data.get("insider_buys", 0)
        insider_sells = insider_data.get("insider_sells", 0)

        # 1. Cash Conversion Analysis (FCF vs Net Income - Munger's accounting quality test)
        if (
            fcf_history
            and net_income_history
            and len(fcf_history) == len(net_income_history)
        ):
            fcf_ni_ratios = []
            for i in range(len(fcf_history)):
                if net_income_history[i] and net_income_history[i] > 0:
                    ratio = fcf_history[i] / net_income_history[i]
                    fcf_ni_ratios.append(ratio)

            if fcf_ni_ratios:
                avg_conversion = sum(fcf_ni_ratios) / len(fcf_ni_ratios)
                if avg_conversion > 1.1:  # FCF exceeds net income
                    score += 3
                    details.append(
                        f"Excellent accounting quality: FCF/NI ratio {avg_conversion:.2f} - conservative accounting practices"
                    )
                elif avg_conversion > 0.9:  # FCF roughly equals net income
                    score += 2
                    details.append(
                        f"Good cash conversion: FCF/NI ratio {avg_conversion:.2f} - reliable earnings quality"
                    )
                elif avg_conversion > 0.7:
                    score += 1
                    details.append(
                        f"Moderate cash conversion: FCF/NI ratio {avg_conversion:.2f} - some accounting concerns"
                    )
                else:
                    details.append(
                        f"Poor cash conversion: FCF/NI ratio {avg_conversion:.2f} - potential accounting quality issues"
                    )
            else:
                details.append(
                    "Cannot calculate FCF/NI ratios - no positive net income periods"
                )
        else:
            details.append(
                "Insufficient FCF or net income data for accounting quality assessment"
            )

        # 2. Debt Management (Munger is very cautious about leverage)
        if (
            debt_history
            and equity_history
            and len(debt_history) > 0
            and len(equity_history) > 0
        ):
            latest_de_ratio = (
                debt_history[0] / equity_history[0]
                if equity_history[0] > 0
                else float("inf")
            )

            if latest_de_ratio < 0.3:  # Very conservative debt levels
                score += 3
                details.append(
                    f"Excellent debt management: D/E ratio {latest_de_ratio:.2f} - very conservative leverage"
                )
            elif latest_de_ratio < 0.7:  # Moderate debt levels
                score += 2
                details.append(
                    f"Good debt management: D/E ratio {latest_de_ratio:.2f} - prudent leverage"
                )
            elif latest_de_ratio < 1.5:
                score += 1
                details.append(
                    f"Moderate debt level: D/E ratio {latest_de_ratio:.2f} - acceptable but elevated"
                )
            else:
                details.append(
                    f"High debt concern: D/E ratio {latest_de_ratio:.2f} - excessive leverage risk"
                )
        else:
            details.append("Insufficient debt or equity data")

        # 3. Cash Management (Munger likes appropriate but not excessive cash)
        if (
            cash_history
            and revenue_history
            and len(cash_history) > 0
            and len(revenue_history) > 0
        ):
            cash_revenue_ratio = (
                cash_history[0] / revenue_history[0] if revenue_history[0] > 0 else 0
            )

            if 0.1 <= cash_revenue_ratio <= 0.25:  # Goldilocks zone
                score += 2
                details.append(
                    f"Prudent cash management: {cash_revenue_ratio:.1%} of revenue - optimal liquidity balance"
                )
            elif 0.05 <= cash_revenue_ratio < 0.1 or 0.25 < cash_revenue_ratio <= 0.4:
                score += 1
                details.append(
                    f"Acceptable cash level: {cash_revenue_ratio:.1%} of revenue - reasonable liquidity"
                )
            elif cash_revenue_ratio > 0.4:
                details.append(
                    f"Excess cash: {cash_revenue_ratio:.1%} of revenue - potentially inefficient capital allocation"
                )
            else:
                details.append(
                    f"Low cash reserves: {cash_revenue_ratio:.1%} of revenue - potential liquidity risk"
                )
        else:
            details.append("Insufficient cash or revenue data")

        # 4. Insider Activity Analysis (Munger values skin in the game)
        total_insider_trades = insider_buys + insider_sells
        if total_insider_trades > 0:
            buy_ratio = insider_buys / total_insider_trades

            if buy_ratio > 0.7:  # Strong insider buying signal
                score += 2
                details.append(
                    f"Strong insider alignment: {insider_buys}/{total_insider_trades} transactions are purchases - management confident"
                )
            elif buy_ratio > 0.4:  # Balanced insider activity
                score += 1
                details.append(
                    f"Moderate insider activity: {insider_buys}/{total_insider_trades} transactions are purchases"
                )
            elif buy_ratio < 0.1 and insider_sells > 5:  # Heavy selling pattern
                score -= 1
                details.append(
                    f"Concerning insider selling: {insider_sells}/{total_insider_trades} transactions are sales"
                )
            else:
                details.append(
                    f"Mixed insider signals: {insider_buys}/{total_insider_trades} transactions are purchases"
                )
        else:
            details.append("No insider trading data available")

        # 5. Share Count Management (Munger prefers stable or decreasing share count)
        if len(shares_history) >= 3:
            latest_shares = shares_history[0]
            earliest_shares = shares_history[-1]

            if latest_shares < earliest_shares * 0.95:  # 5%+ share reduction
                score += 2
                details.append(
                    "Excellent capital allocation: reducing share count through buybacks"
                )
            elif latest_shares < earliest_shares * 1.05:  # Stable share count
                score += 1
                details.append(
                    "Good share discipline: stable share count with limited dilution"
                )
            elif latest_shares > earliest_shares * 1.2:  # Significant dilution
                score -= 1
                details.append("Poor share discipline: significant dilution concerns")
            else:
                details.append("Moderate share count increase over time")
        else:
            details.append("Insufficient share count history")

        # Calculate derived metrics for return
        fcf_ni_conversion = avg_conversion if "avg_conversion" in locals() else None
        debt_equity_ratio = latest_de_ratio if "latest_de_ratio" in locals() else None
        cash_revenue_ratio = (
            cash_revenue_ratio if "cash_revenue_ratio" in locals() else None
        )
        insider_buy_ratio = buy_ratio if "buy_ratio" in locals() else None

        # Determine share count trend
        share_trend = "unknown"
        if len(shares_history) >= 3:
            if shares_history[0] < shares_history[-1] * 0.95:
                share_trend = "decreasing"
            elif shares_history[0] > shares_history[-1] * 1.05:
                share_trend = "increasing"
            else:
                share_trend = "stable"

    except Exception as e:
        logger.warning(f"Error in management quality analysis: {e}")
        details.append(f"Analysis error: {str(e)}")

    return {
        "score": score,
        "max_score": max_score,
        "details": "; ".join(details),
        "fcf_ni_conversion": fcf_ni_conversion,
        "debt_equity_ratio": debt_equity_ratio,
        "cash_revenue_ratio": cash_revenue_ratio,
        "insider_buy_ratio": insider_buy_ratio,
        "share_trend": share_trend,
    }


def analyze_predictability(
    financial_data: Annotated[
        Dict[str, Any],
        "Dictionary containing 5+ years of revenue, operating income, margins, and FCF data for predictability assessment",
    ],
) -> Dict[str, Any]:
    """
    Analyze business predictability using Munger's preference for understandable, stable businesses.

    Munger strongly favors businesses whose future cash flows are relatively predictable:
    - Consistent revenue growth with low volatility
    - Stable operating profitability over multiple cycles
    - Predictable margin structure (limited cyclical swings)
    - Reliable cash generation patterns

    Scoring criteria:
    - +3 points: Steady revenue growth (>5% avg, <10% volatility)
    - +3 points: Consistently positive operating income (100% of periods)
    - +2 points: Stable operating margins (<3% volatility)
    - +2 points: Reliable FCF generation (80%+ positive periods)

    Args:
        financial_data: Dictionary containing 5+ years of revenue, operating income, margin, FCF data

    Returns:
        Dict with predictability score and business stability analysis
    """
    score = 0
    details = []
    max_score = 10

    try:
        revenue_history = financial_data.get("revenue_history", [])
        operating_income_history = financial_data.get("operating_income_history", [])
        operating_margin_history = financial_data.get("operating_margin_history", [])
        fcf_history = financial_data.get("fcf_history", [])

        if len(revenue_history) < 5:
            return {
                "score": 0,
                "max_score": max_score,
                "details": "Insufficient historical data for predictability analysis (need 5+ years)",
                "revenue_volatility": None,
                "operating_consistency": None,
            }

        # 1. Revenue Stability and Growth (Munger's cornerstone of predictability)
        if len(revenue_history) >= 5:
            # Calculate year-over-year growth rates
            growth_rates = []
            for i in range(len(revenue_history) - 1):
                if revenue_history[i + 1] and revenue_history[i + 1] > 0:
                    growth_rate = (
                        revenue_history[i] - revenue_history[i + 1]
                    ) / revenue_history[i + 1]
                    growth_rates.append(growth_rate)

            if growth_rates:
                avg_growth = sum(growth_rates) / len(growth_rates)
                growth_volatility = sum(
                    abs(g - avg_growth) for g in growth_rates
                ) / len(growth_rates)

                if (
                    avg_growth > 0.05 and growth_volatility < 0.1
                ):  # >5% avg growth, <10% volatility
                    score += 3
                    details.append(
                        f"Highly predictable revenue: {avg_growth:.1%} avg growth with {growth_volatility:.1%} volatility - excellent visibility"
                    )
                elif (
                    avg_growth > 0 and growth_volatility < 0.2
                ):  # Positive but more volatile
                    score += 2
                    details.append(
                        f"Moderately predictable revenue: {avg_growth:.1%} avg growth with {growth_volatility:.1%} volatility"
                    )
                elif avg_growth > 0:  # Growing but unpredictable
                    score += 1
                    details.append(
                        f"Growing but volatile revenue: {avg_growth:.1%} avg growth with high {growth_volatility:.1%} volatility"
                    )
                else:
                    details.append(
                        f"Unpredictable revenue: {avg_growth:.1%} avg growth - declining or highly volatile"
                    )
            else:
                details.append(
                    "Cannot calculate revenue growth rates - data quality issues"
                )
        else:
            details.append("Insufficient revenue history for growth analysis")

        # 2. Operating Income Consistency (Munger's operational predictability test)
        if len(operating_income_history) >= 5:
            positive_periods = sum(
                1 for oi in operating_income_history if oi and oi > 0
            )
            consistency_ratio = positive_periods / len(operating_income_history)

            if consistency_ratio == 1.0:  # 100% positive periods
                score += 3
                details.append(
                    "Exceptional operational predictability: positive operating income in all periods"
                )
            elif consistency_ratio >= 0.8:  # 80%+ positive
                score += 2
                details.append(
                    f"Good operational consistency: positive operating income in {positive_periods}/{len(operating_income_history)} periods"
                )
            elif consistency_ratio >= 0.6:  # 60%+ positive
                score += 1
                details.append(
                    f"Moderate operational consistency: positive operating income in {positive_periods}/{len(operating_income_history)} periods"
                )
            else:
                details.append(
                    f"Poor operational consistency: positive operating income in only {positive_periods}/{len(operating_income_history)} periods"
                )
        else:
            details.append("Insufficient operating income history")

        # 3. Margin Stability (Munger values predictable profitability)
        if len(operating_margin_history) >= 5:
            valid_margins = [m for m in operating_margin_history if m is not None]
            if valid_margins:
                avg_margin = sum(valid_margins) / len(valid_margins)
                margin_volatility = sum(
                    abs(m - avg_margin) for m in valid_margins
                ) / len(valid_margins)

                if margin_volatility < 0.03:  # <3% margin volatility
                    score += 2
                    details.append(
                        f"Highly stable margins: {avg_margin:.1%} avg with {margin_volatility:.1%} volatility - predictable profitability"
                    )
                elif margin_volatility < 0.07:  # <7% margin volatility
                    score += 1
                    details.append(
                        f"Moderately stable margins: {avg_margin:.1%} avg with {margin_volatility:.1%} volatility"
                    )
                else:
                    details.append(
                        f"Volatile margins: {avg_margin:.1%} avg with high {margin_volatility:.1%} volatility - unpredictable profitability"
                    )
            else:
                details.append("No valid margin data for stability analysis")
        else:
            details.append("Insufficient margin history")

        # 4. Cash Flow Reliability (Munger's cash generation predictability)
        if len(fcf_history) >= 5:
            positive_fcf_periods = sum(1 for fcf in fcf_history if fcf and fcf > 0)
            fcf_consistency = positive_fcf_periods / len(fcf_history)

            if fcf_consistency == 1.0:  # 100% positive FCF
                score += 2
                details.append(
                    "Exceptional cash generation: positive FCF in all periods - highly predictable cash flows"
                )
            elif fcf_consistency >= 0.8:  # 80%+ positive FCF
                score += 1
                details.append(
                    f"Reliable cash generation: positive FCF in {positive_fcf_periods}/{len(fcf_history)} periods"
                )
            else:
                details.append(
                    f"Inconsistent cash generation: positive FCF in only {positive_fcf_periods}/{len(fcf_history)} periods"
                )
        else:
            details.append("Insufficient FCF history for reliability assessment")

    except Exception as e:
        logger.warning(f"Error in predictability analysis: {e}")
        details.append(f"Analysis error: {str(e)}")

    return {
        "score": score,
        "max_score": max_score,
        "details": "; ".join(details),
        "revenue_volatility": (
            growth_volatility if "growth_volatility" in locals() else None
        ),
        "operating_consistency": (
            consistency_ratio if "consistency_ratio" in locals() else None
        ),
        "margin_volatility": (
            margin_volatility if "margin_volatility" in locals() else None
        ),
    }


def calculate_munger_valuation(
    financial_data: Annotated[
        Dict[str, Any], "Dictionary containing FCF data for owner earnings valuation"
    ],
    market_cap: Annotated[
        float, "Current market capitalization for valuation comparison"
    ],
) -> Dict[str, Any]:
    """
    Calculate intrinsic value using Munger's simple, rational valuation approach.

    Munger prefers straightforward valuations based on "owner earnings" (FCF):
    - Normalize earnings over multiple years to avoid cyclical distortions
    - Apply simple multiples based on business quality and growth
    - Focus on FCF yield and margin of safety rather than complex DCF models
    - "Better to buy a wonderful company at a fair price than a fair company at a wonderful price"

    Scoring criteria:
    - +4 points: Excellent FCF yield (>8% - P/FCF <12.5x)
    - +3 points: Good FCF yield (>5% - P/FCF <20x)
    - +3 points: Large margin of safety (>30% upside to fair value)
    - +3 points: Growing FCF trend (>20% recent vs older average)

    Args:
        financial_data: Dictionary containing FCF history for normalization
        market_cap: Current market capitalization

    Returns:
        Dict with Munger valuation score and owner earnings analysis
    """
    score = 0
    details = []
    max_score = 10

    try:
        fcf_history = financial_data.get("fcf_history", [])

        if not fcf_history or len(fcf_history) < 3:
            return {
                "score": 0,
                "max_score": max_score,
                "details": "Insufficient FCF data for Munger valuation (need 3+ years)",
                "normalized_fcf": None,
                "fcf_yield": None,
                "margin_of_safety": None,
            }

        if not market_cap or market_cap <= 0:
            return {
                "score": 0,
                "max_score": max_score,
                "details": "Invalid market cap for valuation comparison",
                "normalized_fcf": None,
                "fcf_yield": None,
                "margin_of_safety": None,
            }

        # 1. Normalize Owner Earnings (Munger's approach to smoothing cyclical variations)
        periods_to_average = min(5, len(fcf_history))
        normalized_fcf = sum(fcf_history[:periods_to_average]) / periods_to_average

        if normalized_fcf <= 0:
            return {
                "score": 0,
                "max_score": max_score,
                "details": f"Negative normalized FCF ({normalized_fcf:,.0f}) - cannot establish owner earnings value",
                "normalized_fcf": normalized_fcf,
                "fcf_yield": None,
                "margin_of_safety": None,
            }

        # 2. Calculate FCF Yield (Munger's preferred valuation metric)
        fcf_yield = normalized_fcf / market_cap

        # Score based on FCF yield attractiveness
        if fcf_yield > 0.08:  # >8% yield (P/FCF <12.5x)
            score += 4
            details.append(
                f"Excellent value: {fcf_yield:.1%} FCF yield - exceptional owner earnings return"
            )
        elif fcf_yield > 0.05:  # >5% yield (P/FCF <20x)
            score += 3
            details.append(
                f"Good value: {fcf_yield:.1%} FCF yield - attractive owner earnings return"
            )
        elif fcf_yield > 0.03:  # >3% yield (P/FCF <33x)
            score += 1
            details.append(
                f"Fair value: {fcf_yield:.1%} FCF yield - reasonable owner earnings return"
            )
        else:
            details.append(
                f"Expensive: only {fcf_yield:.1%} FCF yield - poor owner earnings return"
            )

        # 3. Simple Intrinsic Value Calculation (Munger's straightforward approach)
        conservative_multiple = 10  # 10x FCF = 10% yield
        reasonable_multiple = 15  # 15x FCF = 6.7% yield
        optimistic_multiple = 20  # 20x FCF = 5% yield

        conservative_value = normalized_fcf * conservative_multiple
        reasonable_value = normalized_fcf * reasonable_multiple
        optimistic_value = normalized_fcf * optimistic_multiple

        # 4. Margin of Safety Analysis (vs reasonable value)
        margin_of_safety = (reasonable_value - market_cap) / market_cap

        if margin_of_safety > 0.3:  # >30% upside
            score += 3
            details.append(
                f"Large margin of safety: {margin_of_safety:.1%} upside to reasonable value - compelling opportunity"
            )
        elif margin_of_safety > 0.1:  # >10% upside
            score += 2
            details.append(
                f"Moderate margin of safety: {margin_of_safety:.1%} upside to reasonable value - adequate buffer"
            )
        elif margin_of_safety > -0.1:  # Within 10% of fair value
            score += 1
            details.append(
                f"Fair pricing: {margin_of_safety:.1%} vs reasonable value - limited margin"
            )
        else:
            details.append(
                f"Overvalued: {margin_of_safety:.1%} vs reasonable value - insufficient margin of safety"
            )

        # 5. FCF Growth Trajectory (Munger likes growing owner earnings)
        if len(fcf_history) >= 6:
            recent_avg = sum(fcf_history[:3]) / 3  # Last 3 years
            older_avg = sum(fcf_history[-3:]) / 3  # Oldest 3 years
            fcf_growth = (
                (recent_avg - older_avg) / abs(older_avg) if older_avg != 0 else 0
            )

            if fcf_growth > 0.2:  # >20% FCF growth
                score += 3
                details.append(
                    f"Growing owner earnings: {fcf_growth:.1%} FCF growth trend enhances intrinsic value"
                )
            elif fcf_growth > 0:
                score += 2
                details.append(
                    f"Stable owner earnings: {fcf_growth:.1%} FCF growth supports valuation"
                )
            else:
                details.append(
                    f"Declining owner earnings: {fcf_growth:.1%} FCF trend concerning for value"
                )
        else:
            details.append("Limited FCF history for growth trend analysis")

        # Summary valuation details
        details.append(
            f"Normalized FCF: ${normalized_fcf:,.0f} based on {periods_to_average}-year average"
        )
        details.append(
            f"Valuation range: ${conservative_value:,.0f} - ${optimistic_value:,.0f}"
        )

    except Exception as e:
        logger.warning(f"Error in Munger valuation analysis: {e}")
        details.append(f"Valuation analysis error: {str(e)}")

    return {
        "score": score,
        "max_score": max_score,
        "details": "; ".join(details),
        "normalized_fcf": normalized_fcf if "normalized_fcf" in locals() else None,
        "fcf_yield": fcf_yield if "fcf_yield" in locals() else None,
        "margin_of_safety": (
            margin_of_safety if "margin_of_safety" in locals() else None
        ),
        "intrinsic_value_range": {
            "conservative": (
                conservative_value if "conservative_value" in locals() else None
            ),
            "reasonable": reasonable_value if "reasonable_value" in locals() else None,
            "optimistic": optimistic_value if "optimistic_value" in locals() else None,
        },
        "fcf_trend": fcf_growth if "fcf_growth" in locals() else None,
    }


def calculate_munger_score(
    moat_analysis: Annotated[Dict[str, Any], "Results from moat strength analysis"],
    management_analysis: Annotated[
        Dict[str, Any], "Results from management quality analysis"
    ],
    predictability_analysis: Annotated[
        Dict[str, Any], "Results from business predictability analysis"
    ],
    valuation_analysis: Annotated[
        Dict[str, Any], "Results from Munger valuation analysis"
    ],
) -> Dict[str, Any]:
    """
    Calculate overall Munger investment score using his quality-focused weighting.

    Munger's investment criteria prioritize quality over price:
    - Business quality (moat + predictability) weighted 60%
    - Management quality weighted 25%
    - Valuation weighted 15%
    - Very high standards: 75%+ for bullish, 55%+ for neutral

    Signal generation:
    - Bullish: Score ≥75% (exceptional quality with reasonable price)
    - Bearish: Score ≤55% (quality concerns or excessive price)
    - Neutral: Score 55-75% (mixed quality/valuation signals)

    Args:
        moat_analysis: Competitive moat assessment results
        management_analysis: Management quality assessment results
        predictability_analysis: Business predictability assessment results
        valuation_analysis: Rational valuation assessment results

    Returns:
        Dict with overall Munger score, signal, and detailed quality breakdown
    """
    try:
        moat_score = moat_analysis.get("score", 0)
        management_score = management_analysis.get("score", 0)
        predictability_score = predictability_analysis.get("score", 0)
        valuation_score = valuation_analysis.get("score", 0)

        moat_max = moat_analysis.get("max_score", 9)
        management_max = management_analysis.get("max_score", 12)
        predictability_max = predictability_analysis.get("max_score", 10)
        valuation_max = valuation_analysis.get("max_score", 10)

        # Apply Munger's quality-focused weighting
        # Quality business (moat + predictability): 60% weight
        quality_score = (moat_score / moat_max) * 0.35 + (
            predictability_score / predictability_max
        ) * 0.25

        # Management quality: 25% weight
        management_weight = (management_score / management_max) * 0.25

        # Valuation: 15% weight (lower because Munger accepts fair prices for quality)
        valuation_weight = (valuation_score / valuation_max) * 0.15

        # Total weighted score (0-1 scale)
        total_weighted_score = quality_score + management_weight + valuation_weight
        score_percentage = total_weighted_score

        # Convert to 0-10 scale for consistency
        final_score = total_weighted_score * 10

        # Munger's high standards for signal generation
        if score_percentage >= 0.75:  # 75%+ - exceptional across all dimensions
            signal = "bullish"
            signal_strength = "Exceptional Munger characteristics - wonderful business at reasonable price"
        elif score_percentage <= 0.55:  # 55%- - quality concerns or overvaluation
            signal = "bearish"
            signal_strength = "Fails Munger quality standards - avoid poor business or excessive price"
        else:  # 55-75% - mixed signals
            signal = "neutral"
            signal_strength = (
                "Mixed Munger signals - some quality but not compelling opportunity"
            )

        # Detailed component breakdown
        breakdown = {
            "moat_strength": f"{moat_score:.1f}/{moat_max}",
            "management_quality": f"{management_score:.1f}/{management_max}",
            "predictability": f"{predictability_score:.1f}/{predictability_max}",
            "valuation": f"{valuation_score:.1f}/{valuation_max}",
        }

        # Munger-specific quality flags for decision context
        quality_flags = {
            "strong_moat": (moat_score / moat_max) >= 0.7,
            "predictable_business": (predictability_score / predictability_max) >= 0.7,
            "aligned_management": (management_score / management_max) >= 0.7,
            "reasonable_price": valuation_analysis.get("margin_of_safety", 0) > 0,
            "high_roic": moat_analysis.get("roic_consistency", 0) >= 0.5,
            "conservative_balance_sheet": management_analysis.get(
                "debt_equity_ratio", 1.0
            )
            < 0.7,
        }

    except Exception as e:
        logger.warning(f"Error calculating Munger score: {e}")
        return {
            "total_score": 0,
            "score_percentage": 0,
            "signal": "neutral",
            "signal_strength": f"Scoring error: {str(e)}",
            "breakdown": {},
            "quality_flags": {},
        }

    return {
        "total_score": final_score,
        "score_percentage": score_percentage,
        "signal": signal,
        "signal_strength": signal_strength,
        "breakdown": breakdown,
        "quality_flags": quality_flags,
        "munger_weighting": {
            "business_quality": "60%",
            "management_quality": "25%",
            "valuation": "15%",
        },
    }
