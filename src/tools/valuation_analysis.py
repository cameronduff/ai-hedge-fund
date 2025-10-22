import json
import math
import statistics
from typing import Dict, Any, List, Optional, Tuple


def calculate_enhanced_dcf(financial_data: str) -> str:
    """
    Calculate enhanced DCF valuation with multi-stage growth and scenario analysis.

    Args:
        financial_data: JSON string containing financial metrics, FCF history, and market data

    Returns:
        JSON string with DCF analysis results
    """
    try:
        data = json.loads(financial_data)
        fcf_history = data.get("fcf_history", [])
        growth_metrics = data.get("growth_metrics", {})
        market_cap = data.get("market_cap", 0)
        financial_metrics = data.get("financial_metrics", [])

        if not fcf_history or fcf_history[0] <= 0:
            return json.dumps(
                {
                    "value": 0,
                    "confidence": 0,
                    "details": "Insufficient or negative free cash flow data",
                    "scenarios": {"bear": 0, "base": 0, "bull": 0},
                }
            )

        # Calculate WACC
        wacc = calculate_wacc(financial_metrics)

        # Get growth rates
        revenue_growth = growth_metrics.get("revenue_growth", 0.05)
        fcf_growth = growth_metrics.get("fcf_growth", 0.05)

        # Multi-stage growth assumptions
        high_growth = min(max(revenue_growth or 0.05, 0.02), 0.25)
        if market_cap > 50_000_000_000:  # Large cap adjustment
            high_growth = min(high_growth, 0.10)

        transition_growth = (high_growth + 0.03) / 2
        terminal_growth = min(0.03, high_growth * 0.6)

        # Calculate scenarios
        scenarios = {
            "bear": {"growth_adj": 0.6, "wacc_adj": 1.3, "terminal_adj": 0.7},
            "base": {"growth_adj": 1.0, "wacc_adj": 1.0, "terminal_adj": 1.0},
            "bull": {"growth_adj": 1.4, "wacc_adj": 0.85, "terminal_adj": 1.2},
        }

        results = {}
        for scenario, adjustments in scenarios.items():
            adj_high_growth = high_growth * adjustments["growth_adj"]
            adj_wacc = wacc * adjustments["wacc_adj"]
            adj_terminal = terminal_growth * adjustments["terminal_adj"]

            scenario_value = calculate_dcf_value(
                fcf_history[0],
                adj_high_growth,
                transition_growth,
                adj_terminal,
                adj_wacc,
            )
            results[scenario] = max(scenario_value, 0)

        # Expected value (probability weighted)
        expected_value = (
            results["bear"] * 0.2 + results["base"] * 0.6 + results["bull"] * 0.2
        )

        # Calculate confidence based on FCF quality
        fcf_quality = calculate_fcf_quality(fcf_history)
        confidence = min(85, 50 + (fcf_quality * 35))

        return json.dumps(
            {
                "value": expected_value,
                "confidence": confidence,
                "wacc": wacc,
                "terminal_growth": terminal_growth,
                "scenarios": results,
                "fcf_quality_score": fcf_quality,
                "details": f"DCF with {len(fcf_history)} years FCF data, WACC: {wacc:.1%}, Terminal growth: {terminal_growth:.1%}",
            }
        )

    except Exception as e:
        return json.dumps(
            {
                "value": 0,
                "confidence": 0,
                "details": f"Error in DCF calculation: {str(e)}",
                "scenarios": {"bear": 0, "base": 0, "bull": 0},
            }
        )


def calculate_owner_earnings(financial_data: str) -> str:
    """
    Calculate Buffett-style owner earnings valuation.

    Args:
        financial_data: JSON string containing earnings, capex, and cash flow data

    Returns:
        JSON string with owner earnings analysis
    """
    try:
        data = json.loads(financial_data)
        net_income = data.get("net_income", 0)
        depreciation = data.get("depreciation", 0)
        capex = data.get("capex", 0)
        working_capital_change = data.get("working_capital_change", 0)

        if not all(
            isinstance(x, (int, float)) for x in [net_income, depreciation, capex]
        ):
            return json.dumps(
                {
                    "value": 0,
                    "confidence": 0,
                    "owner_earnings": 0,
                    "details": "Insufficient data for owner earnings calculation",
                }
            )

        # Calculate owner earnings
        owner_earnings = net_income + depreciation - capex - working_capital_change

        if owner_earnings <= 0:
            return json.dumps(
                {
                    "value": 0,
                    "confidence": 30,
                    "owner_earnings": owner_earnings,
                    "details": "Negative owner earnings - company consuming cash",
                }
            )

        # Growth and return assumptions
        growth_rate = data.get("growth_rate", 0.05)
        required_return = data.get("required_return", 0.12)
        margin_of_safety = data.get("margin_of_safety", 0.25)

        # Two-stage valuation model
        growth_years = 7
        terminal_growth = min(growth_rate, 0.03)

        # Present value of growth stage
        pv_growth = 0
        for year in range(1, growth_years + 1):
            future_earnings = owner_earnings * (1 + growth_rate) ** year
            pv_growth += future_earnings / (1 + required_return) ** year

        # Terminal value
        terminal_earnings = owner_earnings * (1 + growth_rate) ** growth_years
        if required_return <= terminal_growth:
            terminal_growth = required_return * 0.5  # Safety adjustment

        terminal_value = (terminal_earnings * (1 + terminal_growth)) / (
            required_return - terminal_growth
        )
        pv_terminal = terminal_value / (1 + required_return) ** growth_years

        # Total intrinsic value with margin of safety
        intrinsic_value = (pv_growth + pv_terminal) * (1 - margin_of_safety)

        # Confidence based on earnings quality
        earnings_quality = min(max(owner_earnings / max(abs(net_income), 1), 0), 2)
        confidence = min(90, 40 + (earnings_quality * 30))

        return json.dumps(
            {
                "value": intrinsic_value,
                "confidence": confidence,
                "owner_earnings": owner_earnings,
                "growth_rate": growth_rate,
                "required_return": required_return,
                "margin_of_safety": margin_of_safety,
                "details": f"Owner earnings: ${owner_earnings:,.0f}, Growth: {growth_rate:.1%}, Required return: {required_return:.1%}",
            }
        )

    except Exception as e:
        return json.dumps(
            {
                "value": 0,
                "confidence": 0,
                "owner_earnings": 0,
                "details": f"Error in owner earnings calculation: {str(e)}",
            }
        )


def calculate_ev_ebitda_valuation(financial_data: str) -> str:
    """
    Calculate valuation using EV/EBITDA multiple analysis.

    Args:
        financial_data: JSON string containing EBITDA and enterprise value data

    Returns:
        JSON string with EV/EBITDA analysis
    """
    try:
        data = json.loads(financial_data)
        financial_metrics = data.get("financial_metrics", [])

        if not financial_metrics:
            return json.dumps(
                {
                    "value": 0,
                    "confidence": 0,
                    "current_multiple": 0,
                    "details": "No financial metrics available",
                }
            )

        # Get current metrics
        current = financial_metrics[0]
        enterprise_value = current.get("enterprise_value", 0)
        ev_ebitda_ratio = current.get("enterprise_value_to_ebitda_ratio", 0)
        market_cap = current.get("market_cap", 0)

        if not all([enterprise_value, ev_ebitda_ratio, market_cap]):
            return json.dumps(
                {
                    "value": 0,
                    "confidence": 0,
                    "current_multiple": 0,
                    "details": "Incomplete EV/EBITDA data",
                }
            )

        # Calculate current EBITDA
        current_ebitda = (
            enterprise_value / ev_ebitda_ratio if ev_ebitda_ratio != 0 else 0
        )

        if current_ebitda <= 0:
            return json.dumps(
                {
                    "value": 0,
                    "confidence": 20,
                    "current_multiple": ev_ebitda_ratio,
                    "details": "Negative or zero EBITDA",
                }
            )

        # Calculate historical median multiple
        historical_multiples = []
        for metrics in financial_metrics:
            multiple = metrics.get("enterprise_value_to_ebitda_ratio", 0)
            if multiple > 0 and multiple < 50:  # Filter outliers
                historical_multiples.append(multiple)

        if len(historical_multiples) < 2:
            target_multiple = ev_ebitda_ratio  # Use current if no history
            confidence = 40
        else:
            target_multiple = statistics.median(historical_multiples)
            confidence = min(75, 45 + len(historical_multiples) * 5)

        # Industry adjustment (simplified)
        if market_cap > 10_000_000_000:  # Large cap premium
            target_multiple *= 1.1
        elif market_cap < 1_000_000_000:  # Small cap discount
            target_multiple *= 0.9

        # Calculate implied enterprise value and equity value
        implied_ev = current_ebitda * target_multiple
        net_debt = enterprise_value - market_cap
        implied_equity_value = max(implied_ev - net_debt, 0)

        multiple_premium = (
            (ev_ebitda_ratio / target_multiple - 1) if target_multiple > 0 else 0
        )

        return json.dumps(
            {
                "value": implied_equity_value,
                "confidence": confidence,
                "current_multiple": ev_ebitda_ratio,
                "target_multiple": target_multiple,
                "multiple_premium_discount": multiple_premium,
                "current_ebitda": current_ebitda,
                "details": f"Current EV/EBITDA: {ev_ebitda_ratio:.1f}x, Target: {target_multiple:.1f}x, EBITDA: ${current_ebitda:,.0f}",
            }
        )

    except Exception as e:
        return json.dumps(
            {
                "value": 0,
                "confidence": 0,
                "current_multiple": 0,
                "details": f"Error in EV/EBITDA calculation: {str(e)}",
            }
        )


def calculate_residual_income(financial_data: str) -> str:
    """
    Calculate valuation using Residual Income Model (Edwards-Bell-Ohlson).

    Args:
        financial_data: JSON string containing ROE, book value, and market data

    Returns:
        JSON string with residual income analysis
    """
    try:
        data = json.loads(financial_data)
        market_cap = data.get("market_cap", 0)
        net_income = data.get("net_income", 0)
        price_to_book = data.get("price_to_book_ratio", 0)

        if not all([market_cap, net_income, price_to_book]) or price_to_book <= 0:
            return json.dumps(
                {
                    "value": 0,
                    "confidence": 0,
                    "current_roe": 0,
                    "details": "Insufficient data for residual income model",
                }
            )

        # Calculate book value and ROE
        book_value = market_cap / price_to_book
        current_roe = net_income / book_value if book_value > 0 else 0

        # Model assumptions
        cost_of_equity = data.get("cost_of_equity", 0.10)
        book_value_growth = data.get("book_value_growth", 0.03)
        terminal_growth = min(book_value_growth, 0.03)

        # Calculate initial residual income
        residual_income_0 = net_income - (cost_of_equity * book_value)

        if residual_income_0 <= 0:
            return json.dumps(
                {
                    "value": book_value * 0.8,  # Asset value with discount
                    "confidence": 35,
                    "current_roe": current_roe,
                    "details": f"Negative residual income, ROE {current_roe:.1%} < Cost of equity {cost_of_equity:.1%}",
                }
            )

        # Present value of residual income over explicit forecast period
        forecast_years = 5
        pv_residual_income = 0

        for year in range(1, forecast_years + 1):
            # Assume residual income grows with book value
            future_ri = residual_income_0 * (1 + book_value_growth) ** year
            pv_residual_income += future_ri / (1 + cost_of_equity) ** year

        # Terminal value of residual income
        if cost_of_equity <= terminal_growth:
            terminal_growth = cost_of_equity * 0.5

        terminal_ri = residual_income_0 * (1 + book_value_growth) ** (
            forecast_years + 1
        )
        terminal_value = terminal_ri / (cost_of_equity - terminal_growth)
        pv_terminal = terminal_value / (1 + cost_of_equity) ** forecast_years

        # Total intrinsic value
        intrinsic_value = book_value + pv_residual_income + pv_terminal

        # Apply margin of safety
        intrinsic_value *= 0.85

        # Confidence based on ROE sustainability
        roe_premium = current_roe - cost_of_equity
        sustainability_score = min(max(roe_premium / 0.05, 0), 1)  # Normalize to 0-1
        confidence = min(80, 40 + (sustainability_score * 40))

        return json.dumps(
            {
                "value": intrinsic_value,
                "confidence": confidence,
                "current_roe": current_roe,
                "cost_of_equity": cost_of_equity,
                "book_value_growth": book_value_growth,
                "residual_income": residual_income_0,
                "details": f"ROE: {current_roe:.1%}, Cost of equity: {cost_of_equity:.1%}, Book value growth: {book_value_growth:.1%}",
            }
        )

    except Exception as e:
        return json.dumps(
            {
                "value": 0,
                "confidence": 0,
                "current_roe": 0,
                "details": f"Error in residual income calculation: {str(e)}",
            }
        )


def aggregate_valuation_methods(valuation_data: str) -> str:
    """
    Aggregate multiple valuation methods with weighted approach.

    Args:
        valuation_data: JSON string containing results from all valuation methods

    Returns:
        JSON string with aggregated valuation and investment signal
    """
    try:
        data = json.loads(valuation_data)
        market_cap = data.get("market_cap", 0)

        if market_cap <= 0:
            return json.dumps(
                {
                    "signal": "neutral",
                    "confidence": 0,
                    "weighted_value_gap": 0,
                    "details": "Invalid market cap data",
                }
            )

        # Method weights (can be adjusted based on business characteristics)
        method_weights = {
            "dcf": 0.35,
            "owner_earnings": 0.35,
            "ev_ebitda": 0.20,
            "residual_income": 0.10,
        }

        # Collect method results
        methods = {}
        for method_name, weight in method_weights.items():
            method_data = data.get(f"{method_name}_results", {})
            value = method_data.get("value", 0)
            confidence = method_data.get("confidence", 0)

            if value > 0 and confidence > 20:  # Valid result
                value_gap = (value - market_cap) / market_cap
                methods[method_name] = {
                    "value": value,
                    "confidence": confidence,
                    "gap": value_gap,
                    "weight": weight,
                }

        if not methods:
            return json.dumps(
                {
                    "signal": "neutral",
                    "confidence": 0,
                    "weighted_value_gap": 0,
                    "details": "No valid valuation methods",
                }
            )

        # Calculate weighted metrics
        total_weight = sum(m["weight"] for m in methods.values())
        weighted_gap = (
            sum(m["gap"] * m["weight"] for m in methods.values()) / total_weight
        )
        weighted_confidence = (
            sum(m["confidence"] * m["weight"] for m in methods.values()) / total_weight
        )

        # Generate signal
        if weighted_gap > 0.15:  # >15% upside
            signal = "bullish"
        elif weighted_gap < -0.15:  # >15% downside
            signal = "bearish"
        else:
            signal = "neutral"

        # Calculate intrinsic value estimate
        weighted_value = (
            sum(m["value"] * m["weight"] for m in methods.values()) / total_weight
        )

        # Method agreement analysis
        gaps = [m["gap"] for m in methods.values()]
        gap_std = statistics.stdev(gaps) if len(gaps) > 1 else 0
        agreement_factor = max(
            0.5, 1 - (gap_std * 2)
        )  # Reduce confidence if methods disagree

        final_confidence = min(90, weighted_confidence * agreement_factor)

        # Key insights
        bullish_methods = [name for name, data in methods.items() if data["gap"] > 0.1]
        bearish_methods = [name for name, data in methods.items() if data["gap"] < -0.1]

        return json.dumps(
            {
                "signal": signal,
                "confidence": round(final_confidence, 1),
                "weighted_value_gap": round(weighted_gap, 3),
                "intrinsic_value_estimate": round(weighted_value, 0),
                "method_agreement": round(agreement_factor, 2),
                "bullish_methods": bullish_methods,
                "bearish_methods": bearish_methods,
                "methods_used": list(methods.keys()),
                "details": f"Weighted gap: {weighted_gap:.1%}, Methods: {len(methods)}, Agreement: {agreement_factor:.1%}",
            }
        )

    except Exception as e:
        return json.dumps(
            {
                "signal": "neutral",
                "confidence": 0,
                "weighted_value_gap": 0,
                "details": f"Error in aggregation: {str(e)}",
            }
        )


# Helper functions


def calculate_wacc(
    financial_metrics: list,
    risk_free_rate: float = 0.045,
    market_risk_premium: float = 0.06,
) -> float:
    """Calculate Weighted Average Cost of Capital"""
    if not financial_metrics:
        return 0.10  # Default WACC

    current = financial_metrics[0]
    market_cap = current.get("market_cap", 0)

    # Estimate cost of equity (simplified CAPM)
    beta = 1.0  # Default beta
    cost_of_equity = risk_free_rate + beta * market_risk_premium

    # If we have debt information, calculate WACC
    debt_to_equity = current.get("debt_to_equity", 0)
    if debt_to_equity and debt_to_equity > 0:
        # Estimate cost of debt
        interest_coverage = current.get("interest_coverage", 10)
        if interest_coverage and interest_coverage > 0:
            cost_of_debt = risk_free_rate + max(0.01, 3.0 / interest_coverage)
        else:
            cost_of_debt = risk_free_rate + 0.03

        # Calculate weights
        weight_equity = 1 / (1 + debt_to_equity)
        weight_debt = debt_to_equity / (1 + debt_to_equity)

        # WACC with tax shield (assume 25% tax rate)
        wacc = (weight_equity * cost_of_equity) + (weight_debt * cost_of_debt * 0.75)
    else:
        wacc = cost_of_equity

    return max(0.06, min(0.20, wacc))  # Reasonable bounds


def calculate_dcf_value(
    base_fcf: float,
    growth_rate: float,
    transition_rate: float,
    terminal_growth: float,
    discount_rate: float,
) -> float:
    """Calculate DCF value with multi-stage growth"""
    if base_fcf <= 0 or discount_rate <= terminal_growth:
        return 0

    pv = 0

    # High growth stage (years 1-3)
    for year in range(1, 4):
        fcf = base_fcf * (1 + growth_rate) ** year
        pv += fcf / (1 + discount_rate) ** year

    # Transition stage (years 4-7)
    for year in range(4, 8):
        declining_growth = transition_rate * (8 - year) / 4
        fcf = base_fcf * (1 + growth_rate) ** 3 * (1 + declining_growth) ** (year - 3)
        pv += fcf / (1 + discount_rate) ** year

    # Terminal value
    final_fcf = base_fcf * (1 + growth_rate) ** 3 * (1 + transition_rate) ** 4
    terminal_value = (final_fcf * (1 + terminal_growth)) / (
        discount_rate - terminal_growth
    )
    pv_terminal = terminal_value / (1 + discount_rate) ** 7

    return pv + pv_terminal


def calculate_fcf_quality(fcf_history: list) -> float:
    """Calculate free cash flow quality score (0-1)"""
    if len(fcf_history) < 3:
        return 0.5

    # Consistency score
    positive_years = sum(1 for fcf in fcf_history if fcf > 0)
    consistency = positive_years / len(fcf_history)

    # Growth stability
    if len(fcf_history) > 1:
        try:
            growth_rates = []
            for i in range(1, len(fcf_history)):
                if fcf_history[i] > 0:
                    growth_rate = (fcf_history[i - 1] / fcf_history[i]) - 1
                    if abs(growth_rate) < 2.0:  # Filter extreme values
                        growth_rates.append(growth_rate)

            if growth_rates:
                stability = max(0, 1 - (statistics.stdev(growth_rates) / 0.5))
            else:
                stability = 0.3
        except:
            stability = 0.3
    else:
        stability = 0.5

    # Combined quality score
    return (consistency * 0.6) + (stability * 0.4)
