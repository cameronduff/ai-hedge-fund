from typing import Dict, Any
import json


def analyze_signal_consensus(signals_data: str) -> str:
    """
    Analyze consensus across multiple analyst signals for a ticker.

    Args:
        signals_data: JSON string containing analyst signals with format:
                     {"agent_name": {"sig": "bullish/bearish/neutral", "conf": confidence_score}}

    Returns:
        Analysis of signal consensus and weighted recommendation
    """
    try:
        signals = json.loads(signals_data)
        if not signals:
            return "No signals available for analysis"

        total_weight = 0
        bullish_weight = 0
        bearish_weight = 0
        neutral_weight = 0

        signal_summary = []

        for agent, data in signals.items():
            sig = data.get("sig", "neutral")
            conf = data.get("conf", 0)

            signal_summary.append(f"{agent}: {sig} ({conf}% confidence)")

            if sig == "bullish":
                bullish_weight += conf
            elif sig == "bearish":
                bearish_weight += conf
            else:
                neutral_weight += conf

            total_weight += conf

        if total_weight == 0:
            consensus = "neutral"
            strength = 0
        else:
            if bullish_weight > bearish_weight and bullish_weight > neutral_weight:
                consensus = "bullish"
                strength = bullish_weight / total_weight * 100
            elif bearish_weight > bullish_weight and bearish_weight > neutral_weight:
                consensus = "bearish"
                strength = bearish_weight / total_weight * 100
            else:
                consensus = "neutral"
                strength = neutral_weight / total_weight * 100

        analysis = f"""
Signal Analysis:
{chr(10).join(signal_summary)}

Consensus: {consensus.upper()} (Strength: {strength:.1f}%)
- Bullish Weight: {bullish_weight:.1f}
- Bearish Weight: {bearish_weight:.1f}
- Neutral Weight: {neutral_weight:.1f}

Recommendation: {"Strong " if strength > 70 else "Moderate " if strength > 50 else "Weak "}{consensus}
"""

        return analysis.strip()

    except Exception as e:
        return f"Error analyzing signals: {str(e)}"


def calculate_position_size(
    available_actions: str, risk_tolerance: str = "moderate"
) -> str:
    """
    Calculate optimal position size based on available actions and risk tolerance.

    Args:
        available_actions: JSON string with available actions and max quantities
        risk_tolerance: "conservative", "moderate", or "aggressive"

    Returns:
        Position sizing recommendations
    """
    try:
        actions = json.loads(available_actions)

        risk_multipliers = {"conservative": 0.25, "moderate": 0.50, "aggressive": 0.75}

        multiplier = risk_multipliers.get(risk_tolerance, 0.50)
        recommendations = {}

        for action, max_qty in actions.items():
            if action == "hold":
                continue

            if max_qty > 0:
                # Calculate recommended position size based on risk tolerance
                if max_qty <= 10:
                    # Small position limits - use higher percentage
                    recommended = max(1, int(max_qty * (multiplier + 0.2)))
                else:
                    recommended = max(1, int(max_qty * multiplier))

                recommendations[action] = {
                    "max_quantity": max_qty,
                    "recommended_quantity": min(recommended, max_qty),
                    "risk_level": risk_tolerance,
                }

        if not recommendations:
            return "No actionable positions available - recommend HOLD"

        analysis = f"Position Sizing Analysis (Risk Tolerance: {risk_tolerance}):\n"
        for action, data in recommendations.items():
            analysis += f"- {action.upper()}: Max {data['max_quantity']}, Recommended {data['recommended_quantity']} shares\n"

        return analysis.strip()

    except Exception as e:
        return f"Error calculating position size: {str(e)}"


def assess_portfolio_risk(current_portfolio: str, proposed_trades: str) -> str:
    """
    Assess portfolio risk impact of proposed trades.

    Args:
        current_portfolio: JSON string with current portfolio state
        proposed_trades: JSON string with proposed trading decisions

    Returns:
        Risk assessment analysis
    """
    try:
        portfolio = json.loads(current_portfolio)
        trades = json.loads(proposed_trades)

        cash = portfolio.get("cash", 0)
        equity = portfolio.get("equity", cash)
        positions = portfolio.get("positions", {})

        # Calculate current portfolio metrics
        total_long_value = 0
        total_short_value = 0
        position_count = len(positions)

        for ticker, pos in positions.items():
            long_shares = pos.get("long", 0)
            short_shares = pos.get("short", 0)
            # Note: We'd need current prices to calculate exact values
            # This is a simplified risk assessment

        # Analyze proposed trades
        trade_analysis = []
        new_positions = 0

        for ticker, decision in trades.items():
            action = decision.get("action", "hold")
            quantity = decision.get("quantity", 0)
            confidence = decision.get("confidence", 0)

            if action != "hold" and quantity > 0:
                risk_level = (
                    "High"
                    if confidence < 60
                    else "Medium" if confidence < 80 else "Low"
                )
                trade_analysis.append(
                    f"{ticker}: {action.upper()} {quantity} shares (Risk: {risk_level}, Confidence: {confidence}%)"
                )

                if ticker not in positions or positions[ticker].get("long", 0) == 0:
                    new_positions += 1

        # Portfolio concentration analysis
        concentration_risk = (
            "High" if new_positions > 5 else "Medium" if new_positions > 2 else "Low"
        )

        analysis = f"""
Portfolio Risk Assessment:
Current Positions: {position_count}
Available Cash: ${cash:,.2f}
Portfolio Equity: ${equity:,.2f}

Proposed Trades:
{chr(10).join(trade_analysis) if trade_analysis else "No active trades proposed"}

New Positions: {new_positions}
Concentration Risk: {concentration_risk}
Overall Risk Level: {"High" if len(trade_analysis) > 5 or concentration_risk == "High" else "Moderate"}

Recommendations:
- {"Reduce position sizes" if concentration_risk == "High" else "Position sizes appropriate"}
- {"Maintain cash reserves" if cash < equity * 0.1 else "Adequate liquidity"}
- {"Diversify across sectors" if new_positions > 3 else "Reasonable diversification"}
"""

        return analysis.strip()

    except Exception as e:
        return f"Error assessing portfolio risk: {str(e)}"


def optimize_trade_timing(market_conditions: str) -> str:
    """
    Provide trade timing recommendations based on market conditions.

    Args:
        market_conditions: Description of current market conditions

    Returns:
        Trade timing analysis and recommendations
    """
    conditions_lower = market_conditions.lower()

    # Analyze market conditions for timing
    if any(
        word in conditions_lower for word in ["volatile", "uncertainty", "unstable"]
    ):
        timing = (
            "Exercise caution - consider smaller position sizes and gradual entries"
        )
        risk_level = "High"
    elif any(word in conditions_lower for word in ["stable", "trending", "momentum"]):
        timing = "Favorable for position entries - normal position sizing appropriate"
        risk_level = "Low"
    elif any(
        word in conditions_lower for word in ["mixed", "sideways", "consolidation"]
    ):
        timing = "Neutral conditions - be selective with high-conviction trades only"
        risk_level = "Medium"
    else:
        timing = "Assess individual opportunities - no clear market bias"
        risk_level = "Medium"

    analysis = f"""
Market Timing Analysis:

Current Conditions: {market_conditions}
Risk Level: {risk_level}

Timing Recommendation: {timing}

Strategy Adjustments:
- Entry Strategy: {"Gradual/scaled entries" if risk_level == "High" else "Normal entries"}
- Position Sizing: {"Reduced size" if risk_level == "High" else "Standard size"}
- Exit Strategy: {"Tight stops recommended" if risk_level == "High" else "Normal stop levels"}
- Time Horizon: {"Short to medium term" if risk_level == "High" else "Medium to long term"}
"""

    return analysis.strip()
