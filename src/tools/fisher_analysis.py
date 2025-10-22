from typing import Annotated, Dict, Any, Optional, List
import statistics


def analyze_growth_quality_metrics(
    financial_data: Annotated[
        Dict[str, Any],
        "Financial data for assessing long-term growth quality and sustainability",
    ],
) -> Annotated[
    Dict[str, Any],
    "Growth quality analysis focusing on revenue consistency, earnings power, and R&D investment",
]:
    """
    Analyze growth quality using Phil Fisher's emphasis on sustained, above-average growth potential
    driven by superior management and consistent innovation investment.

    Key factors:
    - Consistent revenue growth over multiple years (CAGR analysis)
    - Earnings per share growth sustainability and quality
    - R&D investment as percentage of revenue for future growth
    - Growth consistency and predictability over business cycles
    """
    try:
        analysis = {
            "revenue_cagr": None,
            "eps_cagr": None,
            "rnd_investment_ratio": None,
            "growth_consistency": None,
            "score": 0,
            "max_score": 10,
            "details": [],
        }

        line_items = financial_data.get("line_items", [])
        if not line_items:
            analysis["details"].append("No financial data for growth quality analysis")
            return analysis

        # Revenue Growth Analysis (3 points max)
        revenues = [item.get("revenue") for item in line_items if item.get("revenue")]
        if len(revenues) >= 3:
            latest_rev = revenues[0]
            oldest_rev = revenues[-1]
            years = len(revenues) - 1

            if oldest_rev and oldest_rev > 0 and latest_rev and latest_rev > 0:
                revenue_cagr = ((latest_rev / oldest_rev) ** (1 / years)) - 1
                analysis["revenue_cagr"] = revenue_cagr

                if revenue_cagr > 0.20:  # >20% CAGR - exceptional growth
                    analysis["score"] += 3
                    analysis["details"].append(
                        f"Exceptional revenue CAGR {revenue_cagr:.1%} - superior growth company"
                    )
                elif revenue_cagr > 0.12:  # 12-20% CAGR - strong growth
                    analysis["score"] += 2.5
                    analysis["details"].append(
                        f"Strong revenue CAGR {revenue_cagr:.1%} - above-average growth"
                    )
                elif revenue_cagr > 0.08:  # 8-12% CAGR - moderate growth
                    analysis["score"] += 2
                    analysis["details"].append(
                        f"Solid revenue CAGR {revenue_cagr:.1%} - consistent growth"
                    )
                elif revenue_cagr > 0.03:  # 3-8% CAGR - modest growth
                    analysis["score"] += 1
                    analysis["details"].append(
                        f"Modest revenue CAGR {revenue_cagr:.1%} - below Fisher standards"
                    )
                else:
                    analysis["details"].append(
                        f"Poor revenue CAGR {revenue_cagr:.1%} - insufficient growth"
                    )
            else:
                analysis["details"].append(
                    "Cannot calculate revenue CAGR - invalid data points"
                )
        else:
            analysis["details"].append(
                "Insufficient revenue history for CAGR calculation"
            )

        # EPS Growth Analysis (3 points max)
        eps_values = [
            item.get("earnings_per_share")
            for item in line_items
            if item.get("earnings_per_share")
        ]
        if len(eps_values) >= 3:
            # Filter out negative EPS for CAGR calculation
            positive_eps = [
                (i, eps) for i, eps in enumerate(eps_values) if eps and eps > 0
            ]

            if len(positive_eps) >= 2:
                latest_eps = positive_eps[0][1]
                oldest_eps = positive_eps[-1][1]
                years_between = positive_eps[0][0] - positive_eps[-1][0]

                if years_between > 0:
                    eps_cagr = ((latest_eps / oldest_eps) ** (1 / years_between)) - 1
                    analysis["eps_cagr"] = eps_cagr

                    if eps_cagr > 0.20:  # >20% EPS CAGR
                        analysis["score"] += 3
                        analysis["details"].append(
                            f"Exceptional EPS CAGR {eps_cagr:.1%} - superior earnings power"
                        )
                    elif eps_cagr > 0.15:  # 15-20% EPS CAGR
                        analysis["score"] += 2.5
                        analysis["details"].append(
                            f"Strong EPS CAGR {eps_cagr:.1%} - excellent earnings growth"
                        )
                    elif eps_cagr > 0.10:  # 10-15% EPS CAGR
                        analysis["score"] += 2
                        analysis["details"].append(
                            f"Good EPS CAGR {eps_cagr:.1%} - solid earnings expansion"
                        )
                    elif eps_cagr > 0.05:  # 5-10% EPS CAGR
                        analysis["score"] += 1
                        analysis["details"].append(
                            f"Modest EPS CAGR {eps_cagr:.1%} - below Fisher target"
                        )
                    else:
                        analysis["details"].append(
                            f"Poor EPS CAGR {eps_cagr:.1%} - inadequate earnings growth"
                        )
            else:
                analysis["details"].append(
                    "Insufficient positive EPS data for growth calculation"
                )
        else:
            analysis["details"].append("Insufficient EPS history for growth analysis")

        # R&D Investment Analysis (2 points max)
        rnd_values = [
            item.get("research_and_development")
            for item in line_items
            if item.get("research_and_development")
        ]

        if rnd_values and revenues:
            # Calculate R&D as percentage of revenue (most recent)
            recent_rnd = rnd_values[0] if rnd_values[0] else 0
            recent_revenue = revenues[0] if revenues[0] else 1

            rnd_ratio = recent_rnd / recent_revenue if recent_revenue > 0 else 0
            analysis["rnd_investment_ratio"] = rnd_ratio

            if rnd_ratio >= 0.10:  # 10%+ R&D - heavy innovation investment
                analysis["score"] += 2
                analysis["details"].append(
                    f"Exceptional R&D investment {rnd_ratio:.1%} - strong innovation focus"
                )
            elif rnd_ratio >= 0.05:  # 5-10% R&D - good innovation
                analysis["score"] += 1.5
                analysis["details"].append(
                    f"Strong R&D investment {rnd_ratio:.1%} - future growth potential"
                )
            elif rnd_ratio >= 0.03:  # 3-5% R&D - moderate innovation
                analysis["score"] += 1
                analysis["details"].append(
                    f"Moderate R&D investment {rnd_ratio:.1%} - some innovation"
                )
            elif rnd_ratio > 0:  # <3% R&D - minimal innovation
                analysis["score"] += 0.5
                analysis["details"].append(
                    f"Low R&D investment {rnd_ratio:.1%} - limited innovation"
                )
            else:
                analysis["details"].append(
                    "No R&D investment reported - potential concern for future growth"
                )
        else:
            analysis["details"].append(
                "R&D data unavailable - cannot assess innovation investment"
            )

        # Growth Consistency Analysis (2 points max)
        if len(revenues) >= 4:
            # Calculate year-over-year growth rates
            growth_rates = []
            for i in range(1, len(revenues)):
                if revenues[i] and revenues[i] > 0:
                    yoy_growth = (revenues[i - 1] / revenues[i]) - 1
                    growth_rates.append(yoy_growth)

            if len(growth_rates) >= 3:
                # Calculate consistency (lower standard deviation = more consistent)
                avg_growth = sum(growth_rates) / len(growth_rates)
                growth_volatility = (
                    statistics.pstdev(growth_rates) if len(growth_rates) > 1 else 0
                )

                analysis["growth_consistency"] = {
                    "avg_growth": avg_growth,
                    "volatility": growth_volatility,
                    "consistent_positive": sum(1 for g in growth_rates if g > 0),
                }

                if (
                    growth_volatility < 0.05 and avg_growth > 0.08
                ):  # Low volatility + good growth
                    analysis["score"] += 2
                    analysis["details"].append(
                        f"Excellent growth consistency - volatility {growth_volatility:.1%}"
                    )
                elif (
                    growth_volatility < 0.10 and avg_growth > 0.05
                ):  # Moderate consistency
                    analysis["score"] += 1.5
                    analysis["details"].append(
                        f"Good growth consistency - volatility {growth_volatility:.1%}"
                    )
                elif avg_growth > 0:  # Positive but volatile
                    analysis["score"] += 1
                    analysis["details"].append(
                        f"Growth positive but volatile - volatility {growth_volatility:.1%}"
                    )
                else:
                    analysis["details"].append(
                        "Inconsistent or negative growth pattern"
                    )

        return analysis

    except Exception as e:
        return {
            "error": f"Growth quality analysis failed: {str(e)}",
            "score": 0,
            "max_score": 10,
            "details": ["Error in growth quality analysis"],
        }


def analyze_management_excellence(
    financial_data: Annotated[
        Dict[str, Any],
        "Financial data for evaluating management quality and capital allocation efficiency",
    ],
) -> Annotated[
    Dict[str, Any],
    "Management excellence analysis focusing on ROE, capital efficiency, and operational leverage",
]:
    """
    Analyze management excellence using Phil Fisher's focus on superior management teams
    that effectively deploy capital and create long-term shareholder value.

    Key factors:
    - Return on Equity (ROE) trends and sustainability
    - Capital allocation efficiency and reinvestment returns
    - Operating leverage and margin expansion capability
    - Balance sheet management and financial discipline
    """
    try:
        analysis = {
            "roe_trend": None,
            "capital_efficiency": None,
            "operating_leverage": None,
            "financial_discipline": None,
            "score": 0,
            "max_score": 10,
            "details": [],
        }

        line_items = financial_data.get("line_items", [])
        if not line_items:
            analysis["details"].append("No financial data for management analysis")
            return analysis

        # ROE Analysis and Trends (3 points max)
        net_incomes = [
            item.get("net_income") for item in line_items if item.get("net_income")
        ]
        equities = [
            item.get("shareholders_equity")
            for item in line_items
            if item.get("shareholders_equity")
        ]

        if net_incomes and equities and len(net_incomes) == len(equities):
            roe_values = []
            for i in range(min(len(net_incomes), len(equities))):
                if equities[i] and equities[i] > 0 and net_incomes[i]:
                    roe = net_incomes[i] / equities[i]
                    roe_values.append(roe)

            if len(roe_values) >= 2:
                recent_roe = roe_values[0]
                avg_roe = sum(roe_values) / len(roe_values)
                roe_trend = recent_roe - roe_values[-1] if len(roe_values) > 1 else 0

                analysis["roe_trend"] = {
                    "recent_roe": recent_roe,
                    "avg_roe": avg_roe,
                    "trend": roe_trend,
                }

                if avg_roe > 0.20 and roe_trend >= 0:  # >20% ROE + stable/improving
                    analysis["score"] += 3
                    analysis["details"].append(
                        f"Exceptional ROE {avg_roe:.1%} with positive trend - superior management"
                    )
                elif avg_roe > 0.15 and recent_roe > 0.12:  # >15% average, >12% recent
                    analysis["score"] += 2.5
                    analysis["details"].append(
                        f"Strong ROE {avg_roe:.1%} - excellent capital efficiency"
                    )
                elif avg_roe > 0.10:  # >10% ROE
                    analysis["score"] += 2
                    analysis["details"].append(
                        f"Good ROE {avg_roe:.1%} - solid management performance"
                    )
                elif avg_roe > 0.05:  # 5-10% ROE
                    analysis["score"] += 1
                    analysis["details"].append(
                        f"Modest ROE {avg_roe:.1%} - below Fisher standards"
                    )
                else:
                    analysis["details"].append(
                        f"Poor ROE {avg_roe:.1%} - management effectiveness concerns"
                    )
        else:
            analysis["details"].append("Insufficient data for ROE calculation")

        # Operating Leverage Analysis (2.5 points max)
        revenues = [item.get("revenue") for item in line_items if item.get("revenue")]
        operating_incomes = [
            item.get("operating_income")
            for item in line_items
            if item.get("operating_income")
        ]

        if len(revenues) >= 2 and len(operating_incomes) >= 2:
            # Calculate operating leverage (% change in operating income / % change in revenue)
            rev_change = (revenues[0] / revenues[1] - 1) if revenues[1] > 0 else 0
            op_change = (
                (operating_incomes[0] / operating_incomes[1] - 1)
                if operating_incomes[1] and operating_incomes[1] != 0
                else 0
            )

            if rev_change > 0.01:  # At least 1% revenue growth
                operating_leverage = op_change / rev_change if rev_change != 0 else 0

                analysis["operating_leverage"] = {
                    "revenue_change": rev_change,
                    "operating_income_change": op_change,
                    "leverage_ratio": operating_leverage,
                }

                if operating_leverage > 1.5:  # Strong operating leverage
                    analysis["score"] += 2.5
                    analysis["details"].append(
                        f"Excellent operating leverage {operating_leverage:.1f}x - scalable business model"
                    )
                elif operating_leverage > 1.0:  # Positive operating leverage
                    analysis["score"] += 2
                    analysis["details"].append(
                        f"Good operating leverage {operating_leverage:.1f}x - efficient scaling"
                    )
                elif operating_leverage > 0.5:  # Moderate leverage
                    analysis["score"] += 1
                    analysis["details"].append(
                        f"Moderate operating leverage {operating_leverage:.1f}x"
                    )
                else:
                    analysis["details"].append(
                        f"Weak operating leverage {operating_leverage:.1f}x - scaling concerns"
                    )
        else:
            analysis["details"].append(
                "Insufficient data for operating leverage analysis"
            )

        # Financial Discipline Analysis (2.5 points max)
        debts = [
            item.get("total_debt")
            for item in line_items
            if item.get("total_debt") is not None
        ]
        cash_values = [
            item.get("cash_and_equivalents")
            for item in line_items
            if item.get("cash_and_equivalents")
        ]

        if debts and equities and cash_values:
            recent_debt = debts[0] if debts[0] else 0
            recent_equity = equities[0] if equities[0] else 1
            recent_cash = cash_values[0] if cash_values[0] else 0

            debt_to_equity = (
                recent_debt / recent_equity if recent_equity > 0 else float("inf")
            )
            net_cash_position = recent_cash - recent_debt

            analysis["financial_discipline"] = {
                "debt_to_equity": debt_to_equity,
                "net_cash_position": net_cash_position,
                "cash_coverage": (
                    recent_cash / recent_debt if recent_debt > 0 else float("inf")
                ),
            }

            if debt_to_equity < 0.2 or net_cash_position > 0:  # Very conservative
                analysis["score"] += 2.5
                analysis["details"].append(
                    f"Excellent financial discipline - conservative capital structure"
                )
            elif debt_to_equity < 0.5:  # Moderate leverage
                analysis["score"] += 2
                analysis["details"].append(
                    f"Good financial discipline - D/E {debt_to_equity:.2f}"
                )
            elif debt_to_equity < 1.0:  # Reasonable leverage
                analysis["score"] += 1
                analysis["details"].append(
                    f"Acceptable leverage - D/E {debt_to_equity:.2f}"
                )
            else:
                analysis["details"].append(
                    f"High leverage concerns - D/E {debt_to_equity:.2f}"
                )
        else:
            analysis["details"].append(
                "Insufficient data for financial discipline analysis"
            )

        # Free Cash Flow Generation (2 points max)
        fcf_values = [
            item.get("free_cash_flow")
            for item in line_items
            if item.get("free_cash_flow") is not None
        ]

        if fcf_values and net_incomes:
            # FCF conversion rate and consistency
            fcf_conversion_rates = []
            for i in range(min(len(fcf_values), len(net_incomes))):
                if net_incomes[i] and net_incomes[i] > 0:
                    conversion = fcf_values[i] / net_incomes[i]
                    fcf_conversion_rates.append(conversion)

            if fcf_conversion_rates:
                avg_conversion = sum(fcf_conversion_rates) / len(fcf_conversion_rates)
                positive_fcf_years = sum(1 for fcf in fcf_values if fcf > 0)

                if avg_conversion > 1.0 and positive_fcf_years == len(fcf_values):
                    analysis["score"] += 2
                    analysis["details"].append(
                        f"Excellent FCF generation - {avg_conversion:.1f}x conversion rate"
                    )
                elif (
                    avg_conversion > 0.8 and positive_fcf_years >= len(fcf_values) * 0.8
                ):
                    analysis["score"] += 1.5
                    analysis["details"].append(
                        f"Strong FCF generation - {avg_conversion:.1f}x conversion"
                    )
                elif avg_conversion > 0.5:
                    analysis["score"] += 1
                    analysis["details"].append(
                        f"Adequate FCF generation - {avg_conversion:.1f}x conversion"
                    )
                else:
                    analysis["details"].append(
                        f"Weak FCF conversion - {avg_conversion:.1f}x rate"
                    )

        return analysis

    except Exception as e:
        return {
            "error": f"Management excellence analysis failed: {str(e)}",
            "score": 0,
            "max_score": 10,
            "details": ["Error in management excellence analysis"],
        }


def analyze_profit_margins_stability(
    financial_data: Annotated[
        Dict[str, Any],
        "Financial data for analyzing profit margin trends and operational stability",
    ],
) -> Annotated[
    Dict[str, Any],
    "Profit margin analysis focusing on consistency, improvement trends, and competitive positioning",
]:
    """
    Analyze profit margin stability and trends using Fisher's emphasis on companies
    with sustainable competitive advantages reflected in consistent, superior margins.

    Key factors:
    - Gross margin levels and stability over time
    - Operating margin trends and improvement capability
    - Net margin efficiency and consistency
    - Margin resilience during different business cycles
    """
    try:
        analysis = {
            "gross_margin_analysis": None,
            "operating_margin_analysis": None,
            "net_margin_analysis": None,
            "margin_stability": None,
            "score": 0,
            "max_score": 8,
            "details": [],
        }

        line_items = financial_data.get("line_items", [])
        if not line_items:
            analysis["details"].append("No financial data for margin analysis")
            return analysis

        # Gross Margin Analysis (2.5 points max)
        gross_margins = [
            item.get("gross_margin")
            for item in line_items
            if item.get("gross_margin") is not None
        ]

        if gross_margins:
            recent_gm = gross_margins[0]
            avg_gm = sum(gross_margins) / len(gross_margins)
            gm_trend = recent_gm - gross_margins[-1] if len(gross_margins) > 1 else 0

            analysis["gross_margin_analysis"] = {
                "recent_margin": recent_gm,
                "avg_margin": avg_gm,
                "trend": gm_trend,
            }

            if avg_gm > 0.60 and gm_trend >= 0:  # >60% gross margin + stable/improving
                analysis["score"] += 2.5
                analysis["details"].append(
                    f"Exceptional gross margins {avg_gm:.1%} - strong pricing power"
                )
            elif avg_gm > 0.40 and recent_gm > 0.35:  # >40% average, >35% recent
                analysis["score"] += 2
                analysis["details"].append(
                    f"Strong gross margins {avg_gm:.1%} - good competitive position"
                )
            elif avg_gm > 0.25:  # >25% gross margin
                analysis["score"] += 1.5
                analysis["details"].append(f"Decent gross margins {avg_gm:.1%}")
            elif avg_gm > 0.15:  # 15-25% gross margin
                analysis["score"] += 1
                analysis["details"].append(f"Modest gross margins {avg_gm:.1%}")
            else:
                analysis["details"].append(
                    f"Low gross margins {avg_gm:.1%} - competitive pressure"
                )
        else:
            analysis["details"].append("No gross margin data available")

        # Operating Margin Analysis (2.5 points max)
        operating_margins = [
            item.get("operating_margin")
            for item in line_items
            if item.get("operating_margin") is not None
        ]

        if operating_margins:
            recent_om = operating_margins[0]
            avg_om = sum(operating_margins) / len(operating_margins)
            om_trend = (
                recent_om - operating_margins[-1] if len(operating_margins) > 1 else 0
            )

            analysis["operating_margin_analysis"] = {
                "recent_margin": recent_om,
                "avg_margin": avg_om,
                "trend": om_trend,
            }

            if avg_om > 0.25 and om_trend >= 0:  # >25% operating margin + improving
                analysis["score"] += 2.5
                analysis["details"].append(
                    f"Exceptional operating margins {avg_om:.1%} - superior efficiency"
                )
            elif avg_om > 0.15 and recent_om > 0.12:  # >15% average, >12% recent
                analysis["score"] += 2
                analysis["details"].append(
                    f"Strong operating margins {avg_om:.1%} - efficient operations"
                )
            elif avg_om > 0.08:  # >8% operating margin
                analysis["score"] += 1.5
                analysis["details"].append(f"Good operating margins {avg_om:.1%}")
            elif avg_om > 0.03:  # 3-8% operating margin
                analysis["score"] += 1
                analysis["details"].append(f"Modest operating margins {avg_om:.1%}")
            else:
                analysis["details"].append(
                    f"Poor operating margins {avg_om:.1%} - operational concerns"
                )
        else:
            analysis["details"].append("No operating margin data available")

        # Net Margin Analysis (1.5 points max)
        revenues = [item.get("revenue") for item in line_items if item.get("revenue")]
        net_incomes = [
            item.get("net_income") for item in line_items if item.get("net_income")
        ]

        if revenues and net_incomes and len(revenues) == len(net_incomes):
            net_margins = []
            for i in range(min(len(revenues), len(net_incomes))):
                if revenues[i] and revenues[i] > 0 and net_incomes[i] is not None:
                    net_margin = net_incomes[i] / revenues[i]
                    net_margins.append(net_margin)

            if net_margins:
                recent_nm = net_margins[0]
                avg_nm = sum(net_margins) / len(net_margins)

                analysis["net_margin_analysis"] = {
                    "recent_margin": recent_nm,
                    "avg_margin": avg_nm,
                }

                if avg_nm > 0.15:  # >15% net margin
                    analysis["score"] += 1.5
                    analysis["details"].append(
                        f"Excellent net margins {avg_nm:.1%} - highly profitable"
                    )
                elif avg_nm > 0.08:  # 8-15% net margin
                    analysis["score"] += 1.2
                    analysis["details"].append(f"Strong net margins {avg_nm:.1%}")
                elif avg_nm > 0.03:  # 3-8% net margin
                    analysis["score"] += 0.8
                    analysis["details"].append(f"Decent net margins {avg_nm:.1%}")
                elif avg_nm > 0:  # Positive but low
                    analysis["score"] += 0.5
                    analysis["details"].append(f"Low net margins {avg_nm:.1%}")
                else:
                    analysis["details"].append(
                        f"Negative net margins {avg_nm:.1%} - profitability issues"
                    )
        else:
            analysis["details"].append("Cannot calculate net margins - missing data")

        # Margin Stability Analysis (1.5 points max)
        if len(operating_margins) >= 4:
            # Calculate margin volatility
            om_volatility = (
                statistics.pstdev(operating_margins)
                if len(operating_margins) > 1
                else 0
            )

            # Check for consistent positive margins
            positive_margin_years = sum(1 for om in operating_margins if om > 0)
            consistency_ratio = positive_margin_years / len(operating_margins)

            analysis["margin_stability"] = {
                "volatility": om_volatility,
                "consistency_ratio": consistency_ratio,
                "positive_years": positive_margin_years,
            }

            if (
                om_volatility < 0.02 and consistency_ratio == 1.0
            ):  # Very stable + always positive
                analysis["score"] += 1.5
                analysis["details"].append(
                    f"Exceptional margin stability - volatility {om_volatility:.1%}"
                )
            elif (
                om_volatility < 0.05 and consistency_ratio >= 0.8
            ):  # Stable + mostly positive
                analysis["score"] += 1.2
                analysis["details"].append(
                    f"Good margin stability - volatility {om_volatility:.1%}"
                )
            elif consistency_ratio >= 0.6:  # Somewhat stable
                analysis["score"] += 0.8
                analysis["details"].append(f"Moderate margin stability")
            else:
                analysis["details"].append(
                    "Volatile or inconsistent margins - business cyclicality concerns"
                )

        return analysis

    except Exception as e:
        return {
            "error": f"Profit margin analysis failed: {str(e)}",
            "score": 0,
            "max_score": 8,
            "details": ["Error in profit margin analysis"],
        }


def analyze_competitive_position(
    financial_data: Annotated[
        Dict[str, Any],
        "Financial and market data for assessing competitive positioning and moat strength",
    ],
) -> Annotated[
    Dict[str, Any],
    "Competitive position analysis focusing on market share trends, pricing power, and sustainable advantages",
]:
    """
    Analyze competitive position using Fisher's focus on companies with sustainable
    competitive advantages and ability to maintain superior returns over time.

    Key factors:
    - Revenue growth vs industry (market share gains)
    - Pricing power evidenced through margin expansion
    - Innovation leadership through R&D effectiveness
    - Barriers to entry and competitive moat sustainability
    """
    try:
        analysis = {
            "market_position_trend": None,
            "pricing_power": None,
            "innovation_leadership": None,
            "competitive_moat": None,
            "score": 0,
            "max_score": 8,
            "details": [],
        }

        line_items = financial_data.get("line_items", [])
        if not line_items:
            analysis["details"].append("No financial data for competitive analysis")
            return analysis

        # Market Position Trend Analysis (2.5 points max)
        revenues = [item.get("revenue") for item in line_items if item.get("revenue")]

        if len(revenues) >= 3:
            # Calculate revenue acceleration/deceleration
            recent_growth = (revenues[0] / revenues[1] - 1) if revenues[1] > 0 else 0
            older_growth = (revenues[1] / revenues[2] - 1) if revenues[2] > 0 else 0

            growth_acceleration = recent_growth - older_growth
            multi_year_cagr = (
                ((revenues[0] / revenues[-1]) ** (1 / (len(revenues) - 1))) - 1
                if revenues[-1] > 0
                else 0
            )

            analysis["market_position_trend"] = {
                "recent_growth": recent_growth,
                "growth_acceleration": growth_acceleration,
                "multi_year_cagr": multi_year_cagr,
            }

            if (
                multi_year_cagr > 0.15 and growth_acceleration > 0
            ):  # Strong + accelerating
                analysis["score"] += 2.5
                analysis["details"].append(
                    f"Excellent market position - {multi_year_cagr:.1%} CAGR with acceleration"
                )
            elif multi_year_cagr > 0.10 and recent_growth > 0.08:  # Good growth
                analysis["score"] += 2
                analysis["details"].append(
                    f"Strong market position - {multi_year_cagr:.1%} CAGR"
                )
            elif multi_year_cagr > 0.05:  # Moderate growth
                analysis["score"] += 1.5
                analysis["details"].append(
                    f"Decent market position - {multi_year_cagr:.1%} growth"
                )
            elif multi_year_cagr > 0:  # Positive but slow
                analysis["score"] += 1
                analysis["details"].append(
                    f"Modest market position - {multi_year_cagr:.1%} growth"
                )
            else:
                analysis["details"].append(
                    f"Declining market position - {multi_year_cagr:.1%} growth"
                )
        else:
            analysis["details"].append(
                "Insufficient revenue data for market position analysis"
            )

        # Pricing Power Analysis (2.5 points max)
        gross_margins = [
            item.get("gross_margin")
            for item in line_items
            if item.get("gross_margin") is not None
        ]

        if len(gross_margins) >= 3:
            margin_trend = gross_margins[0] - gross_margins[-1]
            avg_margin = sum(gross_margins) / len(gross_margins)

            # Check if margins are expanding while growing
            revenue_growing = len(revenues) >= 2 and revenues[0] > revenues[1]

            analysis["pricing_power"] = {
                "margin_trend": margin_trend,
                "avg_margin": avg_margin,
                "revenue_growing": revenue_growing,
            }

            if (
                margin_trend > 0.02 and revenue_growing and avg_margin > 0.4
            ):  # Expanding margins + growth
                analysis["score"] += 2.5
                analysis["details"].append(
                    f"Exceptional pricing power - expanding margins during growth"
                )
            elif margin_trend > 0 and avg_margin > 0.3:  # Some margin expansion
                analysis["score"] += 2
                analysis["details"].append(
                    f"Good pricing power - stable/improving margins {avg_margin:.1%}"
                )
            elif margin_trend >= -0.01 and avg_margin > 0.25:  # Stable margins
                analysis["score"] += 1.5
                analysis["details"].append(
                    f"Decent pricing power - stable margins {avg_margin:.1%}"
                )
            elif avg_margin > 0.15:  # Positive but declining
                analysis["score"] += 1
                analysis["details"].append(
                    f"Limited pricing power - margin pressure evident"
                )
            else:
                analysis["details"].append(
                    "Weak pricing power - declining margins and competitive pressure"
                )
        else:
            analysis["details"].append(
                "Insufficient margin data for pricing power analysis"
            )

        # Innovation Leadership Analysis (1.5 points max)
        rnd_values = [
            item.get("research_and_development")
            for item in line_items
            if item.get("research_and_development")
        ]

        if rnd_values and revenues:
            # R&D intensity and trend
            rnd_ratios = []
            for i in range(min(len(rnd_values), len(revenues))):
                if revenues[i] and revenues[i] > 0:
                    rnd_ratio = (rnd_values[i] or 0) / revenues[i]
                    rnd_ratios.append(rnd_ratio)

            if rnd_ratios:
                avg_rnd_ratio = sum(rnd_ratios) / len(rnd_ratios)
                rnd_trend = rnd_ratios[0] - rnd_ratios[-1] if len(rnd_ratios) > 1 else 0

                analysis["innovation_leadership"] = {
                    "avg_rnd_ratio": avg_rnd_ratio,
                    "rnd_trend": rnd_trend,
                }

                if avg_rnd_ratio > 0.08 and rnd_trend >= 0:  # High R&D + increasing
                    analysis["score"] += 1.5
                    analysis["details"].append(
                        f"Strong innovation leadership - {avg_rnd_ratio:.1%} R&D intensity"
                    )
                elif avg_rnd_ratio > 0.05:  # Good R&D investment
                    analysis["score"] += 1.2
                    analysis["details"].append(
                        f"Good innovation focus - {avg_rnd_ratio:.1%} R&D"
                    )
                elif avg_rnd_ratio > 0.02:  # Moderate R&D
                    analysis["score"] += 0.8
                    analysis["details"].append(
                        f"Moderate innovation investment - {avg_rnd_ratio:.1%} R&D"
                    )
                else:
                    analysis["details"].append(
                        f"Limited innovation investment - {avg_rnd_ratio:.1%} R&D"
                    )
        else:
            analysis["details"].append("R&D data unavailable for innovation assessment")

        # Competitive Moat Assessment (1.5 points max)
        # Combine multiple indicators: consistent high margins + pricing power + innovation
        moat_indicators = 0

        if gross_margins and sum(gross_margins) / len(gross_margins) > 0.40:
            moat_indicators += 1  # High gross margins indicate pricing power

        if analysis["pricing_power"] and analysis["pricing_power"]["margin_trend"] >= 0:
            moat_indicators += (
                1  # Stable/improving margins indicate competitive strength
            )

        if (
            analysis["innovation_leadership"]
            and analysis["innovation_leadership"]["avg_rnd_ratio"] > 0.05
        ):
            moat_indicators += 1  # Significant R&D indicates innovation barrier

        # ROE consistency (calculated from earlier data)
        net_incomes = [
            item.get("net_income") for item in line_items if item.get("net_income")
        ]
        equities = [
            item.get("shareholders_equity")
            for item in line_items
            if item.get("shareholders_equity")
        ]

        if net_incomes and equities:
            roe_values = []
            for i in range(min(len(net_incomes), len(equities))):
                if equities[i] and equities[i] > 0 and net_incomes[i]:
                    roe = net_incomes[i] / equities[i]
                    roe_values.append(roe)

            if roe_values and sum(roe_values) / len(roe_values) > 0.15:
                moat_indicators += 1  # High ROE indicates competitive advantages

        analysis["competitive_moat"] = {
            "moat_indicators": moat_indicators,
            "total_possible": 4,
        }

        if moat_indicators >= 3:
            analysis["score"] += 1.5
            analysis["details"].append(
                f"Strong competitive moat - {moat_indicators}/4 indicators present"
            )
        elif moat_indicators >= 2:
            analysis["score"] += 1
            analysis["details"].append(
                f"Moderate competitive advantages - {moat_indicators}/4 indicators"
            )
        elif moat_indicators >= 1:
            analysis["score"] += 0.5
            analysis["details"].append(
                f"Limited competitive protection - {moat_indicators}/4 indicators"
            )
        else:
            analysis["details"].append(
                "Weak competitive position - no clear moat indicators"
            )

        return analysis

    except Exception as e:
        return {
            "error": f"Competitive position analysis failed: {str(e)}",
            "score": 0,
            "max_score": 8,
            "details": ["Error in competitive position analysis"],
        }


def calculate_fisher_score(
    analysis_results: Annotated[
        Dict[str, Any], "Combined analysis results from all Fisher methodology tools"
    ],
) -> Annotated[
    Dict[str, Any],
    "Overall Phil Fisher investment score emphasizing long-term growth and management excellence",
]:
    """
    Calculate overall Phil Fisher investment score emphasizing his focus on superior
    long-term growth companies with excellent management and sustainable competitive advantages.

    Scoring weights (reflecting Fisher priorities):
    - Growth Quality: 35% weight (most important for Fisher)
    - Management Excellence: 30% weight (Fisher's key differentiator)
    - Profit Margin Stability: 20% weight (indicates competitive strength)
    - Competitive Position: 15% weight (sustainable advantage assessment)

    Fisher's approach favors companies with superior growth potential and management quality.
    """
    try:
        # Extract individual analysis scores
        growth_analysis = analysis_results.get("growth_analysis", {})
        management_analysis = analysis_results.get("management_analysis", {})
        margin_analysis = analysis_results.get("margin_analysis", {})
        competitive_analysis = analysis_results.get("competitive_analysis", {})

        # Calculate weighted score based on Fisher's priorities
        growth_score = growth_analysis.get("score", 0)  # max 10
        management_score = management_analysis.get("score", 0)  # max 10
        margin_score = margin_analysis.get("score", 0)  # max 8
        competitive_score = competitive_analysis.get("score", 0)  # max 8

        # Weighted calculation reflecting Fisher's emphasis
        weighted_score = (
            (growth_score / 10) * 35  # 35% weight on growth quality
            + (management_score / 10) * 30  # 30% weight on management excellence
            + (margin_score / 8) * 20  # 20% weight on margin stability
            + (competitive_score / 8) * 15  # 15% weight on competitive position
        )

        score_percentage = weighted_score

        # Fisher's criteria for investment signals
        revenue_cagr = growth_analysis.get("revenue_cagr")
        avg_roe = management_analysis.get("roe_trend", {}).get("avg_roe")
        rnd_ratio = growth_analysis.get("rnd_investment_ratio")

        # Signal determination with Fisher's high standards
        if (
            score_percentage >= 80
            and revenue_cagr
            and revenue_cagr > 0.12
            and avg_roe
            and avg_roe > 0.15
        ):
            signal = "bullish"
            conviction = "high"
        elif score_percentage >= 70 and (
            (revenue_cagr and revenue_cagr > 0.08) or (avg_roe and avg_roe > 0.12)
        ):
            signal = "bullish"
            conviction = "moderate"
        elif score_percentage <= 35 or (revenue_cagr and revenue_cagr < 0.03):
            signal = "bearish"
            conviction = "high"
        else:
            signal = "neutral"
            conviction = "low"

        # Assess key Fisher criteria
        strengths = []
        concerns = []
        fisher_checklist = []

        # Growth quality assessment
        if revenue_cagr and revenue_cagr > 0.15:
            strengths.append("Superior revenue growth")
            fisher_checklist.append(f"✓ Exceptional revenue CAGR {revenue_cagr:.1%}")
        elif revenue_cagr and revenue_cagr > 0.08:
            fisher_checklist.append(f"✓ Good revenue CAGR {revenue_cagr:.1%}")
        else:
            concerns.append("Insufficient growth rate")
            fisher_checklist.append("✗ Below-average growth")

        # Management excellence
        if avg_roe and avg_roe > 0.20:
            strengths.append("Exceptional management performance")
            fisher_checklist.append(f"✓ Superior ROE {avg_roe:.1%}")
        elif avg_roe and avg_roe > 0.12:
            fisher_checklist.append(f"✓ Strong ROE {avg_roe:.1%}")
        else:
            concerns.append("Management effectiveness concerns")
            fisher_checklist.append("✗ Inadequate ROE performance")

        # Innovation investment
        if rnd_ratio and rnd_ratio > 0.08:
            strengths.append("Strong innovation investment")
            fisher_checklist.append(f"✓ High R&D investment {rnd_ratio:.1%}")
        elif rnd_ratio and rnd_ratio > 0.03:
            fisher_checklist.append(f"✓ Adequate R&D investment {rnd_ratio:.1%}")
        else:
            fisher_checklist.append("? Limited innovation data")

        # Competitive positioning
        competitive_moat = competitive_analysis.get("competitive_moat", {})
        moat_indicators = competitive_moat.get("moat_indicators", 0)

        if moat_indicators >= 3:
            strengths.append("Strong competitive moat")
            fisher_checklist.append("✓ Multiple competitive advantages")
        elif moat_indicators >= 2:
            fisher_checklist.append("✓ Some competitive protection")
        else:
            concerns.append("Weak competitive position")
            fisher_checklist.append("✗ Limited competitive advantages")

        # Margin quality
        avg_operating_margin = margin_analysis.get("operating_margin_analysis", {}).get(
            "avg_margin"
        )
        if avg_operating_margin and avg_operating_margin > 0.20:
            strengths.append("Superior profit margins")
        elif avg_operating_margin and avg_operating_margin > 0.10:
            fisher_checklist.append("✓ Solid profit margins")
        else:
            concerns.append("Margin pressures evident")

        # Overall Fisher assessment
        analysis_summary = {
            "total_score": weighted_score,
            "max_score": 100,
            "score_percentage": score_percentage,
            "signal": signal,
            "conviction": conviction,
            "strengths": strengths,
            "concerns": concerns,
            "fisher_checklist": fisher_checklist,
            "component_scores": {
                "growth_quality": f"{growth_score:.1f}/10",
                "management_excellence": f"{management_score:.1f}/10",
                "margin_stability": f"{margin_score:.1f}/8",
                "competitive_position": f"{competitive_score:.1f}/8",
            },
            "key_metrics": {
                "revenue_cagr": revenue_cagr,
                "eps_cagr": growth_analysis.get("eps_cagr"),
                "rnd_investment_ratio": rnd_ratio,
                "avg_roe": avg_roe,
                "avg_operating_margin": avg_operating_margin,
                "moat_indicators": moat_indicators,
            },
            "fisher_philosophy": {
                "superior_growth": revenue_cagr and revenue_cagr > 0.12,
                "excellent_management": avg_roe and avg_roe > 0.15,
                "innovation_focus": rnd_ratio and rnd_ratio > 0.05,
                "competitive_strength": moat_indicators >= 2,
                "meets_fisher_criteria": (
                    score_percentage >= 70
                    and revenue_cagr
                    and revenue_cagr > 0.08
                    and avg_roe
                    and avg_roe > 0.12
                ),
            },
        }

        return analysis_summary

    except Exception as e:
        return {
            "error": f"Fisher score calculation failed: {str(e)}",
            "total_score": 0,
            "max_score": 100,
            "score_percentage": 0,
            "signal": "neutral",
            "conviction": "none",
            "fisher_checklist": ["Error in analysis"],
        }
