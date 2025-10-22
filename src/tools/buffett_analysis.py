from typing import Annotated, Dict, Any


def analyze_business_quality(
    financial_data: Annotated[
        Dict[str, Any],
        "Financial data for assessing business quality and fundamental strength",
    ],
) -> Annotated[
    Dict[str, Any],
    "Business quality analysis focusing on ROE, debt levels, margins, and financial strength",
]:
    """
    Analyze business quality using Warren Buffett's emphasis on consistent profitability,
    conservative debt levels, strong margins, and overall financial strength.
    """
    try:
        analysis = {
            "roe_analysis": None,
            "debt_analysis": None,
            "margin_analysis": None,
            "liquidity_analysis": None,
            "score": 0,
            "max_score": 10,
            "details": [],
        }

        line_items = financial_data.get("line_items", [])
        if not line_items:
            analysis["details"].append(
                "No financial data for business quality analysis"
            )
            return analysis

        latest = line_items[0]

        # ROE Analysis (3 points max) - Buffett's key metric for business quality
        net_income = latest.get("net_income")
        total_assets = latest.get("total_assets")
        total_liabilities = latest.get("total_liabilities")

        if net_income and total_assets and total_liabilities:
            shareholders_equity = total_assets - total_liabilities
            if shareholders_equity > 0:
                roe = net_income / shareholders_equity

                analysis["roe_analysis"] = {"roe": roe}

                if roe > 0.20:  # >20% ROE - exceptional
                    analysis["score"] += 3
                    analysis["details"].append(
                        f"Exceptional ROE {roe:.1%} - superior business"
                    )
                elif roe > 0.15:  # >15% ROE - Buffett's target
                    analysis["score"] += 2.5
                    analysis["details"].append(
                        f"Strong ROE {roe:.1%} - quality business"
                    )
                elif roe > 0.12:  # >12% ROE - decent
                    analysis["score"] += 2
                    analysis["details"].append(f"Good ROE {roe:.1%} - solid business")
                elif roe > 0.08:  # 8-12% ROE - moderate
                    analysis["score"] += 1
                    analysis["details"].append(f"Moderate ROE {roe:.1%} - acceptable")
                else:
                    analysis["details"].append(
                        f"Low ROE {roe:.1%} - poor business quality"
                    )

        # Debt Analysis (2.5 points max) - Conservative balance sheet
        if total_assets and total_liabilities:
            debt_to_assets = total_liabilities / total_assets

            analysis["debt_analysis"] = {"debt_to_assets": debt_to_assets}

            if debt_to_assets < 0.3:  # Very conservative - Buffett likes this
                analysis["score"] += 2.5
                analysis["details"].append(
                    f"Excellent debt position - {debt_to_assets:.1%}"
                )
            elif debt_to_assets < 0.5:  # Moderate debt
                analysis["score"] += 2
                analysis["details"].append(f"Good debt position - {debt_to_assets:.1%}")
            elif debt_to_assets < 0.6:  # Higher debt
                analysis["score"] += 1
                analysis["details"].append(
                    f"Moderate debt concern - {debt_to_assets:.1%}"
                )
            else:  # High debt
                analysis["details"].append(f"High debt concern - {debt_to_assets:.1%}")

        # Margin Analysis (2.5 points max) - Profitability strength
        revenue = latest.get("revenue")
        gross_profit = latest.get("gross_profit")

        if revenue and gross_profit and revenue > 0:
            gross_margin = gross_profit / revenue

            analysis["margin_analysis"] = {"gross_margin": gross_margin}

            if gross_margin > 0.5:  # >50% gross margin - exceptional
                analysis["score"] += 2.5
                analysis["details"].append(
                    f"Exceptional gross margins {gross_margin:.1%}"
                )
            elif gross_margin > 0.4:  # 40-50% gross margin - strong
                analysis["score"] += 2
                analysis["details"].append(f"Strong gross margins {gross_margin:.1%}")
            elif gross_margin > 0.3:  # 30-40% gross margin - good
                analysis["score"] += 1.5
                analysis["details"].append(f"Good gross margins {gross_margin:.1%}")
            elif gross_margin > 0.2:  # 20-30% gross margin - modest
                analysis["score"] += 1
                analysis["details"].append(f"Modest gross margins {gross_margin:.1%}")
            else:
                analysis["details"].append(f"Low gross margins {gross_margin:.1%}")

        # Liquidity Analysis (2 points max) - Financial strength
        current_assets = latest.get("current_assets")
        current_liabilities = latest.get("current_liabilities")

        if current_assets and current_liabilities and current_liabilities > 0:
            current_ratio = current_assets / current_liabilities

            analysis["liquidity_analysis"] = {"current_ratio": current_ratio}

            if current_ratio > 2.0:  # Strong liquidity
                analysis["score"] += 2
                analysis["details"].append(
                    f"Strong liquidity - current ratio {current_ratio:.2f}"
                )
            elif current_ratio > 1.5:  # Good liquidity
                analysis["score"] += 1.5
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
            "error": f"Business quality analysis failed: {str(e)}",
            "score": 0,
            "max_score": 10,
            "details": ["Error in business quality analysis"],
        }


def analyze_competitive_moat(
    financial_data: Annotated[
        Dict[str, Any],
        "Financial data for evaluating competitive moat and economic advantages",
    ],
) -> Annotated[
    Dict[str, Any],
    "Competitive moat analysis focusing on ROE consistency, pricing power, and market position",
]:
    """
    Analyze competitive moat using Warren Buffett's focus on durable competitive advantages,
    consistent high returns, and pricing power sustainability over time.
    """
    try:
        analysis = {
            "roe_consistency": None,
            "margin_stability": None,
            "market_position": None,
            "score": 0,
            "max_score": 10,
            "details": [],
        }

        line_items = financial_data.get("line_items", [])
        if not line_items or len(line_items) < 3:
            analysis["details"].append("Insufficient data for moat analysis")
            return analysis

        # ROE Consistency Analysis (5 points max) - Key moat indicator
        roe_values = []
        for item in line_items:
            net_income = item.get("net_income")
            total_assets = item.get("total_assets")
            total_liabilities = item.get("total_liabilities")

            if net_income and total_assets and total_liabilities:
                shareholders_equity = total_assets - total_liabilities
                if shareholders_equity > 0:
                    roe = net_income / shareholders_equity
                    roe_values.append(roe)

        if len(roe_values) >= 3:
            avg_roe = sum(roe_values) / len(roe_values)
            high_roe_periods = sum(1 for roe in roe_values if roe > 0.15)
            consistency_ratio = high_roe_periods / len(roe_values)

            analysis["roe_consistency"] = {
                "avg_roe": avg_roe,
                "consistency_ratio": consistency_ratio,
                "high_roe_periods": high_roe_periods,
            }

            if (
                avg_roe > 0.20 and consistency_ratio >= 0.8
            ):  # 20%+ ROE, 80%+ consistency
                analysis["score"] += 5
                analysis["details"].append(
                    f"Exceptional moat - {avg_roe:.1%} avg ROE, {consistency_ratio*100:.0f}% high periods"
                )
            elif (
                avg_roe > 0.15 and consistency_ratio >= 0.7
            ):  # 15%+ ROE, 70%+ consistency
                analysis["score"] += 4
                analysis["details"].append(
                    f"Strong moat - {avg_roe:.1%} avg ROE with good consistency"
                )
            elif avg_roe > 0.12:  # 12%+ ROE
                analysis["score"] += 3
                analysis["details"].append(f"Moderate moat - {avg_roe:.1%} avg ROE")
            elif avg_roe > 0.08:  # 8-12% ROE
                analysis["score"] += 2
                analysis["details"].append(f"Weak moat - {avg_roe:.1%} avg ROE")
            else:
                analysis["details"].append(f"No evident moat - {avg_roe:.1%} avg ROE")

        # Margin Stability Analysis (3 points max) - Pricing power indicator
        margin_values = []
        for item in line_items:
            revenue = item.get("revenue")
            gross_profit = item.get("gross_profit")
            if revenue and gross_profit and revenue > 0:
                margin = gross_profit / revenue
                margin_values.append(margin)

        if len(margin_values) >= 3:
            avg_margin = sum(margin_values) / len(margin_values)
            recent_margin = margin_values[0]
            oldest_margin = margin_values[-1]

            analysis["margin_stability"] = {
                "avg_margin": avg_margin,
                "recent_margin": recent_margin,
                "trend": (
                    "improving"
                    if recent_margin > oldest_margin
                    else "declining" if recent_margin < oldest_margin else "stable"
                ),
            }

            if (
                avg_margin > 0.5 and recent_margin >= oldest_margin
            ):  # 50%+ margins, stable/improving
                analysis["score"] += 3
                analysis["details"].append(
                    f"Exceptional pricing power - {avg_margin:.1%} margins, stable trend"
                )
            elif avg_margin > 0.4:  # 40%+ margins
                analysis["score"] += 2
                analysis["details"].append(
                    f"Strong pricing power - {avg_margin:.1%} margins"
                )
            elif avg_margin > 0.3:  # 30%+ margins
                analysis["score"] += 1
                analysis["details"].append(
                    f"Moderate pricing power - {avg_margin:.1%} margins"
                )
            else:
                analysis["details"].append(
                    f"Limited pricing power - {avg_margin:.1%} margins"
                )

        # Market Position Assessment (2 points max) - Scale and efficiency
        revenues = [item.get("revenue") for item in line_items if item.get("revenue")]
        if len(revenues) >= 3:
            revenue_growth = revenues[0] > revenues[-1]
            revenue_stability = (
                min(revenues) / max(revenues) > 0.7
            )  # Revenue doesn't vary more than 30%

            analysis["market_position"] = {
                "revenue_growth": revenue_growth,
                "revenue_stability": revenue_stability,
            }

            if revenue_growth and revenue_stability:
                analysis["score"] += 2
                analysis["details"].append(
                    "Strong market position - growing and stable revenues"
                )
            elif revenue_growth or revenue_stability:
                analysis["score"] += 1
                analysis["details"].append("Decent market position")
            else:
                analysis["details"].append("Weak market position indicators")

        return analysis

    except Exception as e:
        return {
            "error": f"Competitive moat analysis failed: {str(e)}",
            "score": 0,
            "max_score": 10,
            "details": ["Error in competitive moat analysis"],
        }


def analyze_management_excellence(
    financial_data: Annotated[
        Dict[str, Any],
        "Financial data for evaluating management quality and capital allocation",
    ],
) -> Annotated[
    Dict[str, Any],
    "Management excellence analysis focusing on capital allocation, shareholder returns, and stewardship",
]:
    """
    Analyze management excellence using Warren Buffett's focus on capital allocation discipline,
    shareholder-friendly actions, and effective stewardship of shareholder capital.
    """
    try:
        analysis = {
            "capital_allocation": None,
            "shareholder_returns": None,
            "financial_stewardship": None,
            "score": 0,
            "max_score": 8,
            "details": [],
        }

        line_items = financial_data.get("line_items", [])
        if not line_items:
            analysis["details"].append("No financial data for management analysis")
            return analysis

        latest = line_items[0]

        # Share Buyback Analysis (3 points max) - Capital allocation discipline
        share_buybacks = latest.get("issuance_or_purchase_of_equity_shares")
        if share_buybacks is not None:
            if share_buybacks < 0:  # Negative means buybacks
                analysis["score"] += 2
                analysis["details"].append(
                    f"Share buybacks ${abs(share_buybacks)/1e6:.0f}M - good capital allocation"
                )

                # Extra point for significant buybacks
                if abs(share_buybacks) > 1e9:  # >$1B in buybacks
                    analysis["score"] += 1
                    analysis["details"].append(
                        "Substantial buyback program shows confidence"
                    )
            elif share_buybacks > 0:
                analysis["details"].append(
                    "Share issuance detected - potential dilution concern"
                )
            else:
                analysis["details"].append("No share buyback activity")

        # Dividend Policy Analysis (2 points max) - Shareholder returns
        dividends = latest.get("dividends_and_other_cash_distributions")
        if dividends is not None and dividends < 0:  # Negative means cash paid out
            analysis["score"] += 1
            analysis["details"].append(
                f"Dividend payments ${abs(dividends)/1e6:.0f}M - shareholder returns"
            )

            # Check for consistency if we have historical data
            if len(line_items) >= 3:
                dividend_payments = [
                    item.get("dividends_and_other_cash_distributions", 0)
                    for item in line_items
                ]
                consistent_dividends = all(
                    d < 0 for d in dividend_payments if d is not None
                )
                if consistent_dividends:
                    analysis["score"] += 1
                    analysis["details"].append(
                        "Consistent dividend policy - reliable shareholder returns"
                    )

        # ROE Trend Analysis (3 points max) - Management effectiveness
        if len(line_items) >= 3:
            roe_values = []
            for item in line_items:
                net_income = item.get("net_income")
                total_assets = item.get("total_assets")
                total_liabilities = item.get("total_liabilities")

                if net_income and total_assets and total_liabilities:
                    shareholders_equity = total_assets - total_liabilities
                    if shareholders_equity > 0:
                        roe = net_income / shareholders_equity
                        roe_values.append(roe)

            if len(roe_values) >= 3:
                recent_roe = roe_values[0]
                older_roe = roe_values[-1]
                avg_roe = sum(roe_values) / len(roe_values)

                analysis["financial_stewardship"] = {
                    "avg_roe": avg_roe,
                    "roe_trend": "improving" if recent_roe > older_roe else "declining",
                }

                if (
                    avg_roe > 0.18 and recent_roe >= older_roe
                ):  # 18%+ ROE and stable/improving
                    analysis["score"] += 3
                    analysis["details"].append(
                        f"Excellent management - {avg_roe:.1%} avg ROE with good trend"
                    )
                elif avg_roe > 0.15:  # 15%+ ROE
                    analysis["score"] += 2
                    analysis["details"].append(
                        f"Strong management - {avg_roe:.1%} avg ROE"
                    )
                elif avg_roe > 0.12:  # 12%+ ROE
                    analysis["score"] += 1
                    analysis["details"].append(
                        f"Decent management - {avg_roe:.1%} avg ROE"
                    )
                else:
                    analysis["details"].append(
                        f"Weak management results - {avg_roe:.1%} avg ROE"
                    )

        # Combine shareholder-friendly actions
        buyback_score = 2 if share_buybacks and share_buybacks < 0 else 0
        dividend_score = 1 if dividends and dividends < 0 else 0

        analysis["capital_allocation"] = {
            "buybacks": share_buybacks and share_buybacks < 0,
            "dividends": dividends and dividends < 0,
            "total_shareholder_friendly_score": buyback_score + dividend_score,
        }

        analysis["shareholder_returns"] = {
            "pays_dividends": dividends and dividends < 0,
            "repurchases_shares": share_buybacks and share_buybacks < 0,
        }

        return analysis

    except Exception as e:
        return {
            "error": f"Management excellence analysis failed: {str(e)}",
            "score": 0,
            "max_score": 8,
            "details": ["Error in management excellence analysis"],
        }


def analyze_earnings_consistency(
    financial_data: Annotated[
        Dict[str, Any],
        "Financial data for evaluating earnings consistency and predictability",
    ],
) -> Annotated[
    Dict[str, Any],
    "Earnings consistency analysis focusing on owner earnings, book value growth, and cash flow quality",
]:
    """
    Analyze earnings consistency using Warren Buffett's focus on predictable business models,
    owner earnings calculation, and steady book value per share growth.
    """
    try:
        analysis = {
            "earnings_stability": None,
            "book_value_growth": None,
            "cash_flow_quality": None,
            "score": 0,
            "max_score": 10,
            "details": [],
        }

        line_items = financial_data.get("line_items", [])
        if not line_items or len(line_items) < 3:
            analysis["details"].append(
                "Insufficient data for earnings consistency analysis"
            )
            return analysis

        # Earnings Stability Analysis (4 points max)
        net_incomes = [
            item.get("net_income") for item in line_items if item.get("net_income")
        ]

        if len(net_incomes) >= 3:
            positive_years = sum(1 for income in net_incomes if income > 0)
            consistency_ratio = positive_years / len(net_incomes)

            # Check for growth trend
            if len(net_incomes) >= 2:
                recent_income = net_incomes[0]
                older_income = net_incomes[-1]
                growth_trend = recent_income > older_income
            else:
                growth_trend = False

            analysis["earnings_stability"] = {
                "consistency_ratio": consistency_ratio,
                "positive_years": positive_years,
                "growth_trend": growth_trend,
            }

            if (
                consistency_ratio >= 0.9 and growth_trend
            ):  # 90%+ profitable years + growth
                analysis["score"] += 4
                analysis["details"].append(
                    "Exceptional earnings consistency with growth"
                )
            elif consistency_ratio >= 0.8:  # 80%+ profitable years
                analysis["score"] += 3
                analysis["details"].append("Strong earnings consistency")
            elif consistency_ratio >= 0.6:  # 60%+ profitable years
                analysis["score"] += 2
                analysis["details"].append("Moderate earnings consistency")
            elif consistency_ratio >= 0.4:  # 40%+ profitable years
                analysis["score"] += 1
                analysis["details"].append("Weak earnings consistency")
            else:
                analysis["details"].append("Poor earnings consistency")

        # Book Value Per Share Growth (3 points max) - Buffett's favorite metric
        book_values_per_share = []
        for item in line_items:
            total_assets = item.get("total_assets")
            total_liabilities = item.get("total_liabilities")
            outstanding_shares = item.get("outstanding_shares")

            if (
                total_assets
                and total_liabilities
                and outstanding_shares
                and outstanding_shares > 0
            ):
                book_value = (total_assets - total_liabilities) / outstanding_shares
                book_values_per_share.append(book_value)

        if len(book_values_per_share) >= 3:
            recent_bv = book_values_per_share[0]
            oldest_bv = book_values_per_share[-1]

            # Calculate CAGR
            years = len(book_values_per_share) - 1
            if oldest_bv > 0:
                bv_cagr = ((recent_bv / oldest_bv) ** (1 / years)) - 1

                analysis["book_value_growth"] = {
                    "bv_cagr": bv_cagr,
                    "recent_bv": recent_bv,
                    "oldest_bv": oldest_bv,
                }

                if bv_cagr > 0.15:  # >15% CAGR
                    analysis["score"] += 3
                    analysis["details"].append(
                        f"Excellent book value CAGR {bv_cagr:.1%}"
                    )
                elif bv_cagr > 0.10:  # 10-15% CAGR
                    analysis["score"] += 2
                    analysis["details"].append(f"Strong book value CAGR {bv_cagr:.1%}")
                elif bv_cagr > 0.05:  # 5-10% CAGR
                    analysis["score"] += 1
                    analysis["details"].append(f"Modest book value CAGR {bv_cagr:.1%}")
                else:
                    analysis["details"].append(f"Weak book value CAGR {bv_cagr:.1%}")

        # Free Cash Flow Quality (3 points max)
        free_cash_flows = [
            item.get("free_cash_flow")
            for item in line_items
            if item.get("free_cash_flow") is not None
        ]

        if len(free_cash_flows) >= 2:
            positive_fcf_years = sum(1 for fcf in free_cash_flows if fcf > 0)
            fcf_consistency = positive_fcf_years / len(free_cash_flows)

            # Check FCF growth
            recent_fcf = free_cash_flows[0]
            older_fcf = free_cash_flows[-1]
            fcf_growth = (
                recent_fcf > older_fcf if recent_fcf > 0 and older_fcf > 0 else False
            )

            analysis["cash_flow_quality"] = {
                "fcf_consistency": fcf_consistency,
                "positive_fcf_years": positive_fcf_years,
                "fcf_growth": fcf_growth,
            }

            if (
                fcf_consistency >= 0.8 and fcf_growth
            ):  # 80%+ positive FCF years + growth
                analysis["score"] += 3
                analysis["details"].append(
                    "Excellent free cash flow quality and growth"
                )
            elif fcf_consistency >= 0.7:  # 70%+ positive FCF years
                analysis["score"] += 2
                analysis["details"].append("Strong free cash flow consistency")
            elif fcf_consistency >= 0.5:  # 50%+ positive FCF years
                analysis["score"] += 1
                analysis["details"].append("Moderate free cash flow quality")
            else:
                analysis["details"].append("Poor free cash flow quality")

        return analysis

    except Exception as e:
        return {
            "error": f"Earnings consistency analysis failed: {str(e)}",
            "score": 0,
            "max_score": 10,
            "details": ["Error in earnings consistency analysis"],
        }


def calculate_intrinsic_value_buffett(
    financial_data: Annotated[
        Dict[str, Any],
        "Financial data and market cap for Buffett-style intrinsic valuation",
    ],
) -> Annotated[
    Dict[str, Any],
    "Intrinsic value calculation using Buffett's owner earnings and conservative DCF approach",
]:
    """
    Calculate intrinsic value using Warren Buffett's approach emphasizing owner earnings,
    conservative growth assumptions, and significant margin of safety requirements.
    """
    try:
        analysis = {
            "owner_earnings": None,
            "dcf_valuation": None,
            "margin_of_safety": None,
            "score": 0,
            "max_score": 8,
            "details": [],
        }

        line_items = financial_data.get("line_items", [])
        market_cap = financial_data.get("market_cap")

        if not line_items or len(line_items) < 2:
            analysis["details"].append(
                "Insufficient data for intrinsic value calculation"
            )
            return analysis

        latest = line_items[0]

        # Calculate Owner Earnings (Buffett's preferred metric)
        net_income = latest.get("net_income")
        depreciation = latest.get("depreciation_and_amortization") or 0
        capex = latest.get("capital_expenditure") or 0

        if net_income:
            # Owner earnings = Net Income + Depreciation - Maintenance CapEx
            # Assume maintenance capex is 80% of total capex (conservative)
            maintenance_capex = abs(capex) * 0.8 if capex else 0
            owner_earnings = net_income + depreciation - maintenance_capex

            analysis["owner_earnings"] = {
                "net_income": net_income,
                "depreciation": depreciation,
                "maintenance_capex": maintenance_capex,
                "owner_earnings": owner_earnings,
            }

            if owner_earnings > 0:
                analysis["score"] += 2
                analysis["details"].append(
                    f"Positive owner earnings: ${owner_earnings/1e6:.0f}M"
                )

                # DCF Valuation using owner earnings
                outstanding_shares = latest.get("outstanding_shares")
                if outstanding_shares and outstanding_shares > 0:

                    # Conservative growth assumptions (Buffett style)
                    # Analyze historical growth to set conservative expectations
                    historical_incomes = [
                        item.get("net_income")
                        for item in line_items
                        if item.get("net_income")
                    ]

                    if len(historical_incomes) >= 3:
                        oldest_income = historical_incomes[-1]
                        latest_income = historical_incomes[0]
                        years = len(historical_incomes) - 1

                        if oldest_income > 0:
                            historical_growth = (
                                (latest_income / oldest_income) ** (1 / years)
                            ) - 1
                            # Conservative adjustment - cap and haircut
                            conservative_growth = max(
                                0.02, min(historical_growth * 0.6, 0.08)
                            )  # 2-8% range
                        else:
                            conservative_growth = 0.03
                    else:
                        conservative_growth = 0.03  # Default 3%

                    # Buffett's conservative DCF parameters
                    discount_rate = 0.10  # 10% required return
                    terminal_growth = 0.025  # Long-term GDP growth
                    projection_years = 10

                    # Calculate DCF
                    dcf_value = 0
                    for year in range(1, projection_years + 1):
                        if year <= 5:
                            growth_rate = conservative_growth
                        else:
                            growth_rate = terminal_growth

                        future_earnings = owner_earnings * ((1 + growth_rate) ** year)
                        present_value = future_earnings / ((1 + discount_rate) ** year)
                        dcf_value += present_value

                    # Terminal value
                    terminal_earnings = (
                        owner_earnings
                        * ((1 + conservative_growth) ** 5)
                        * ((1 + terminal_growth) ** 5)
                    )
                    terminal_value = (terminal_earnings * (1 + terminal_growth)) / (
                        discount_rate - terminal_growth
                    )
                    terminal_pv = terminal_value / (
                        (1 + discount_rate) ** projection_years
                    )

                    total_intrinsic_value = dcf_value + terminal_pv

                    analysis["dcf_valuation"] = {
                        "conservative_growth": conservative_growth,
                        "discount_rate": discount_rate,
                        "terminal_growth": terminal_growth,
                        "intrinsic_value": total_intrinsic_value,
                        "dcf_component": dcf_value,
                        "terminal_component": terminal_pv,
                    }

                    # Margin of Safety Analysis
                    if market_cap and market_cap > 0:
                        margin_of_safety = (
                            total_intrinsic_value - market_cap
                        ) / market_cap

                        analysis["margin_of_safety"] = margin_of_safety

                        # Score based on margin of safety (Buffett demands significant margins)
                        if margin_of_safety > 0.5:  # >50% margin of safety
                            analysis["score"] += 6
                            analysis["details"].append(
                                f"Exceptional value - {margin_of_safety:.1%} margin of safety"
                            )
                        elif margin_of_safety > 0.3:  # 30-50% margin of safety
                            analysis["score"] += 5
                            analysis["details"].append(
                                f"Strong value - {margin_of_safety:.1%} margin of safety"
                            )
                        elif margin_of_safety > 0.15:  # 15-30% margin of safety
                            analysis["score"] += 3
                            analysis["details"].append(
                                f"Fair value - {margin_of_safety:.1%} margin of safety"
                            )
                        elif margin_of_safety > 0:  # 0-15% margin of safety
                            analysis["score"] += 1
                            analysis["details"].append(
                                f"Slight discount - {margin_of_safety:.1%} margin of safety"
                            )
                        else:
                            analysis["details"].append(
                                f"Overvalued - {margin_of_safety:.1%} margin of safety"
                            )

                    analysis["details"].append(
                        f"Intrinsic value: ${total_intrinsic_value/1e9:.2f}B"
                    )
                    analysis["details"].append(
                        f"Growth assumption: {conservative_growth:.1%} conservative"
                    )
            else:
                analysis["details"].append(
                    "Negative owner earnings - value creation concern"
                )

        return analysis

    except Exception as e:
        return {
            "error": f"Intrinsic value calculation failed: {str(e)}",
            "score": 0,
            "max_score": 8,
            "details": ["Error in intrinsic value calculation"],
        }


def calculate_buffett_score(
    analysis_results: Annotated[
        Dict[str, Any], "Combined analysis results from all Buffett methodology tools"
    ],
) -> Annotated[
    Dict[str, Any],
    "Overall Warren Buffett investment score emphasizing business quality, moats, and value",
]:
    """
    Calculate overall Warren Buffett investment score emphasizing his focus on
    wonderful businesses with durable competitive advantages at attractive prices.
    """
    try:
        # Extract individual analysis scores
        business_quality_analysis = analysis_results.get(
            "business_quality_analysis", {}
        )
        moat_analysis = analysis_results.get("moat_analysis", {})
        management_analysis = analysis_results.get("management_analysis", {})
        consistency_analysis = analysis_results.get("consistency_analysis", {})
        valuation_analysis = analysis_results.get("valuation_analysis", {})

        # Calculate weighted score based on Buffett's priorities
        business_quality_score = business_quality_analysis.get("score", 0)  # max 10
        moat_score = moat_analysis.get("score", 0)  # max 10
        management_score = management_analysis.get("score", 0)  # max 8
        consistency_score = consistency_analysis.get("score", 0)  # max 10
        valuation_score = valuation_analysis.get("score", 0)  # max 8

        # Weighted calculation reflecting Buffett's emphasis
        weighted_score = (
            (business_quality_score / 10) * 25  # 25% weight on business quality
            + (moat_score / 10) * 25  # 25% weight on competitive moat
            + (valuation_score / 8) * 20  # 20% weight on intrinsic value
            + (consistency_score / 10) * 15  # 15% weight on earnings consistency
            + (management_score / 8) * 15  # 15% weight on management excellence
        )

        score_percentage = weighted_score

        # Buffett's criteria for investment signals
        avg_roe = business_quality_analysis.get("roe_analysis", {}).get("roe")
        margin_of_safety = valuation_analysis.get("margin_of_safety")
        moat_strength = moat_analysis.get("roe_consistency", {}).get("avg_roe")

        # Signal determination with Buffett's demanding standards
        if (
            score_percentage >= 80
            and margin_of_safety
            and margin_of_safety > 0.3
            and avg_roe
            and avg_roe > 0.15
        ):
            signal = "bullish"
            conviction = "high"
        elif score_percentage >= 70 and margin_of_safety and margin_of_safety > 0.15:
            signal = "bullish"
            conviction = "moderate"
        elif score_percentage <= 40 or (margin_of_safety and margin_of_safety < -0.2):
            signal = "bearish"
            conviction = "high"
        else:
            signal = "neutral"
            conviction = "low"

        # Assess key Buffett criteria
        strengths = []
        concerns = []
        buffett_checklist = []

        # Business quality assessment
        if avg_roe and avg_roe > 0.20:
            strengths.append("Exceptional business quality")
            buffett_checklist.append(
                f"✓ Superior ROE {avg_roe:.1%} - wonderful business"
            )
        elif avg_roe and avg_roe > 0.15:
            buffett_checklist.append(f"✓ Strong ROE {avg_roe:.1%} - quality business")
        else:
            concerns.append("Insufficient business quality")
            buffett_checklist.append("✗ Below Buffett ROE standards")

        # Competitive moat assessment
        if moat_strength and moat_strength > 0.18:
            strengths.append("Strong competitive moat")
            buffett_checklist.append("✓ Durable competitive advantages evident")
        elif moat_strength and moat_strength > 0.12:
            buffett_checklist.append("✓ Some competitive protection")
        else:
            concerns.append("Weak competitive position")
            buffett_checklist.append("✗ Limited economic moat")

        # Margin of safety - Buffett's key decision factor
        if margin_of_safety and margin_of_safety > 0.5:
            strengths.append("Exceptional margin of safety")
            buffett_checklist.append(
                f"✓ Outstanding value - {margin_of_safety:.1%} margin of safety"
            )
        elif margin_of_safety and margin_of_safety > 0.3:
            strengths.append("Strong margin of safety")
            buffett_checklist.append(
                f"✓ Significant discount - {margin_of_safety:.1%} margin of safety"
            )
        elif margin_of_safety and margin_of_safety > 0.1:
            buffett_checklist.append(
                f"✓ Modest discount - {margin_of_safety:.1%} margin of safety"
            )
        else:
            concerns.append("Insufficient margin of safety")
            buffett_checklist.append("✗ Overvalued or inadequate discount")

        # Management excellence
        shareholder_returns = management_analysis.get("shareholder_returns", {})
        if shareholder_returns and (
            shareholder_returns.get("pays_dividends")
            or shareholder_returns.get("repurchases_shares")
        ):
            strengths.append("Shareholder-friendly management")
            buffett_checklist.append("✓ Capital allocation excellence")

        # Earnings consistency
        earnings_stability = consistency_analysis.get("earnings_stability", {})
        if earnings_stability and earnings_stability.get("consistency_ratio", 0) >= 0.8:
            strengths.append("Predictable business model")
            buffett_checklist.append("✓ Consistent earnings power")

        # Overall Buffett assessment
        analysis_summary = {
            "total_score": weighted_score,
            "max_score": 100,
            "score_percentage": score_percentage,
            "signal": signal,
            "conviction": conviction,
            "strengths": strengths,
            "concerns": concerns,
            "buffett_checklist": buffett_checklist,
            "component_scores": {
                "business_quality": f"{business_quality_score:.1f}/10",
                "competitive_moat": f"{moat_score:.1f}/10",
                "management_excellence": f"{management_score:.1f}/8",
                "earnings_consistency": f"{consistency_score:.1f}/10",
                "intrinsic_value": f"{valuation_score:.1f}/8",
            },
            "key_metrics": {
                "business_roe": avg_roe,
                "moat_roe": moat_strength,
                "margin_of_safety": margin_of_safety,
                "owner_earnings": valuation_analysis.get("owner_earnings", {}).get(
                    "owner_earnings"
                ),
                "intrinsic_value": valuation_analysis.get("dcf_valuation", {}).get(
                    "intrinsic_value"
                ),
            },
            "buffett_philosophy": {
                "wonderful_business": avg_roe and avg_roe > 0.15,
                "durable_moat": moat_strength and moat_strength > 0.12,
                "excellent_management": shareholder_returns
                and (
                    shareholder_returns.get("pays_dividends")
                    or shareholder_returns.get("repurchases_shares")
                ),
                "predictable_earnings": earnings_stability
                and earnings_stability.get("consistency_ratio", 0) >= 0.7,
                "attractive_price": margin_of_safety and margin_of_safety > 0.15,
                "meets_buffett_criteria": (
                    score_percentage >= 70
                    and margin_of_safety
                    and margin_of_safety > 0.15
                    and avg_roe
                    and avg_roe > 0.12
                ),
            },
        }

        return analysis_summary

    except Exception as e:
        return {
            "error": f"Buffett score calculation failed: {str(e)}",
            "total_score": 0,
            "max_score": 100,
            "score_percentage": 0,
            "signal": "neutral",
            "conviction": "none",
            "buffett_checklist": ["Error in analysis"],
        }
