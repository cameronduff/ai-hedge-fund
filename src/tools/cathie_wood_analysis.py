"""
Cathie Wood-style disruptive innovation analysis tools.
Implements her focus on breakthrough technologies, exponential growth, and transformative business models.
"""

from typing import Dict, List, Optional, Any, Annotated
import json
from loguru import logger


def analyze_disruptive_potential(
    financial_data: Annotated[
        Dict[str, Any],
        "Dictionary containing revenue history, gross margins, R&D spending, and operational metrics for disruptive potential assessment",
    ],
) -> Dict[str, Any]:
    """
    Analyze disruptive potential following Cathie Wood's criteria for breakthrough technologies.

    Wood focuses on companies with transformative technologies that can create new markets or
    fundamentally disrupt existing industries. Scoring criteria:
    - +3 points: Exceptional revenue growth (>100% latest year)
    - +2 points: Strong revenue growth (>50% latest year)
    - +1 point: Moderate growth (>20% latest year)
    - +2 points: Revenue growth acceleration (increasing growth rates)
    - +2 points: Expanding gross margins (indicates scaling/pricing power)
    - +3 points: High R&D intensity (>15% of revenue)
    - +2 points: Positive operating leverage (revenue growing faster than expenses)

    Args:
        financial_data: Dictionary containing revenue_history, gross_margin_history, rd_expenses, operating_expenses

    Returns:
        Dict with disruptive potential score and detailed innovation analysis
    """
    score = 0
    details = []
    max_score = 15

    try:
        revenue_history = financial_data.get("revenue_history", [])
        gross_margin_history = financial_data.get("gross_margin_history", [])
        rd_expenses = financial_data.get("research_and_development", 0)
        operating_expenses = financial_data.get("operating_expense_history", [])

        # 1. Revenue Growth Analysis - Wood's key indicator of market disruption
        if len(revenue_history) >= 2:
            latest_revenue = revenue_history[0]  # Most recent
            prior_revenue = revenue_history[1]  # Previous year
            oldest_revenue = revenue_history[-1]  # Oldest available

            if latest_revenue and prior_revenue and prior_revenue > 0:
                latest_growth = (latest_revenue - prior_revenue) / prior_revenue

                if latest_growth > 1.0:  # >100% growth
                    score += 3
                    details.append(
                        f"Exceptional revenue growth: {latest_growth:.1%} indicates breakthrough market adoption"
                    )
                elif latest_growth > 0.5:  # >50% growth
                    score += 2
                    details.append(
                        f"Strong revenue growth: {latest_growth:.1%} shows disruptive market expansion"
                    )
                elif latest_growth > 0.2:  # >20% growth
                    score += 1
                    details.append(
                        f"Solid revenue growth: {latest_growth:.1%} suggests innovation traction"
                    )
                else:
                    details.append(
                        f"Weak revenue growth: {latest_growth:.1%} - insufficient for Wood's disruption criteria"
                    )
            else:
                details.append(
                    "Cannot calculate latest revenue growth - insufficient data quality"
                )

            # 2. Growth Acceleration Analysis (Wood looks for exponential curves)
            if len(revenue_history) >= 3:
                growth_rates = []
                for i in range(len(revenue_history) - 1):
                    if (
                        revenue_history[i]
                        and revenue_history[i + 1]
                        and revenue_history[i + 1] > 0
                    ):
                        growth_rate = (
                            revenue_history[i] - revenue_history[i + 1]
                        ) / revenue_history[i + 1]
                        growth_rates.append(growth_rate)

                if len(growth_rates) >= 2:
                    # Check if recent growth > older growth (acceleration)
                    if growth_rates[0] > growth_rates[-1]:
                        score += 2
                        details.append(
                            f"Growth acceleration detected: {growth_rates[0]:.1%} vs {growth_rates[-1]:.1%} - exponential adoption pattern"
                        )
                    else:
                        details.append(
                            "No growth acceleration - growth may be plateauing"
                        )
        else:
            details.append("Insufficient revenue history for disruption assessment")

        # 3. Gross Margin Expansion (indicates scalability and pricing power)
        if len(gross_margin_history) >= 2:
            latest_margin = gross_margin_history[0]
            earliest_margin = gross_margin_history[-1]

            if latest_margin and earliest_margin:
                margin_expansion = latest_margin - earliest_margin
                if margin_expansion > 0.05:  # 5%+ margin expansion
                    score += 2
                    details.append(
                        f"Strong margin expansion: +{margin_expansion:.1%} indicates scaling efficiency and pricing power"
                    )
                elif margin_expansion > 0:
                    score += 1
                    details.append(
                        f"Margin improvement: +{margin_expansion:.1%} shows some operational leverage"
                    )
                else:
                    details.append(
                        "No margin expansion - may face competitive pressure or scaling challenges"
                    )

                # Also score high absolute margins
                if latest_margin and latest_margin > 0.7:  # 70%+ gross margin
                    score += 1
                    details.append(
                        f"Exceptional gross margin: {latest_margin:.1%} indicates strong differentiation/moat"
                    )
        else:
            details.append("No gross margin data for scalability assessment")

        # 4. R&D Investment Intensity (Wood's innovation indicator)
        if rd_expenses and revenue_history and revenue_history[0]:
            rd_intensity = rd_expenses / revenue_history[0]
            if rd_intensity > 0.15:  # 15%+ R&D intensity
                score += 3
                details.append(
                    f"Exceptional R&D investment: {rd_intensity:.1%} of revenue - strong innovation commitment"
                )
            elif rd_intensity > 0.08:
                score += 2
                details.append(
                    f"Strong R&D investment: {rd_intensity:.1%} of revenue - solid innovation focus"
                )
            elif rd_intensity > 0.05:
                score += 1
                details.append(
                    f"Moderate R&D investment: {rd_intensity:.1%} of revenue - some innovation activity"
                )
            else:
                details.append(
                    f"Low R&D intensity: {rd_intensity:.1%} - insufficient innovation investment for Wood's criteria"
                )
        else:
            details.append("No R&D data available for innovation assessment")

        # 5. Operating Leverage Analysis (revenue scaling faster than costs)
        if len(revenue_history) >= 2 and len(operating_expenses) >= 2:
            revenue_growth = (
                (revenue_history[0] - revenue_history[1]) / revenue_history[1]
                if revenue_history[1] > 0
                else 0
            )
            opex_growth = (
                (operating_expenses[0] - operating_expenses[1]) / operating_expenses[1]
                if operating_expenses[1] > 0
                else 0
            )

            if revenue_growth > opex_growth and revenue_growth > 0:
                leverage_factor = revenue_growth - opex_growth
                score += 2
                details.append(
                    f"Strong operating leverage: Revenue growing {leverage_factor:.1%} faster than expenses - efficient scaling"
                )
            else:
                details.append(
                    "No operating leverage detected - expenses growing as fast as revenue"
                )
        else:
            details.append("Insufficient data for operating leverage analysis")

    except Exception as e:
        logger.warning(f"Error in disruptive potential analysis: {e}")
        details.append(f"Analysis error: {str(e)}")

    return {
        "score": score,
        "max_score": max_score,
        "details": "; ".join(details),
        "latest_revenue_growth": latest_growth if "latest_growth" in locals() else None,
        "rd_intensity": rd_intensity if "rd_intensity" in locals() else None,
        "margin_expansion": (
            margin_expansion if "margin_expansion" in locals() else None
        ),
    }


def analyze_innovation_growth(
    financial_data: Annotated[
        Dict[str, Any],
        "Dictionary containing R&D trends, free cash flow, operating margins, and capital allocation data",
    ],
) -> Dict[str, Any]:
    """
    Analyze innovation-driven growth following Wood's focus on exponential scaling potential.

    Wood looks for companies that reinvest heavily in innovation and demonstrate ability to
    scale breakthrough technologies. Scoring criteria:
    - +3 points: Strong R&D growth (>50%) with increasing intensity
    - +2 points: Consistent positive FCF with growth (innovation funding capacity)
    - +3 points: Improving operating margins >15% (efficient innovation scaling)
    - +2 points: High capex investment (>10% revenue) with growth (infrastructure building)
    - +2 points: Low dividend payout (<20%) indicating reinvestment focus

    Args:
        financial_data: Dictionary containing R&D trends, FCF, margins, capex, dividend data

    Returns:
        Dict with innovation growth score and scaling analysis
    """
    score = 0
    details = []
    max_score = 12

    try:
        rd_history = financial_data.get("rd_history", [])
        revenue_history = financial_data.get("revenue_history", [])
        fcf_history = financial_data.get("free_cash_flow_history", [])
        operating_margin_history = financial_data.get("operating_margin_history", [])
        capex_history = financial_data.get("capex_history", [])
        dividend_history = financial_data.get("dividend_history", [])

        # 1. R&D Investment Trends (Wood's innovation commitment indicator)
        if len(rd_history) >= 2 and len(revenue_history) >= 2:
            rd_growth = (
                (rd_history[0] - rd_history[-1]) / rd_history[-1]
                if rd_history[-1] > 0
                else 0
            )

            # Calculate R&D intensity trend
            rd_intensity_latest = (
                rd_history[0] / revenue_history[0] if revenue_history[0] > 0 else 0
            )
            rd_intensity_earliest = (
                rd_history[-1] / revenue_history[-1] if revenue_history[-1] > 0 else 0
            )

            if rd_growth > 0.5 and rd_intensity_latest > rd_intensity_earliest:
                score += 3
                details.append(
                    f"Exceptional R&D scaling: {rd_growth:.1%} growth with increasing intensity"
                )
            elif rd_growth > 0.2:
                score += 2
                details.append(f"Strong R&D investment growth: {rd_growth:.1%}")
            elif rd_growth > 0:
                score += 1
                details.append(f"Moderate R&D growth: {rd_growth:.1%}")
            else:
                details.append(
                    f"Declining R&D investment: {rd_growth:.1%} - concerning for innovation focus"
                )
        else:
            details.append("Insufficient R&D data for trend analysis")

        # 2. Free Cash Flow Analysis (ability to fund innovation)
        if len(fcf_history) >= 2:
            positive_fcf_periods = sum(1 for fcf in fcf_history if fcf and fcf > 0)
            fcf_consistency = positive_fcf_periods / len(fcf_history)

            if fcf_history[0] and fcf_history[-1]:
                fcf_growth = (fcf_history[0] - fcf_history[-1]) / abs(fcf_history[-1])

                if fcf_growth > 0.3 and fcf_consistency >= 0.75:
                    score += 2
                    details.append(
                        f"Strong FCF growth: {fcf_growth:.1%} with {fcf_consistency:.1%} consistency - excellent innovation funding"
                    )
                elif fcf_consistency >= 0.5:
                    score += 1
                    details.append(
                        f"Adequate FCF generation: {fcf_consistency:.1%} consistency supports innovation investment"
                    )
                else:
                    details.append(
                        f"Inconsistent FCF: only {fcf_consistency:.1%} positive periods - limited innovation funding capacity"
                    )
        else:
            details.append("No FCF data for innovation funding assessment")

        # 3. Operating Margin Efficiency (Wood looks for efficient scaling)
        if len(operating_margin_history) >= 2:
            latest_margin = operating_margin_history[0]
            margin_trend = operating_margin_history[0] - operating_margin_history[-1]

            if latest_margin and latest_margin > 0.15 and margin_trend > 0:
                score += 3
                details.append(
                    f"Excellent operating efficiency: {latest_margin:.1%} margins improving by {margin_trend:.1%}"
                )
            elif latest_margin and latest_margin > 0.10:
                score += 2
                details.append(
                    f"Good operating margins: {latest_margin:.1%} shows efficient scaling"
                )
            elif margin_trend and margin_trend > 0:
                score += 1
                details.append(
                    "Improving operational efficiency despite current challenges"
                )
            else:
                details.append(
                    "Margins below Wood's efficiency standards for innovation scaling"
                )
        else:
            details.append("No operating margin data for efficiency assessment")

        # 4. Capital Investment Analysis (infrastructure for growth)
        if len(capex_history) >= 2 and len(revenue_history) >= 2:
            capex_intensity = (
                abs(capex_history[0]) / revenue_history[0]
                if revenue_history[0] > 0
                else 0
            )
            capex_growth = (
                (abs(capex_history[0]) - abs(capex_history[-1]))
                / abs(capex_history[-1])
                if capex_history[-1] > 0
                else 0
            )

            if capex_intensity > 0.10 and capex_growth > 0.2:
                score += 2
                details.append(
                    f"Strong growth investment: {capex_intensity:.1%} capex intensity with {capex_growth:.1%} growth"
                )
            elif capex_intensity > 0.05:
                score += 1
                details.append(
                    f"Moderate growth investment: {capex_intensity:.1%} of revenue in capex"
                )
            else:
                details.append("Limited capital investment in growth infrastructure")
        else:
            details.append("Insufficient capex data for growth investment analysis")

        # 5. Reinvestment Focus (low dividends indicate growth reinvestment)
        if (
            dividend_history
            and fcf_history
            and len(dividend_history) > 0
            and len(fcf_history) > 0
        ):
            if fcf_history[0] and fcf_history[0] > 0:
                payout_ratio = (
                    abs(dividend_history[0]) / fcf_history[0]
                    if dividend_history[0]
                    else 0
                )

                if payout_ratio < 0.2:  # <20% payout
                    score += 2
                    details.append(
                        f"Strong reinvestment focus: {payout_ratio:.1%} payout ratio - prioritizing growth over dividends"
                    )
                elif payout_ratio < 0.4:
                    score += 1
                    details.append(
                        f"Moderate reinvestment: {payout_ratio:.1%} payout ratio"
                    )
                else:
                    details.append(
                        f"High dividend payout: {payout_ratio:.1%} - may limit growth reinvestment"
                    )
            else:
                details.append("Negative FCF limits dividend analysis")
        else:
            details.append("No dividend data for reinvestment focus assessment")

    except Exception as e:
        logger.warning(f"Error in innovation growth analysis: {e}")
        details.append(f"Analysis error: {str(e)}")

    return {
        "score": score,
        "max_score": max_score,
        "details": "; ".join(details),
        "rd_growth": rd_growth if "rd_growth" in locals() else None,
        "fcf_consistency": fcf_consistency if "fcf_consistency" in locals() else None,
        "capex_intensity": capex_intensity if "capex_intensity" in locals() else None,
    }


def analyze_cathie_wood_valuation(
    financial_data: Annotated[
        Dict[str, Any],
        "Dictionary containing free cash flow for high-growth DCF analysis",
    ],
    market_cap: Annotated[
        float, "Current market capitalization for valuation comparison"
    ],
) -> Dict[str, Any]:
    """
    Perform Cathie Wood-style valuation analysis using high-growth DCF methodology.

    Wood uses aggressive growth assumptions reflecting exponential innovation adoption:
    - High growth rates (20%+ for disruptive companies)
    - Higher terminal multiples reflecting platform/network effects
    - Longer growth periods for transformative technologies
    - Focus on total addressable market (TAM) expansion

    Scoring criteria:
    - +5 points: >50% margin of safety (exceptional growth opportunity)
    - +3 points: >20% margin of safety (strong growth value)
    - +1 point: Positive margin of safety (some undervaluation)

    Args:
        financial_data: Dictionary containing latest free_cash_flow
        market_cap: Current market capitalization

    Returns:
        Dict with high-growth valuation score and exponential growth analysis
    """
    score = 0
    details = []
    max_score = 5

    try:
        latest_fcf = financial_data.get("free_cash_flow", 0)

        if not latest_fcf or latest_fcf <= 0:
            # Wood sometimes invests in pre-profitability companies with strong growth
            return {
                "score": 0,
                "max_score": max_score,
                "details": f"No positive FCF currently: {latest_fcf} - may be acceptable for early-stage disruptive company",
                "intrinsic_value": None,
                "margin_of_safety": None,
                "growth_scenario": "pre_profitability",
            }

        if not market_cap or market_cap <= 0:
            return {
                "score": 0,
                "max_score": max_score,
                "details": "Invalid market cap for valuation comparison",
                "intrinsic_value": None,
                "margin_of_safety": None,
            }

        # Cathie Wood-style high-growth DCF assumptions
        growth_rate = 0.20  # 20% long-term growth (aggressive for innovation)
        discount_rate = 0.15  # 15% discount rate (higher risk for growth)
        terminal_multiple = 25  # 25x terminal FCF (network effects/platforms)
        projection_years = 7  # Longer projection for transformative tech

        # Calculate present value of projected FCF (exponential growth phase)
        present_value = 0
        for year in range(1, projection_years + 1):
            future_fcf = latest_fcf * (1 + growth_rate) ** year
            pv = future_fcf / ((1 + discount_rate) ** year)
            present_value += pv

        # Terminal value calculation (mature growth phase)
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

        # Score based on Wood's aggressive growth expectations
        if margin_of_safety > 0.5:  # 50%+ undervaluation
            score += 5
            details.append(
                f"Exceptional growth opportunity: {margin_of_safety:.1%} margin of safety - massive disruption potential"
            )
        elif margin_of_safety > 0.2:  # 20%+ undervaluation
            score += 3
            details.append(
                f"Strong growth value: {margin_of_safety:.1%} margin of safety - significant innovation upside"
            )
        elif margin_of_safety > 0:  # Any undervaluation
            score += 1
            details.append(
                f"Moderate opportunity: {margin_of_safety:.1%} margin of safety - some growth potential"
            )
        else:
            details.append(
                f"Overvalued at current levels: {margin_of_safety:.1%} - market may be ahead of fundamentals"
            )

        details.append(
            f"High-growth DCF value: ${intrinsic_value:,.0f} vs market cap: ${market_cap:,.0f}"
        )
        details.append(
            f"Aggressive assumptions: {growth_rate:.1%} growth, {terminal_multiple}x terminal multiple, {projection_years}-year horizon"
        )

        # Additional context for Wood's investment style
        if margin_of_safety < -0.3:  # 30%+ overvaluation
            details.append(
                "Significant overvaluation may indicate market speculation - wait for better entry point"
            )
        elif latest_fcf < market_cap * 0.02:  # FCF yield <2%
            details.append(
                "Low FCF yield requires exceptional growth execution to justify current valuation"
            )

    except Exception as e:
        logger.warning(f"Error in Cathie Wood valuation analysis: {e}")
        details.append(f"Valuation analysis error: {str(e)}")
        intrinsic_value = None
        margin_of_safety = None

    return {
        "score": score,
        "max_score": max_score,
        "details": "; ".join(details),
        "intrinsic_value": intrinsic_value,
        "margin_of_safety": margin_of_safety,
        "growth_assumptions": {
            "growth_rate": growth_rate if "growth_rate" in locals() else None,
            "discount_rate": discount_rate if "discount_rate" in locals() else None,
            "terminal_multiple": (
                terminal_multiple if "terminal_multiple" in locals() else None
            ),
            "projection_years": (
                projection_years if "projection_years" in locals() else None
            ),
        },
        "growth_scenario": "exponential_innovation",
    }


def calculate_cathie_wood_score(
    disruptive_analysis: Annotated[
        Dict[str, Any], "Results from disruptive potential analysis"
    ],
    innovation_analysis: Annotated[
        Dict[str, Any], "Results from innovation growth analysis"
    ],
    valuation_analysis: Annotated[
        Dict[str, Any], "Results from high-growth valuation analysis"
    ],
) -> Dict[str, Any]:
    """
    Calculate overall Cathie Wood investment score and generate signal.

    Wood's signal criteria (focused on exponential growth potential):
    - Bullish: Total score >= 70% AND strong disruptive potential (breakthrough technology focus)
    - Bearish: Total score <= 30% OR lack of innovation investment/growth
    - Neutral: Score between 30-70% OR mixed innovation signals

    Args:
        disruptive_analysis: Disruptive potential assessment results
        innovation_analysis: Innovation growth assessment results
        valuation_analysis: High-growth valuation analysis results

    Returns:
        Dict with overall score, signal, and detailed innovation breakdown
    """
    try:
        disruptive_score = disruptive_analysis.get("score", 0)
        innovation_score = innovation_analysis.get("score", 0)
        valuation_score = valuation_analysis.get("score", 0)

        disruptive_max = disruptive_analysis.get("max_score", 15)
        innovation_max = innovation_analysis.get("max_score", 12)
        valuation_max = valuation_analysis.get("max_score", 5)

        total_score = disruptive_score + innovation_score + valuation_score
        max_possible_score = disruptive_max + innovation_max + valuation_max
        score_percentage = (
            (total_score / max_possible_score) if max_possible_score > 0 else 0
        )

        # Wood prioritizes disruptive potential - require strong disruption score for bullish
        disruptive_percentage = (
            (disruptive_score / disruptive_max) if disruptive_max > 0 else 0
        )

        # Determine Cathie Wood signal with disruption emphasis
        if score_percentage >= 0.7 and disruptive_percentage >= 0.6:
            signal = "bullish"
            signal_strength = "Strong disruption characteristics - breakthrough technology with exponential growth potential"
        elif score_percentage <= 0.3 or disruptive_percentage <= 0.2:
            signal = "bearish"
            signal_strength = "Insufficient innovation/disruption - lacks transformative technology or growth trajectory"
        else:
            signal = "neutral"
            signal_strength = "Mixed innovation signals - some disruptive elements but not compelling breakthrough opportunity"

        breakdown = {
            "disruptive_potential": f"{disruptive_score:.1f}/{disruptive_max}",
            "innovation_growth": f"{innovation_score:.1f}/{innovation_max}",
            "valuation": f"{valuation_score:.1f}/{valuation_max}",
        }

        # Additional Wood-specific insights
        insights = []
        if disruptive_percentage >= 0.8:
            insights.append(
                "Exceptional disruptive potential - prime Wood investment candidate"
            )
        if innovation_analysis.get("rd_intensity", 0) > 0.15:
            insights.append(
                "Strong R&D investment suggests serious innovation commitment"
            )
        if valuation_analysis.get("margin_of_safety", 0) > 0.3:
            insights.append(
                "Significant undervaluation provides attractive entry point for long-term growth"
            )

    except Exception as e:
        logger.warning(f"Error calculating Cathie Wood score: {e}")
        return {
            "total_score": 0,
            "max_possible_score": 32,
            "score_percentage": 0,
            "signal": "neutral",
            "signal_strength": f"Scoring error: {str(e)}",
            "breakdown": {},
            "insights": [],
        }

    return {
        "total_score": total_score,
        "max_possible_score": max_possible_score,
        "score_percentage": score_percentage,
        "disruptive_percentage": disruptive_percentage,
        "signal": signal,
        "signal_strength": signal_strength,
        "breakdown": breakdown,
        "insights": insights if "insights" in locals() else [],
    }
