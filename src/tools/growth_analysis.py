import json
import statistics
from typing import List, Dict, Any, Optional


def calculate_trend_slope(data_points: str) -> str:
    """
    Calculate the slope of a trend line for given data points.

    Args:
        data_points: JSON string containing list of numerical values

    Returns:
        JSON string with trend analysis
    """
    try:
        data = json.loads(data_points)

        # Filter out None values
        clean_data = [d for d in data if d is not None]

        if len(clean_data) < 2:
            return json.dumps(
                {
                    "slope": 0.0,
                    "trend": "insufficient_data",
                    "data_points": len(clean_data),
                }
            )

        # Simple linear regression to calculate slope
        y = clean_data
        x = list(range(len(y)))

        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(i * j for i, j in zip(x, y))
        sum_x2 = sum(i**2 for i in x)
        n = len(y)

        if n * sum_x2 - sum_x**2 == 0:
            slope = 0.0
        else:
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)

        # Interpret trend
        if slope > 0.02:
            trend = "strongly_positive"
        elif slope > 0:
            trend = "positive"
        elif slope < -0.02:
            trend = "strongly_negative"
        elif slope < 0:
            trend = "negative"
        else:
            trend = "flat"

        analysis = {
            "slope": float(slope),
            "trend": trend,
            "data_points": len(clean_data),
            "latest_value": clean_data[0] if clean_data else None,
            "average_value": statistics.mean(clean_data) if clean_data else None,
        }

        return json.dumps(analysis)

    except Exception as e:
        return json.dumps(
            {
                "slope": 0.0,
                "trend": "error",
                "error": f"Error calculating trend: {str(e)}",
            }
        )


def analyze_historical_growth(financial_metrics: str) -> str:
    """
    Analyze historical growth trends across revenue, EPS, and FCF.

    Args:
        financial_metrics: JSON string containing historical financial metrics

    Returns:
        JSON string with comprehensive growth analysis
    """
    try:
        metrics = json.loads(financial_metrics)

        if not metrics or len(metrics) < 2:
            return json.dumps(
                {
                    "score": 0.0,
                    "error": "Insufficient historical data for growth analysis",
                }
            )

        # Extract growth metrics (most recent first)
        revenue_growth = [m.get("revenue_growth") for m in metrics]
        eps_growth = [m.get("earnings_per_share_growth") for m in metrics]
        fcf_growth = [m.get("free_cash_flow_growth") for m in metrics]

        # Calculate trends
        rev_trend_data = calculate_trend_slope(json.dumps(revenue_growth))
        eps_trend_data = calculate_trend_slope(json.dumps(eps_growth))
        fcf_trend_data = calculate_trend_slope(json.dumps(fcf_growth))

        rev_trend = json.loads(rev_trend_data)["slope"]
        eps_trend = json.loads(eps_trend_data)["slope"]
        fcf_trend = json.loads(fcf_trend_data)["slope"]

        # Score based on recent growth and trends
        score = 0.0

        # Revenue Growth Analysis (40% of total)
        recent_rev_growth = revenue_growth[0] if revenue_growth[0] is not None else 0
        if recent_rev_growth > 0.20:  # 20%+ excellent
            score += 0.4
        elif recent_rev_growth > 0.10:  # 10%+ good
            score += 0.2

        if rev_trend > 0:  # Accelerating growth bonus
            score += 0.1

        # EPS Growth Analysis (30% of total)
        recent_eps_growth = eps_growth[0] if eps_growth[0] is not None else 0
        if recent_eps_growth > 0.20:  # 20%+ excellent
            score += 0.25
        elif recent_eps_growth > 0.10:  # 10%+ good
            score += 0.1

        if eps_trend > 0:  # Accelerating earnings
            score += 0.05

        # FCF Growth Analysis (10% of total)
        recent_fcf_growth = fcf_growth[0] if fcf_growth[0] is not None else 0
        if recent_fcf_growth > 0.15:  # 15%+ strong cash generation
            score += 0.1

        score = min(score, 1.0)  # Cap at 1.0

        # Determine growth quality
        if score >= 0.8:
            quality = "excellent"
        elif score >= 0.6:
            quality = "strong"
        elif score >= 0.4:
            quality = "moderate"
        else:
            quality = "weak"

        analysis = {
            "score": score,
            "quality": quality,
            "revenue_growth": recent_rev_growth,
            "revenue_trend": rev_trend,
            "eps_growth": recent_eps_growth,
            "eps_trend": eps_trend,
            "fcf_growth": recent_fcf_growth,
            "fcf_trend": fcf_trend,
            "growth_summary": f"Revenue: {recent_rev_growth:.1%}, EPS: {recent_eps_growth:.1%}, FCF: {recent_fcf_growth:.1%}",
            "trend_summary": f"Rev Trend: {'↑' if rev_trend > 0 else '↓'}, EPS Trend: {'↑' if eps_trend > 0 else '↓'}, FCF Trend: {'↑' if fcf_trend > 0 else '↓'}",
        }

        return json.dumps(analysis)

    except Exception as e:
        return json.dumps({"score": 0.0, "error": f"Error analyzing growth: {str(e)}"})


def analyze_growth_valuation(financial_metrics: str) -> str:
    """
    Analyze valuation metrics from a growth perspective.

    Args:
        financial_metrics: JSON string containing current valuation metrics

    Returns:
        JSON string with growth-oriented valuation analysis
    """
    try:
        metrics = json.loads(financial_metrics)

        peg_ratio = metrics.get("peg_ratio")
        ps_ratio = metrics.get("price_to_sales_ratio")
        pe_ratio = metrics.get("price_to_earnings_ratio")

        score = 0.0
        details = []

        # PEG Ratio Analysis (50% weight)
        if peg_ratio is not None:
            if peg_ratio < 1.0:
                score += 0.5
                details.append(f"Excellent PEG: {peg_ratio:.2f}")
            elif peg_ratio < 2.0:
                score += 0.25
                details.append(f"Reasonable PEG: {peg_ratio:.2f}")
            else:
                details.append(f"High PEG: {peg_ratio:.2f}")
        else:
            details.append("PEG: N/A")

        # Price-to-Sales Analysis (50% weight)
        if ps_ratio is not None:
            if ps_ratio < 2.0:
                score += 0.5
                details.append(f"Attractive P/S: {ps_ratio:.2f}")
            elif ps_ratio < 5.0:
                score += 0.25
                details.append(f"Reasonable P/S: {ps_ratio:.2f}")
            else:
                details.append(f"High P/S: {ps_ratio:.2f}")
        else:
            details.append("P/S: N/A")

        score = min(score, 1.0)

        # Determine valuation attractiveness
        if score >= 0.75:
            attractiveness = "very_attractive"
        elif score >= 0.5:
            attractiveness = "attractive"
        elif score >= 0.25:
            attractiveness = "fair"
        else:
            attractiveness = "expensive"

        analysis = {
            "score": score,
            "attractiveness": attractiveness,
            "peg_ratio": peg_ratio,
            "price_to_sales_ratio": ps_ratio,
            "price_to_earnings_ratio": pe_ratio,
            "details": ", ".join(details),
            "interpretation": (
                "Growth at attractive price"
                if score >= 0.5
                else (
                    "Growth at fair price"
                    if score >= 0.25
                    else "Expensive relative to growth"
                )
            ),
        }

        return json.dumps(analysis)

    except Exception as e:
        return json.dumps(
            {"score": 0.0, "error": f"Error analyzing valuation: {str(e)}"}
        )


def analyze_margin_expansion(financial_metrics: str) -> str:
    """
    Analyze margin trends and expansion potential.

    Args:
        financial_metrics: JSON string containing historical margin data

    Returns:
        JSON string with margin expansion analysis
    """
    try:
        metrics = json.loads(financial_metrics)

        if not metrics or len(metrics) < 2:
            return json.dumps(
                {"score": 0.0, "error": "Insufficient data for margin analysis"}
            )

        # Extract margin data
        gross_margins = [m.get("gross_margin") for m in metrics]
        operating_margins = [m.get("operating_margin") for m in metrics]
        net_margins = [m.get("net_margin") for m in metrics]

        # Calculate trends
        gm_trend_data = calculate_trend_slope(json.dumps(gross_margins))
        om_trend_data = calculate_trend_slope(json.dumps(operating_margins))
        nm_trend_data = calculate_trend_slope(json.dumps(net_margins))

        gm_trend = json.loads(gm_trend_data)["slope"]
        om_trend = json.loads(om_trend_data)["slope"]
        nm_trend = json.loads(nm_trend_data)["slope"]

        score = 0.0

        # Current margin levels
        current_gm = gross_margins[0] if gross_margins[0] is not None else 0
        current_om = operating_margins[0] if operating_margins[0] is not None else 0
        current_nm = net_margins[0] if net_margins[0] is not None else 0

        # Gross Margin Analysis (40% weight)
        if current_gm > 0.5:  # 50%+ is excellent
            score += 0.2
        elif current_gm > 0.3:  # 30%+ is good
            score += 0.1

        if gm_trend > 0:  # Expanding gross margin
            score += 0.2

        # Operating Margin Analysis (40% weight)
        if current_om > 0.15:  # 15%+ is strong
            score += 0.2
        elif current_om > 0.1:  # 10%+ is decent
            score += 0.1

        if om_trend > 0:  # Expanding operating margin
            score += 0.2

        # Net Margin Trend (20% weight)
        if nm_trend > 0:  # Expanding net margin
            score += 0.2

        score = min(score, 1.0)

        # Determine margin quality
        if score >= 0.8:
            quality = "exceptional"
        elif score >= 0.6:
            quality = "strong"
        elif score >= 0.4:
            quality = "moderate"
        else:
            quality = "weak"

        analysis = {
            "score": score,
            "quality": quality,
            "gross_margin": current_gm,
            "gross_margin_trend": gm_trend,
            "operating_margin": current_om,
            "operating_margin_trend": om_trend,
            "net_margin": current_nm,
            "net_margin_trend": nm_trend,
            "margin_summary": f"GM: {current_gm:.1%}, OM: {current_om:.1%}, NM: {current_nm:.1%}",
            "trend_summary": f"Trends - GM: {'↑' if gm_trend > 0 else '↓'}, OM: {'↑' if om_trend > 0 else '↓'}, NM: {'↑' if nm_trend > 0 else '↓'}",
        }

        return json.dumps(analysis)

    except Exception as e:
        return json.dumps({"score": 0.0, "error": f"Error analyzing margins: {str(e)}"})


def analyze_insider_activity(insider_trades: str) -> str:
    """
    Analyze insider trading activity for conviction signals.

    Args:
        insider_trades: JSON string containing insider trading data

    Returns:
        JSON string with insider conviction analysis
    """
    try:
        trades = json.loads(insider_trades)

        if not trades:
            return json.dumps(
                {
                    "score": 0.5,
                    "net_flow_ratio": 0.0,
                    "buys": 0.0,
                    "sells": 0.0,
                    "interpretation": "No insider trading data available",
                }
            )

        # Calculate buy and sell totals
        buys = 0.0
        sells = 0.0

        for trade in trades:
            transaction_value = trade.get("transaction_value", 0) or 0
            transaction_shares = trade.get("transaction_shares", 0) or 0

            if transaction_value and transaction_shares > 0:  # Buy
                buys += transaction_value
            elif transaction_value and transaction_shares < 0:  # Sell
                sells += abs(transaction_value)

        # Calculate net flow ratio
        total_activity = buys + sells
        if total_activity == 0:
            net_flow_ratio = 0.0
        else:
            net_flow_ratio = (buys - sells) / total_activity

        # Score based on net flow ratio
        if net_flow_ratio > 0.5:
            score = 1.0
            conviction = "very_bullish"
        elif net_flow_ratio > 0.1:
            score = 0.7
            conviction = "bullish"
        elif net_flow_ratio > -0.1:
            score = 0.5
            conviction = "neutral"
        elif net_flow_ratio > -0.5:
            score = 0.3
            conviction = "bearish"
        else:
            score = 0.1
            conviction = "very_bearish"

        analysis = {
            "score": score,
            "conviction": conviction,
            "net_flow_ratio": net_flow_ratio,
            "buys": buys,
            "sells": sells,
            "total_activity": total_activity,
            "interpretation": (
                "Strong insider buying signal"
                if net_flow_ratio > 0.3
                else (
                    "Moderate insider buying"
                    if net_flow_ratio > 0
                    else (
                        "Balanced insider activity"
                        if net_flow_ratio == 0
                        else (
                            "Insider selling pressure"
                            if net_flow_ratio > -0.3
                            else "Heavy insider selling"
                        )
                    )
                )
            ),
        }

        return json.dumps(analysis)

    except Exception as e:
        return json.dumps(
            {"score": 0.5, "error": f"Error analyzing insider activity: {str(e)}"}
        )


def assess_financial_stability(financial_metrics: str) -> str:
    """
    Assess financial health and stability for sustainable growth.

    Args:
        financial_metrics: JSON string containing financial health metrics

    Returns:
        JSON string with financial stability analysis
    """
    try:
        metrics = json.loads(financial_metrics)

        debt_to_equity = metrics.get("debt_to_equity")
        current_ratio = metrics.get("current_ratio")

        score = 1.0  # Start with perfect score and deduct for issues
        concerns = []
        strengths = []

        # Debt-to-Equity Analysis
        if debt_to_equity is not None:
            if debt_to_equity > 1.5:
                score -= 0.5
                concerns.append(f"High debt burden: D/E {debt_to_equity:.2f}")
            elif debt_to_equity > 0.8:
                score -= 0.2
                concerns.append(f"Elevated debt: D/E {debt_to_equity:.2f}")
            else:
                strengths.append(f"Conservative debt: D/E {debt_to_equity:.2f}")
        else:
            concerns.append("D/E ratio not available")

        # Current Ratio Analysis
        if current_ratio is not None:
            if current_ratio < 1.0:
                score -= 0.5
                concerns.append(f"Poor liquidity: Current ratio {current_ratio:.2f}")
            elif current_ratio < 1.5:
                score -= 0.2
                concerns.append(
                    f"Adequate liquidity: Current ratio {current_ratio:.2f}"
                )
            else:
                strengths.append(f"Strong liquidity: Current ratio {current_ratio:.2f}")
        else:
            concerns.append("Current ratio not available")

        score = max(score, 0.0)  # Don't go below 0

        # Determine financial health
        if score >= 0.8:
            health = "excellent"
        elif score >= 0.6:
            health = "good"
        elif score >= 0.4:
            health = "fair"
        else:
            health = "poor"

        analysis = {
            "score": score,
            "health": health,
            "debt_to_equity": debt_to_equity,
            "current_ratio": current_ratio,
            "strengths": strengths,
            "concerns": concerns,
            "interpretation": (
                "Strong balance sheet supports growth"
                if score >= 0.7
                else (
                    "Adequate financial foundation"
                    if score >= 0.5
                    else "Financial constraints may limit growth"
                )
            ),
        }

        return json.dumps(analysis)

    except Exception as e:
        return json.dumps(
            {"score": 0.5, "error": f"Error assessing financial stability: {str(e)}"}
        )
