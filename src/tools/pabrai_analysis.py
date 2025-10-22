from typing import Annotated, Dict, Any, Optional, List


def analyze_downside_protection(
    financial_data: Annotated[
        Dict[str, Any],
        "Financial balance sheet and cash flow data for downside protection analysis",
    ],
) -> Annotated[
    Dict[str, Any],
    "Downside protection analysis focusing on capital preservation and balance sheet strength",
]:
    """
    Analyze downside protection using Mohnish Pabrai's 'tails I don't lose much' philosophy.
    Focus on balance sheet strength, liquidity, and cash generation stability.

    Key factors:
    - Net cash position (preferred) vs net debt
    - Current ratio for liquidity assessment
    - Debt-to-equity ratios (low leverage preferred)
    - Free cash flow stability and positivity
    """
    try:
        analysis = {
            "net_cash_position": None,
            "current_ratio": None,
            "debt_to_equity": None,
            "fcf_stability": None,
            "score": 0,
            "max_score": 10,
            "details": [],
        }

        line_items = financial_data.get("line_items", [])
        if not line_items:
            analysis["details"].append("No financial line items available")
            return analysis

        latest = line_items[0]

        # Net Cash Position Analysis (3 points max)
        cash = latest.get("cash_and_equivalents")
        debt = latest.get("total_debt")

        if cash is not None and debt is not None:
            net_cash = cash - debt
            analysis["net_cash_position"] = net_cash

            if net_cash > 0:
                analysis["score"] += 3
                analysis["details"].append(
                    f"Strong net cash position: ${net_cash/1e6:.0f}M - excellent downside protection"
                )
            else:
                analysis["details"].append(
                    f"Net debt position: ${abs(net_cash)/1e6:.0f}M - potential risk"
                )
        else:
            analysis["details"].append(
                "Cash/debt data unavailable - cannot assess net position"
            )

        # Current Ratio Analysis (2 points max)
        current_assets = latest.get("current_assets")
        current_liabilities = latest.get("current_liabilities")

        if current_assets and current_liabilities and current_liabilities > 0:
            current_ratio = current_assets / current_liabilities
            analysis["current_ratio"] = current_ratio

            if current_ratio >= 2.0:
                analysis["score"] += 2
                analysis["details"].append(
                    f"Excellent liquidity - current ratio {current_ratio:.2f}"
                )
            elif current_ratio >= 1.2:
                analysis["score"] += 1
                analysis["details"].append(
                    f"Adequate liquidity - current ratio {current_ratio:.2f}"
                )
            else:
                analysis["details"].append(
                    f"Weak liquidity - current ratio {current_ratio:.2f}"
                )
        else:
            analysis["details"].append("Current ratio data unavailable")

        # Debt-to-Equity Analysis (2 points max)
        equity = latest.get("shareholders_equity")

        if equity and equity > 0 and debt is not None:
            de_ratio = debt / equity
            analysis["debt_to_equity"] = de_ratio

            if de_ratio < 0.3:
                analysis["score"] += 2
                analysis["details"].append(
                    f"Very conservative leverage - D/E {de_ratio:.2f}"
                )
            elif de_ratio < 0.7:
                analysis["score"] += 1
                analysis["details"].append(f"Moderate leverage - D/E {de_ratio:.2f}")
            else:
                analysis["details"].append(f"High leverage risk - D/E {de_ratio:.2f}")
        else:
            analysis["details"].append("Debt-to-equity calculation unavailable")

        # Free Cash Flow Stability (3 points max)
        fcf_values = [
            item.get("free_cash_flow")
            for item in line_items
            if item.get("free_cash_flow") is not None
        ]

        if fcf_values and len(fcf_values) >= 3:
            recent_avg = sum(fcf_values[:3]) / 3
            older_avg = (
                sum(fcf_values[-3:]) / 3 if len(fcf_values) >= 6 else fcf_values[-1]
            )

            analysis["fcf_stability"] = {
                "recent_avg": recent_avg,
                "older_avg": older_avg,
                "growth": (recent_avg / older_avg - 1) if older_avg != 0 else 0,
            }

            if recent_avg > 0 and recent_avg >= older_avg:
                analysis["score"] += 3
                analysis["details"].append(
                    "Positive and stable/improving FCF - reliable cash generation"
                )
            elif recent_avg > 0:
                analysis["score"] += 2
                analysis["details"].append("Positive but declining FCF - monitor trend")
            else:
                analysis["details"].append("Negative FCF - cash burn concern")
        else:
            analysis["details"].append(
                "Insufficient FCF history for stability analysis"
            )

        return analysis

    except Exception as e:
        return {
            "error": f"Downside protection analysis failed: {str(e)}",
            "score": 0,
            "max_score": 10,
            "details": ["Error in downside protection analysis"],
        }


def analyze_pabrai_valuation(
    financial_data: Annotated[
        Dict[str, Any],
        "Financial data and market cap for Pabrai-style valuation analysis",
    ],
) -> Annotated[
    Dict[str, Any],
    "Pabrai valuation analysis focusing on FCF yield and asset-light characteristics",
]:
    """
    Analyze valuation using Pabrai's preference for high FCF yields and asset-light business models.
    Keep it simple with focus on sustainable cash generation relative to market cap.

    Key metrics:
    - Normalized FCF yield (5+ years average preferred)
    - Asset-light preference (low capex intensity)
    - Sustainable cash generation capacity
    - Margin of safety assessment
    """
    try:
        analysis = {
            "fcf_yield": None,
            "normalized_fcf": None,
            "capex_intensity": None,
            "asset_light_score": 0,
            "score": 0,
            "max_score": 10,
            "details": [],
        }

        line_items = financial_data.get("line_items", [])
        market_cap = financial_data.get("market_cap")

        if not line_items or not market_cap or market_cap <= 0:
            analysis["details"].append("Insufficient data for valuation analysis")
            return analysis

        # FCF Yield Analysis (6 points max)
        fcf_values = [
            item.get("free_cash_flow")
            for item in line_items
            if item.get("free_cash_flow") is not None
        ]

        if fcf_values and len(fcf_values) >= 3:
            # Use 5-year average or available years
            years_to_use = min(5, len(fcf_values))
            normalized_fcf = sum(fcf_values[:years_to_use]) / years_to_use
            analysis["normalized_fcf"] = normalized_fcf

            if normalized_fcf > 0:
                fcf_yield = normalized_fcf / market_cap
                analysis["fcf_yield"] = fcf_yield

                if fcf_yield > 0.10:  # 10%+ FCF yield
                    analysis["score"] += 6
                    analysis["details"].append(
                        f"Exceptional FCF yield {fcf_yield:.1%} - Pabrai sweet spot"
                    )
                elif fcf_yield > 0.07:  # 7-10% FCF yield
                    analysis["score"] += 4
                    analysis["details"].append(
                        f"Attractive FCF yield {fcf_yield:.1%} - good value"
                    )
                elif fcf_yield > 0.05:  # 5-7% FCF yield
                    analysis["score"] += 3
                    analysis["details"].append(
                        f"Reasonable FCF yield {fcf_yield:.1%} - fair value"
                    )
                elif fcf_yield > 0.03:  # 3-5% FCF yield
                    analysis["score"] += 1
                    analysis["details"].append(
                        f"Borderline FCF yield {fcf_yield:.1%} - limited upside"
                    )
                else:  # <3% FCF yield
                    analysis["details"].append(
                        f"Poor FCF yield {fcf_yield:.1%} - expensive"
                    )
            else:
                analysis["details"].append(
                    f"Negative normalized FCF ${normalized_fcf/1e6:.0f}M - avoid"
                )
        else:
            analysis["details"].append(
                "Insufficient FCF history for normalized yield calculation"
            )

        # Asset-Light Analysis (4 points max)
        capex_to_revenue_ratios = []
        for item in line_items:
            revenue = item.get("revenue")
            capex = abs(item.get("capital_expenditure") or 0)

            if revenue and revenue > 0:
                capex_to_revenue_ratios.append(capex / revenue)

        if capex_to_revenue_ratios:
            avg_capex_intensity = sum(capex_to_revenue_ratios) / len(
                capex_to_revenue_ratios
            )
            analysis["capex_intensity"] = avg_capex_intensity

            if avg_capex_intensity < 0.03:  # <3% of revenue
                analysis["score"] += 4
                analysis["asset_light_score"] = 4
                analysis["details"].append(
                    f"Highly asset-light - capex only {avg_capex_intensity:.1%} of revenue"
                )
            elif avg_capex_intensity < 0.05:  # 3-5% of revenue
                analysis["score"] += 3
                analysis["asset_light_score"] = 3
                analysis["details"].append(
                    f"Asset-light model - capex {avg_capex_intensity:.1%} of revenue"
                )
            elif avg_capex_intensity < 0.10:  # 5-10% of revenue
                analysis["score"] += 1
                analysis["asset_light_score"] = 1
                analysis["details"].append(
                    f"Moderate capex intensity {avg_capex_intensity:.1%}"
                )
            else:  # >10% of revenue
                analysis["asset_light_score"] = 0
                analysis["details"].append(
                    f"Capital intensive - high capex {avg_capex_intensity:.1%} of revenue"
                )
        else:
            analysis["details"].append(
                "Cannot calculate capex intensity - revenue data missing"
            )

        return analysis

    except Exception as e:
        return {
            "error": f"Pabrai valuation analysis failed: {str(e)}",
            "score": 0,
            "max_score": 10,
            "details": ["Error in valuation analysis"],
        }


def analyze_double_potential(
    financial_data: Annotated[
        Dict[str, Any],
        "Historical financial data for assessing potential to double investment",
    ],
) -> Annotated[
    Dict[str, Any],
    "Analysis of potential to double capital in 2-3 years through growth and rerating",
]:
    """
    Analyze the potential to double capital in 2-3 years using Pabrai's framework.
    Focus on sustainable growth in revenue and FCF plus potential for valuation rerating.

    Key factors:
    - Revenue growth trajectory and sustainability
    - Free cash flow growth trends
    - High FCF yield enabling doubling through retained cash/buybacks
    - Market rerating potential based on improving fundamentals
    """
    try:
        analysis = {
            "revenue_growth": None,
            "fcf_growth": None,
            "doubling_pathway": None,
            "score": 0,
            "max_score": 10,
            "details": [],
        }

        line_items = financial_data.get("line_items", [])
        market_cap = financial_data.get("market_cap")

        if not line_items:
            analysis["details"].append("No financial data for growth analysis")
            return analysis

        # Revenue Growth Analysis (3 points max)
        revenues = [
            item.get("revenue")
            for item in line_items
            if item.get("revenue") is not None
        ]

        if revenues and len(revenues) >= 3:
            recent_rev = sum(revenues[:3]) / 3  # Last 3 years average
            older_rev = sum(revenues[-3:]) / 3 if len(revenues) >= 6 else revenues[-1]

            if older_rev > 0:
                rev_growth = (recent_rev / older_rev) - 1
                analysis["revenue_growth"] = rev_growth

                if rev_growth > 0.15:  # >15% compound growth
                    analysis["score"] += 3
                    analysis["details"].append(
                        f"Strong revenue trajectory {rev_growth:.1%} CAGR"
                    )
                elif rev_growth > 0.05:  # 5-15% growth
                    analysis["score"] += 2
                    analysis["details"].append(
                        f"Modest revenue growth {rev_growth:.1%} CAGR"
                    )
                elif rev_growth > 0:  # Positive growth
                    analysis["score"] += 1
                    analysis["details"].append(f"Slow revenue growth {rev_growth:.1%}")
                else:
                    analysis["details"].append(f"Declining revenues {rev_growth:.1%}")
        else:
            analysis["details"].append(
                "Insufficient revenue history for growth analysis"
            )

        # FCF Growth Analysis (4 points max)
        fcf_values = [
            item.get("free_cash_flow")
            for item in line_items
            if item.get("free_cash_flow") is not None
        ]

        if fcf_values and len(fcf_values) >= 3:
            recent_fcf = sum(fcf_values[:3]) / 3
            older_fcf = (
                sum(fcf_values[-3:]) / 3 if len(fcf_values) >= 6 else fcf_values[-1]
            )

            if older_fcf != 0:
                fcf_growth = (recent_fcf / older_fcf) - 1
                analysis["fcf_growth"] = fcf_growth

                if fcf_growth > 0.20:  # >20% FCF growth
                    analysis["score"] += 4
                    analysis["details"].append(
                        f"Exceptional FCF growth {fcf_growth:.1%} - compounding machine"
                    )
                elif fcf_growth > 0.08:  # 8-20% FCF growth
                    analysis["score"] += 3
                    analysis["details"].append(f"Strong FCF growth {fcf_growth:.1%}")
                elif fcf_growth > 0:  # Positive FCF growth
                    analysis["score"] += 1
                    analysis["details"].append(f"Positive FCF growth {fcf_growth:.1%}")
                else:
                    analysis["details"].append(f"Declining FCF {fcf_growth:.1%}")
        else:
            analysis["details"].append("Insufficient FCF history for growth analysis")

        # High FCF Yield Doubling Potential (3 points max)
        if market_cap:
            # Get current FCF yield from valuation analysis
            val_analysis = analyze_pabrai_valuation(financial_data)
            fcf_yield = val_analysis.get("fcf_yield")

            if fcf_yield:
                analysis["current_fcf_yield"] = fcf_yield

                if fcf_yield > 0.08:  # >8% FCF yield
                    analysis["score"] += 3
                    years_to_double = 0.693 / fcf_yield  # Rule of 70
                    analysis["details"].append(
                        f"High FCF yield {fcf_yield:.1%} can double capital via buybacks/retained cash in {years_to_double:.1f} years"
                    )
                    analysis["doubling_pathway"] = "cash_generation"
                elif fcf_yield > 0.05:  # 5-8% FCF yield
                    analysis["score"] += 1
                    analysis["details"].append(
                        f"Moderate FCF yield {fcf_yield:.1%} supports gradual compounding"
                    )
                    analysis["doubling_pathway"] = "gradual_compounding"
                else:
                    analysis["details"].append(
                        f"Low FCF yield {fcf_yield:.1%} - doubling requires significant rerating"
                    )
                    analysis["doubling_pathway"] = "rerating_required"

        # Overall doubling assessment
        total_growth_score = analysis["score"]
        if total_growth_score >= 8:
            analysis["doubling_probability"] = "high"
            analysis["details"].append(
                "High probability of doubling in 2-3 years via multiple pathways"
            )
        elif total_growth_score >= 5:
            analysis["doubling_probability"] = "moderate"
            analysis["details"].append(
                "Moderate doubling potential - requires continued execution"
            )
        else:
            analysis["doubling_probability"] = "low"
            analysis["details"].append(
                "Limited doubling potential - significant rerating needed"
            )

        return analysis

    except Exception as e:
        return {
            "error": f"Double potential analysis failed: {str(e)}",
            "score": 0,
            "max_score": 10,
            "details": ["Error in doubling potential analysis"],
        }


def analyze_business_simplicity(
    financial_data: Annotated[
        Dict[str, Any],
        "Financial metrics for assessing business model simplicity and durability",
    ],
) -> Annotated[
    Dict[str, Any],
    "Analysis of business model simplicity and competitive moat sustainability",
]:
    """
    Analyze business simplicity and moat durability using Pabrai's preference for
    understandable, predictable businesses with sustainable competitive advantages.

    Key factors:
    - Margin consistency and predictability
    - Revenue and profit stability
    - Capital efficiency and ROIC trends
    - Simple business model indicators
    """
    try:
        analysis = {
            "margin_consistency": None,
            "revenue_stability": None,
            "roic_trend": None,
            "score": 0,
            "max_score": 8,
            "details": [],
        }

        line_items = financial_data.get("line_items", [])
        if not line_items:
            analysis["details"].append("No financial data for business analysis")
            return analysis

        # Margin Consistency Analysis (3 points max)
        gross_margins = []
        operating_margins = []

        for item in line_items:
            revenue = item.get("revenue")
            gross_profit = item.get("gross_profit")
            operating_income = item.get("operating_income")

            if revenue and revenue > 0:
                if gross_profit is not None:
                    gross_margins.append(gross_profit / revenue)
                if operating_income is not None:
                    operating_margins.append(operating_income / revenue)

        if gross_margins and len(gross_margins) >= 3:
            margin_volatility = max(gross_margins) - min(gross_margins)
            avg_margin = sum(gross_margins) / len(gross_margins)

            analysis["margin_consistency"] = {
                "avg_gross_margin": avg_margin,
                "margin_volatility": margin_volatility,
            }

            if (
                margin_volatility < 0.05 and avg_margin > 0.3
            ):  # <5% volatility, >30% margins
                analysis["score"] += 3
                analysis["details"].append(
                    f"Excellent margin stability - avg {avg_margin:.1%}, volatility {margin_volatility:.1%}"
                )
            elif (
                margin_volatility < 0.10 and avg_margin > 0.2
            ):  # <10% volatility, >20% margins
                analysis["score"] += 2
                analysis["details"].append(
                    f"Good margin consistency - avg {avg_margin:.1%}"
                )
            elif margin_volatility < 0.15:  # <15% volatility
                analysis["score"] += 1
                analysis["details"].append(
                    f"Acceptable margin stability - some volatility {margin_volatility:.1%}"
                )
            else:
                analysis["details"].append(
                    f"Volatile margins - high volatility {margin_volatility:.1%}"
                )
        else:
            analysis["details"].append(
                "Insufficient margin data for consistency analysis"
            )

        # Revenue Stability Analysis (2 points max)
        revenues = [item.get("revenue") for item in line_items if item.get("revenue")]

        if revenues and len(revenues) >= 5:
            revenue_declines = sum(
                1 for i in range(1, len(revenues)) if revenues[i] < revenues[i - 1]
            )
            decline_percentage = revenue_declines / (len(revenues) - 1)

            analysis["revenue_stability"] = {
                "decline_years": revenue_declines,
                "total_years": len(revenues) - 1,
                "decline_percentage": decline_percentage,
            }

            if decline_percentage <= 0.2:  # ≤20% of years with declines
                analysis["score"] += 2
                analysis["details"].append(
                    f"Highly stable revenue - only {decline_percentage:.0%} decline years"
                )
            elif decline_percentage <= 0.4:  # ≤40% of years with declines
                analysis["score"] += 1
                analysis["details"].append(
                    f"Moderately stable revenue - {decline_percentage:.0%} decline years"
                )
            else:
                analysis["details"].append(
                    f"Volatile revenue - {decline_percentage:.0%} years with declines"
                )

        # Capital Efficiency (ROIC Trend) (3 points max)
        roic_estimates = []
        for item in line_items:
            operating_income = item.get("operating_income")
            shareholders_equity = item.get("shareholders_equity")
            total_debt = item.get("total_debt") or 0

            if operating_income and shareholders_equity:
                invested_capital = shareholders_equity + total_debt
                if invested_capital > 0:
                    roic = operating_income / invested_capital
                    roic_estimates.append(roic)

        if roic_estimates and len(roic_estimates) >= 3:
            avg_roic = sum(roic_estimates) / len(roic_estimates)
            recent_roic = (
                sum(roic_estimates[:2]) / 2
                if len(roic_estimates) >= 2
                else roic_estimates[0]
            )

            analysis["roic_trend"] = {
                "avg_roic": avg_roic,
                "recent_roic": recent_roic,
                "improving": recent_roic > avg_roic,
            }

            if (
                avg_roic > 0.15 and recent_roic >= avg_roic
            ):  # >15% ROIC and stable/improving
                analysis["score"] += 3
                analysis["details"].append(
                    f"Excellent capital efficiency - ROIC {avg_roic:.1%}, improving trend"
                )
            elif avg_roic > 0.10:  # >10% ROIC
                analysis["score"] += 2
                analysis["details"].append(
                    f"Good capital efficiency - ROIC {avg_roic:.1%}"
                )
            elif avg_roic > 0.05:  # >5% ROIC
                analysis["score"] += 1
                analysis["details"].append(
                    f"Moderate capital efficiency - ROIC {avg_roic:.1%}"
                )
            else:
                analysis["details"].append(
                    f"Poor capital efficiency - ROIC {avg_roic:.1%}"
                )
        else:
            analysis["details"].append("Insufficient data for ROIC calculation")

        return analysis

    except Exception as e:
        return {
            "error": f"Business simplicity analysis failed: {str(e)}",
            "score": 0,
            "max_score": 8,
            "details": ["Error in business simplicity analysis"],
        }


def calculate_pabrai_score(
    analysis_results: Annotated[
        Dict[str, Any], "Combined analysis results from all Pabrai methodology tools"
    ],
) -> Annotated[
    Dict[str, Any],
    "Overall Pabrai investment score and 'heads I win, tails I don't lose much' assessment",
]:
    """
    Calculate overall Mohnish Pabrai investment score emphasizing his core philosophy:
    'Heads I win, tails I don't lose much' with focus on downside protection first.

    Scoring weights (reflecting Pabrai priorities):
    - Downside Protection: 45% weight (10/22.2 points equivalent)
    - Valuation (FCF yield): 35% weight (10/28.6 points equivalent)
    - Double Potential: 20% weight (10/50 points equivalent)

    Pabrai's high standards require strong scores across all dimensions for bullish signal.
    """
    try:
        # Extract individual analysis scores
        downside_analysis = analysis_results.get("downside_analysis", {})
        valuation_analysis = analysis_results.get("valuation_analysis", {})
        double_analysis = analysis_results.get("double_analysis", {})
        simplicity_analysis = analysis_results.get("simplicity_analysis", {})

        # Calculate weighted score based on Pabrai's priorities
        downside_score = downside_analysis.get("score", 0)  # max 10
        valuation_score = valuation_analysis.get("score", 0)  # max 10
        double_score = double_analysis.get("score", 0)  # max 10
        simplicity_score = simplicity_analysis.get("score", 0)  # max 8

        # Weighted calculation reflecting Pabrai's emphasis
        weighted_score = (
            downside_score * 0.45  # 45% weight on downside protection
            + valuation_score * 0.35  # 35% weight on valuation
            + double_score * 0.20  # 20% weight on doubling potential
        )

        max_weighted_score = 10.0  # Perfect weighted score
        score_percentage = (weighted_score / max_weighted_score) * 100

        # Pabrai's demanding criteria for signals
        if (
            score_percentage >= 80 and downside_score >= 7
        ):  # High bar + strong downside protection
            signal = "bullish"
            conviction = "high"
        elif (
            score_percentage >= 65 and downside_score >= 5
        ):  # Good score + adequate protection
            signal = "bullish"
            conviction = "moderate"
        elif (
            score_percentage <= 30 or downside_score <= 2
        ):  # Poor score or weak protection
            signal = "bearish"
            conviction = "high"
        else:  # Mixed signals
            signal = "neutral"
            conviction = "low"

        # Assess key Pabrai criteria
        strengths = []
        concerns = []
        checklist_items = []

        # Downside protection checklist
        if downside_score >= 8:
            strengths.append("Fortress balance sheet")
            checklist_items.append("✓ Excellent downside protection")
        elif downside_score >= 5:
            checklist_items.append("✓ Adequate downside protection")
        else:
            concerns.append("Weak downside protection")
            checklist_items.append("✗ Insufficient capital preservation")

        # Valuation checklist
        fcf_yield = valuation_analysis.get("fcf_yield")
        if fcf_yield and fcf_yield > 0.08:
            strengths.append("High FCF yield")
            checklist_items.append(f"✓ Attractive FCF yield {fcf_yield:.1%}")
        elif fcf_yield and fcf_yield > 0.05:
            checklist_items.append(f"✓ Reasonable FCF yield {fcf_yield:.1%}")
        else:
            concerns.append("Insufficient FCF yield")
            checklist_items.append("✗ Poor cash generation vs market cap")

        # Asset-light preference
        asset_light_score = valuation_analysis.get("asset_light_score", 0)
        if asset_light_score >= 3:
            strengths.append("Asset-light business model")
            checklist_items.append("✓ Asset-light model")
        elif asset_light_score >= 1:
            checklist_items.append("~ Moderate asset requirements")
        else:
            checklist_items.append("✗ Capital intensive model")

        # Doubling potential
        double_probability = double_analysis.get("doubling_probability")
        if double_probability == "high":
            strengths.append("Clear path to double in 2-3 years")
            checklist_items.append("✓ High doubling probability")
        elif double_probability == "moderate":
            checklist_items.append("✓ Moderate doubling potential")
        else:
            checklist_items.append("✗ Limited doubling prospects")

        # Business simplicity (if available)
        if simplicity_score >= 6:
            strengths.append("Simple, predictable business")
            checklist_items.append("✓ Simple business model")
        elif simplicity_score >= 3:
            checklist_items.append("~ Moderately complex business")
        else:
            checklist_items.append("✗ Complex or unpredictable business")

        # Overall Pabrai assessment
        analysis_summary = {
            "total_score": weighted_score,
            "max_score": max_weighted_score,
            "score_percentage": score_percentage,
            "signal": signal,
            "conviction": conviction,
            "strengths": strengths,
            "concerns": concerns,
            "pabrai_checklist": checklist_items,
            "component_scores": {
                "downside_protection": f"{downside_score:.1f}/10",
                "valuation_fcf_yield": f"{valuation_score:.1f}/10",
                "doubling_potential": f"{double_score:.1f}/10",
                "business_simplicity": (
                    f"{simplicity_score:.1f}/8" if simplicity_score > 0 else "N/A"
                ),
            },
            "key_metrics": {
                "fcf_yield": fcf_yield,
                "net_cash_position": downside_analysis.get("net_cash_position"),
                "debt_to_equity": downside_analysis.get("debt_to_equity"),
                "doubling_pathway": double_analysis.get("doubling_pathway"),
                "revenue_growth": double_analysis.get("revenue_growth"),
                "fcf_growth": double_analysis.get("fcf_growth"),
            },
            "pabrai_philosophy": {
                "heads_i_win": score_percentage >= 65
                and fcf_yield
                and fcf_yield > 0.05,
                "tails_i_dont_lose_much": downside_score >= 6,
                "meets_pabrai_criteria": score_percentage >= 65 and downside_score >= 6,
            },
        }

        return analysis_summary

    except Exception as e:
        return {
            "error": f"Pabrai score calculation failed: {str(e)}",
            "total_score": 0,
            "max_score": 10,
            "score_percentage": 0,
            "signal": "neutral",
            "conviction": "none",
            "pabrai_checklist": ["Error in analysis"],
        }
