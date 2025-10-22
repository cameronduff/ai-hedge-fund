from typing import Annotated, Dict, Any


def analyze_quality_fundamentals(
    financial_data: Annotated[
        Dict[str, Any],
        "Financial data for assessing company quality and fundamental strength",
    ],
) -> Annotated[
    Dict[str, Any],
    "Quality fundamentals analysis focusing on ROE, profitability consistency, and operational excellence",
]:
    """
    Analyze quality fundamentals using Rakesh Jhunjhunwala's emphasis on high-quality companies
    with consistent profitability, strong returns, and operational excellence.
    """
    try:
        analysis = {
            "roe_analysis": None,
            "profitability_trend": None,
            "score": 0,
            "max_score": 10,
            "details": [],
        }

        line_items = financial_data.get("line_items", [])
        if not line_items:
            analysis["details"].append("No financial data for quality analysis")
            return analysis

        # ROE Analysis (6 points max) - Jhunjhunwala's key metric
        net_incomes = [
            item.get("net_income") for item in line_items if item.get("net_income")
        ]
        total_assets = [
            item.get("total_assets") for item in line_items if item.get("total_assets")
        ]
        total_liabilities = [
            item.get("total_liabilities")
            for item in line_items
            if item.get("total_liabilities")
        ]

        if net_incomes and total_assets and total_liabilities:
            roe_values = []
            for i in range(
                min(len(net_incomes), len(total_assets), len(total_liabilities))
            ):
                if (
                    total_assets[i]
                    and total_liabilities[i]
                    and total_assets[i] > total_liabilities[i]
                    and net_incomes[i]
                ):
                    shareholders_equity = total_assets[i] - total_liabilities[i]
                    if shareholders_equity > 0:
                        roe = net_incomes[i] / shareholders_equity
                        roe_values.append(roe)

            if roe_values:
                recent_roe = roe_values[0]
                avg_roe = sum(roe_values) / len(roe_values)

                analysis["roe_analysis"] = {
                    "recent_roe": recent_roe,
                    "avg_roe": avg_roe,
                    "years_data": len(roe_values),
                }

                if avg_roe > 0.25:  # >25% ROE - exceptional
                    analysis["score"] += 6
                    analysis["details"].append(
                        f"Exceptional ROE {avg_roe:.1%} - Jhunjhunwala quality"
                    )
                elif avg_roe > 0.18:  # >18% ROE - target level
                    analysis["score"] += 5
                    analysis["details"].append(
                        f"Superior ROE {avg_roe:.1%} - high quality"
                    )
                elif avg_roe > 0.15:  # >15% ROE - good
                    analysis["score"] += 4
                    analysis["details"].append(
                        f"Good ROE {avg_roe:.1%} - solid returns"
                    )
                elif avg_roe > 0.10:  # 10-15% ROE - moderate
                    analysis["score"] += 2
                    analysis["details"].append(
                        f"Moderate ROE {avg_roe:.1%} - acceptable"
                    )
                else:
                    analysis["details"].append(
                        f"Low ROE {avg_roe:.1%} - below standards"
                    )

        # Profitability Consistency (4 points max)
        if len(net_incomes) >= 4:
            positive_years = sum(1 for income in net_incomes if income and income > 0)
            consistency_ratio = positive_years / len(net_incomes)

            analysis["profitability_trend"] = {
                "consistency_ratio": consistency_ratio,
                "positive_years": positive_years,
                "total_years": len(net_incomes),
            }

            if consistency_ratio >= 0.9:  # 90%+ profitable years
                analysis["score"] += 4
                analysis["details"].append("Excellent profitability consistency")
            elif consistency_ratio >= 0.75:  # 75%+ profitable years
                analysis["score"] += 3
                analysis["details"].append("Good profitability consistency")
            elif consistency_ratio >= 0.5:  # 50%+ profitable years
                analysis["score"] += 2
                analysis["details"].append("Moderate profitability consistency")
            else:
                analysis["details"].append("Poor profitability consistency")

        return analysis

    except Exception as e:
        return {
            "error": f"Quality analysis failed: {str(e)}",
            "score": 0,
            "max_score": 10,
            "details": ["Error in quality analysis"],
        }


def analyze_growth_sustainability(
    financial_data: Annotated[
        Dict[str, Any], "Financial data for evaluating growth sustainability and trends"
    ],
) -> Annotated[
    Dict[str, Any],
    "Growth sustainability analysis focusing on revenue and earnings compound growth rates",
]:
    """
    Analyze growth sustainability using Jhunjhunwala's focus on companies with
    consistent, compound growth in revenues and earnings over multiple years.
    """
    try:
        analysis = {
            "revenue_cagr": None,
            "earnings_cagr": None,
            "score": 0,
            "max_score": 10,
            "details": [],
        }

        line_items = financial_data.get("line_items", [])
        if not line_items:
            analysis["details"].append("No financial data for growth analysis")
            return analysis

        # Revenue Growth Analysis (6 points max)
        revenues = [
            item.get("revenue")
            for item in line_items
            if item.get("revenue") and item.get("revenue") > 0
        ]

        if len(revenues) >= 3:
            latest_rev = revenues[0]
            oldest_rev = revenues[-1]
            years = len(revenues) - 1

            revenue_cagr = (
                ((latest_rev / oldest_rev) ** (1 / years)) - 1 if oldest_rev > 0 else 0
            )
            analysis["revenue_cagr"] = revenue_cagr

            if revenue_cagr > 0.20:  # >20% CAGR - exceptional
                analysis["score"] += 6
                analysis["details"].append(
                    f"Exceptional revenue CAGR {revenue_cagr:.1%}"
                )
            elif revenue_cagr > 0.15:  # >15% CAGR - target level
                analysis["score"] += 5
                analysis["details"].append(f"Strong revenue CAGR {revenue_cagr:.1%}")
            elif revenue_cagr > 0.10:  # >10% CAGR - good
                analysis["score"] += 4
                analysis["details"].append(f"Good revenue CAGR {revenue_cagr:.1%}")
            elif revenue_cagr > 0.05:  # 5-10% CAGR - modest
                analysis["score"] += 2
                analysis["details"].append(f"Modest revenue CAGR {revenue_cagr:.1%}")
            else:
                analysis["details"].append(f"Weak revenue CAGR {revenue_cagr:.1%}")

        # Earnings Growth Analysis (4 points max)
        net_incomes = [
            item.get("net_income")
            for item in line_items
            if item.get("net_income") and item.get("net_income") > 0
        ]

        if len(net_incomes) >= 3:
            latest_income = net_incomes[0]
            oldest_income = net_incomes[-1]
            years = len(net_incomes) - 1

            earnings_cagr = (
                ((latest_income / oldest_income) ** (1 / years)) - 1
                if oldest_income > 0
                else 0
            )
            analysis["earnings_cagr"] = earnings_cagr

            if earnings_cagr > 0.25:  # >25% earnings CAGR
                analysis["score"] += 4
                analysis["details"].append(
                    f"Outstanding earnings CAGR {earnings_cagr:.1%}"
                )
            elif earnings_cagr > 0.15:  # >15% CAGR
                analysis["score"] += 3
                analysis["details"].append(f"Strong earnings CAGR {earnings_cagr:.1%}")
            elif earnings_cagr > 0.10:  # 10-15% CAGR
                analysis["score"] += 2
                analysis["details"].append(f"Good earnings CAGR {earnings_cagr:.1%}")
            elif earnings_cagr > 0.05:  # 5-10% CAGR
                analysis["score"] += 1
                analysis["details"].append(f"Modest earnings CAGR {earnings_cagr:.1%}")
            else:
                analysis["details"].append(f"Weak earnings CAGR {earnings_cagr:.1%}")

        return analysis

    except Exception as e:
        return {
            "error": f"Growth analysis failed: {str(e)}",
            "score": 0,
            "max_score": 10,
            "details": ["Error in growth analysis"],
        }


def analyze_balance_sheet_strength(
    financial_data: Annotated[
        Dict[str, Any],
        "Financial data for balance sheet strength and financial health assessment",
    ],
) -> Annotated[
    Dict[str, Any],
    "Balance sheet strength analysis focusing on debt levels, liquidity, and financial stability",
]:
    """
    Analyze balance sheet strength using Jhunjhunwala's preference for companies
    with strong balance sheets, manageable debt, and solid liquidity positions.
    """
    try:
        analysis = {
            "debt_analysis": None,
            "liquidity_analysis": None,
            "score": 0,
            "max_score": 8,
            "details": [],
        }

        line_items = financial_data.get("line_items", [])
        if not line_items:
            analysis["details"].append("No balance sheet data available")
            return analysis

        latest = line_items[0]

        # Debt Analysis (5 points max)
        total_assets = latest.get("total_assets")
        total_liabilities = latest.get("total_liabilities")

        if total_assets and total_liabilities:
            debt_to_assets = total_liabilities / total_assets

            analysis["debt_analysis"] = {
                "debt_to_assets": debt_to_assets,
                "total_assets": total_assets,
                "total_liabilities": total_liabilities,
            }

            if debt_to_assets < 0.3:  # Very conservative
                analysis["score"] += 5
                analysis["details"].append(
                    f"Excellent debt position - {debt_to_assets:.1%}"
                )
            elif debt_to_assets < 0.4:  # Conservative - Jhunjhunwala target
                analysis["score"] += 4
                analysis["details"].append(
                    f"Strong debt position - {debt_to_assets:.1%}"
                )
            elif debt_to_assets < 0.5:  # Moderate
                analysis["score"] += 3
                analysis["details"].append(
                    f"Acceptable debt position - {debt_to_assets:.1%}"
                )
            elif debt_to_assets < 0.6:  # Higher but manageable
                analysis["score"] += 2
                analysis["details"].append(
                    f"Moderate debt concern - {debt_to_assets:.1%}"
                )
            else:  # High debt
                analysis["details"].append(f"High debt concern - {debt_to_assets:.1%}")

        # Liquidity Analysis (3 points max)
        current_assets = latest.get("current_assets")
        current_liabilities = latest.get("current_liabilities")

        if current_assets and current_liabilities and current_liabilities > 0:
            current_ratio = current_assets / current_liabilities

            analysis["liquidity_analysis"] = {
                "current_ratio": current_ratio,
                "current_assets": current_assets,
                "current_liabilities": current_liabilities,
            }

            if current_ratio > 2.0:  # Strong liquidity
                analysis["score"] += 3
                analysis["details"].append(
                    f"Strong liquidity - current ratio {current_ratio:.2f}"
                )
            elif current_ratio > 1.5:  # Good liquidity
                analysis["score"] += 2
                analysis["details"].append(
                    f"Good liquidity - current ratio {current_ratio:.2f}"
                )
            elif current_ratio > 1.0:  # Adequate liquidity
                analysis["score"] += 1
                analysis["details"].append(
                    f"Adequate liquidity - current ratio {current_ratio:.2f}"
                )
            else:
                analysis["details"].append(
                    f"Liquidity concern - current ratio {current_ratio:.2f}"
                )

        return analysis

    except Exception as e:
        return {
            "error": f"Balance sheet analysis failed: {str(e)}",
            "score": 0,
            "max_score": 8,
            "details": ["Error in balance sheet analysis"],
        }


def analyze_cash_flow_quality(
    financial_data: Annotated[
        Dict[str, Any],
        "Financial data for cash flow quality and shareholder value creation assessment",
    ],
) -> Annotated[
    Dict[str, Any],
    "Cash flow quality analysis focusing on free cash flow generation and shareholder distributions",
]:
    """
    Analyze cash flow quality using Jhunjhunwala's focus on companies that generate
    strong free cash flows and reward shareholders through dividends and buybacks.
    """
    try:
        analysis = {
            "fcf_analysis": None,
            "shareholder_returns": None,
            "score": 0,
            "max_score": 8,
            "details": [],
        }

        line_items = financial_data.get("line_items", [])
        if not line_items:
            analysis["details"].append("No cash flow data available")
            return analysis

        latest = line_items[0]

        # Free Cash Flow Analysis (5 points max)
        free_cash_flow = latest.get("free_cash_flow")
        net_income = latest.get("net_income")

        if free_cash_flow is not None:
            analysis["fcf_analysis"] = {
                "free_cash_flow": free_cash_flow,
                "fcf_positive": free_cash_flow > 0,
            }

            if free_cash_flow > 0:
                analysis["score"] += 3
                analysis["details"].append(
                    f"Positive free cash flow: ${free_cash_flow/1e6:.0f}M"
                )

                # FCF quality relative to income
                if net_income and net_income > 0:
                    fcf_conversion = free_cash_flow / net_income
                    if fcf_conversion > 1.0:
                        analysis["score"] += 2
                        analysis["details"].append(
                            f"Excellent FCF conversion {fcf_conversion:.1f}x"
                        )
                    elif fcf_conversion > 0.8:
                        analysis["score"] += 1
                        analysis["details"].append(
                            f"Good FCF conversion {fcf_conversion:.1f}x"
                        )
            else:
                analysis["details"].append(
                    f"Negative free cash flow: ${free_cash_flow/1e6:.0f}M"
                )

        # Shareholder Returns (3 points max)
        dividends = latest.get("dividends_and_other_cash_distributions")
        share_buybacks = latest.get("issuance_or_purchase_of_equity_shares")

        shareholder_friendly_actions = 0

        # Dividend payments (negative indicates cash outflow for dividends)
        if dividends and dividends < 0:
            shareholder_friendly_actions += 1
            analysis["details"].append(f"Pays dividends - ${abs(dividends)/1e6:.0f}M")

        # Share buybacks (negative indicates repurchases)
        if share_buybacks and share_buybacks < 0:
            shareholder_friendly_actions += 1
            analysis["details"].append(
                f"Share buybacks - ${abs(share_buybacks)/1e6:.0f}M"
            )

        analysis["shareholder_returns"] = {
            "pays_dividends": dividends and dividends < 0,
            "share_buybacks": share_buybacks and share_buybacks < 0,
            "shareholder_friendly_actions": shareholder_friendly_actions,
        }

        if shareholder_friendly_actions >= 2:
            analysis["score"] += 3
            analysis["details"].append("Multiple shareholder-friendly actions")
        elif shareholder_friendly_actions >= 1:
            analysis["score"] += 2
            analysis["details"].append("Some shareholder returns evident")
        else:
            analysis["details"].append("Limited shareholder return mechanisms")

        return analysis

    except Exception as e:
        return {
            "error": f"Cash flow analysis failed: {str(e)}",
            "score": 0,
            "max_score": 8,
            "details": ["Error in cash flow analysis"],
        }


def calculate_jhunjhunwala_score(
    analysis_results: Annotated[
        Dict[str, Any],
        "Combined analysis results from all Jhunjhunwala methodology tools",
    ],
) -> Annotated[
    Dict[str, Any],
    "Overall Rakesh Jhunjhunwala investment score emphasizing quality, growth, and value",
]:
    """
    Calculate overall Rakesh Jhunjhunwala investment score emphasizing his focus on
    high-quality companies with strong growth, solid balance sheets, and attractive valuations.
    """
    try:
        # Extract individual analysis scores
        quality_analysis = analysis_results.get("quality_analysis", {})
        growth_analysis = analysis_results.get("growth_analysis", {})
        balance_sheet_analysis = analysis_results.get("balance_sheet_analysis", {})
        cash_flow_analysis = analysis_results.get("cash_flow_analysis", {})

        # Calculate weighted score based on Jhunjhunwala's priorities
        quality_score = quality_analysis.get("score", 0)  # max 10
        growth_score = growth_analysis.get("score", 0)  # max 10
        balance_sheet_score = balance_sheet_analysis.get("score", 0)  # max 8
        cash_flow_score = cash_flow_analysis.get("score", 0)  # max 8

        # Weighted calculation reflecting Jhunjhunwala's emphasis
        weighted_score = (
            (quality_score / 10) * 35  # 35% weight on quality fundamentals
            + (growth_score / 10) * 30  # 30% weight on growth sustainability
            + (balance_sheet_score / 8) * 20  # 20% weight on balance sheet strength
            + (cash_flow_score / 8) * 15  # 15% weight on cash flow quality
        )

        score_percentage = weighted_score

        # Jhunjhunwala's criteria for investment signals
        avg_roe = quality_analysis.get("roe_analysis", {}).get("avg_roe")
        revenue_cagr = growth_analysis.get("revenue_cagr")
        debt_to_assets = balance_sheet_analysis.get("debt_analysis", {}).get(
            "debt_to_assets"
        )

        # Signal determination with Jhunjhunwala's demanding standards
        if (
            score_percentage >= 80
            and avg_roe
            and avg_roe > 0.18
            and revenue_cagr
            and revenue_cagr > 0.15
        ):
            signal = "bullish"
            conviction = "high"
        elif score_percentage >= 70 and (
            (avg_roe and avg_roe > 0.15) or (revenue_cagr and revenue_cagr > 0.12)
        ):
            signal = "bullish"
            conviction = "moderate"
        elif (
            score_percentage <= 35
            or (avg_roe and avg_roe < 0.08)
            or (debt_to_assets and debt_to_assets > 0.6)
        ):
            signal = "bearish"
            conviction = "high"
        else:
            signal = "neutral"
            conviction = "low"

        # Assess key Jhunjhunwala criteria
        strengths = []
        concerns = []
        jhunjhunwala_checklist = []

        # Quality assessment
        if avg_roe and avg_roe > 0.20:
            strengths.append("Exceptional ROE performance")
            jhunjhunwala_checklist.append(f"✓ Superior ROE {avg_roe:.1%}")
        elif avg_roe and avg_roe > 0.15:
            jhunjhunwala_checklist.append(f"✓ Strong ROE {avg_roe:.1%}")
        else:
            concerns.append("Insufficient ROE performance")
            jhunjhunwala_checklist.append("✗ Below-standard ROE")

        # Growth assessment
        if revenue_cagr and revenue_cagr > 0.15:
            strengths.append("Strong revenue growth")
            jhunjhunwala_checklist.append(
                f"✓ Excellent revenue CAGR {revenue_cagr:.1%}"
            )
        elif revenue_cagr and revenue_cagr > 0.10:
            jhunjhunwala_checklist.append(f"✓ Good revenue CAGR {revenue_cagr:.1%}")
        else:
            concerns.append("Weak growth trajectory")
            jhunjhunwala_checklist.append("✗ Insufficient growth")

        # Balance sheet assessment
        if debt_to_assets and debt_to_assets < 0.4:
            strengths.append("Conservative balance sheet")
            jhunjhunwala_checklist.append("✓ Strong balance sheet")
        elif debt_to_assets and debt_to_assets < 0.5:
            jhunjhunwala_checklist.append("✓ Adequate balance sheet")
        else:
            concerns.append("Balance sheet concerns")
            jhunjhunwala_checklist.append("✗ High debt levels")

        # Cash flow assessment
        fcf_positive = cash_flow_analysis.get("fcf_analysis", {}).get(
            "fcf_positive", False
        )
        if fcf_positive:
            strengths.append("Positive free cash flow")
            jhunjhunwala_checklist.append("✓ Strong cash generation")
        else:
            concerns.append("Cash flow concerns")
            jhunjhunwala_checklist.append("✗ Negative free cash flow")

        # Overall assessment
        analysis_summary = {
            "total_score": weighted_score,
            "max_score": 100,
            "score_percentage": score_percentage,
            "signal": signal,
            "conviction": conviction,
            "strengths": strengths,
            "concerns": concerns,
            "jhunjhunwala_checklist": jhunjhunwala_checklist,
            "component_scores": {
                "quality_fundamentals": f"{quality_score:.1f}/10",
                "growth_sustainability": f"{growth_score:.1f}/10",
                "balance_sheet_strength": f"{balance_sheet_score:.1f}/8",
                "cash_flow_quality": f"{cash_flow_score:.1f}/8",
            },
            "key_metrics": {
                "avg_roe": avg_roe,
                "revenue_cagr": revenue_cagr,
                "debt_to_assets": debt_to_assets,
                "fcf_positive": fcf_positive,
            },
            "jhunjhunwala_philosophy": {
                "quality_company": avg_roe and avg_roe > 0.15,
                "growth_trajectory": revenue_cagr and revenue_cagr > 0.10,
                "conservative_balance_sheet": debt_to_assets and debt_to_assets < 0.5,
                "meets_jhunjhunwala_criteria": (
                    score_percentage >= 70
                    and avg_roe
                    and avg_roe > 0.15
                    and revenue_cagr
                    and revenue_cagr > 0.10
                ),
            },
        }

        return analysis_summary

    except Exception as e:
        return {
            "error": f"Jhunjhunwala score calculation failed: {str(e)}",
            "total_score": 0,
            "max_score": 100,
            "score_percentage": 0,
            "signal": "neutral",
            "conviction": "none",
            "jhunjhunwala_checklist": ["Error in analysis"],
        }
