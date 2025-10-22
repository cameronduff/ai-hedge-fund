import json
import numpy as np
import pandas as pd
from typing import Dict, List, Optional


def calculate_volatility_metrics(prices_data: str, lookback_days: int = 60) -> str:
    """
    Calculate comprehensive volatility metrics from price data.

    Args:
        prices_data: JSON string containing price data with 'close' prices
        lookback_days: Number of recent days to use for volatility calculation

    Returns:
        JSON string with volatility analysis
    """
    try:
        # Parse the price data
        prices_dict = json.loads(prices_data)

        if not prices_dict or "close" not in prices_dict:
            return json.dumps(
                {
                    "daily_volatility": 0.05,
                    "annualized_volatility": 0.05 * np.sqrt(252),
                    "volatility_percentile": 100,
                    "data_points": 0,
                    "error": "No close price data provided",
                }
            )

        # Convert to pandas Series for analysis
        close_prices = pd.Series(prices_dict["close"])

        if len(close_prices) < 2:
            return json.dumps(
                {
                    "daily_volatility": 0.05,
                    "annualized_volatility": 0.05 * np.sqrt(252),
                    "volatility_percentile": 100,
                    "data_points": len(close_prices),
                }
            )

        # Calculate daily returns
        daily_returns = close_prices.pct_change().dropna()

        if len(daily_returns) < 2:
            return json.dumps(
                {
                    "daily_volatility": 0.05,
                    "annualized_volatility": 0.05 * np.sqrt(252),
                    "volatility_percentile": 100,
                    "data_points": len(daily_returns),
                }
            )

        # Use the most recent lookback_days for volatility calculation
        recent_returns = daily_returns.tail(min(lookback_days, len(daily_returns)))

        # Calculate volatility metrics
        daily_vol = recent_returns.std()
        annualized_vol = daily_vol * np.sqrt(252)  # Annualize assuming 252 trading days

        # Calculate percentile rank of recent volatility vs historical volatility
        if (
            len(daily_returns) >= 30
        ):  # Need sufficient history for percentile calculation
            # Calculate 30-day rolling volatility for the full history
            rolling_vol = daily_returns.rolling(window=30).std().dropna()
            if len(rolling_vol) > 0:
                # Compare current volatility against historical rolling volatilities
                current_vol_percentile = (rolling_vol <= daily_vol).mean() * 100
            else:
                current_vol_percentile = 50  # Default to median
        else:
            current_vol_percentile = 50  # Default to median if insufficient data

        analysis = {
            "daily_volatility": float(daily_vol) if not np.isnan(daily_vol) else 0.025,
            "annualized_volatility": (
                float(annualized_vol) if not np.isnan(annualized_vol) else 0.25
            ),
            "volatility_percentile": (
                float(current_vol_percentile)
                if not np.isnan(current_vol_percentile)
                else 50.0
            ),
            "data_points": len(recent_returns),
            "volatility_regime": (
                "Low"
                if annualized_vol < 0.15
                else (
                    "Medium"
                    if annualized_vol < 0.30
                    else "High" if annualized_vol < 0.50 else "Very High"
                )
            ),
        }

        return json.dumps(analysis)

    except Exception as e:
        return json.dumps(
            {
                "daily_volatility": 0.05,
                "annualized_volatility": 0.25,
                "volatility_percentile": 100,
                "data_points": 0,
                "error": f"Error calculating volatility: {str(e)}",
            }
        )


def calculate_volatility_adjusted_limit(annualized_volatility: float) -> str:
    """
    Calculate position limit as percentage of portfolio based on volatility.

    Args:
        annualized_volatility: Annual volatility as a decimal (e.g., 0.25 for 25%)

    Returns:
        JSON string with position limit analysis
    """
    try:
        base_limit = 0.20  # 20% baseline

        if annualized_volatility < 0.15:  # Low volatility
            # Allow higher allocation for stable stocks
            vol_multiplier = 1.25  # Up to 25%
            risk_category = "Low Risk"
            explanation = "Low volatility allows increased allocation"
        elif annualized_volatility < 0.30:  # Medium volatility
            # Standard allocation with slight adjustment based on volatility
            vol_multiplier = 1.0 - (annualized_volatility - 0.15) * 0.5  # 20% -> 12.5%
            risk_category = "Medium Risk"
            explanation = "Medium volatility with standard allocation adjustment"
        elif annualized_volatility < 0.50:  # High volatility
            # Reduce allocation significantly
            vol_multiplier = 0.75 - (annualized_volatility - 0.30) * 0.5  # 15% -> 5%
            risk_category = "High Risk"
            explanation = "High volatility requires significant allocation reduction"
        else:  # Very high volatility (>50%)
            # Minimum allocation for very risky stocks
            vol_multiplier = 0.50  # Max 10%
            risk_category = "Very High Risk"
            explanation = "Very high volatility limited to minimum allocation"

        # Apply bounds to ensure reasonable limits
        vol_multiplier = max(0.25, min(1.25, vol_multiplier))  # 5% to 25% range
        position_limit_pct = base_limit * vol_multiplier

        analysis = {
            "base_limit_pct": base_limit,
            "volatility_multiplier": vol_multiplier,
            "position_limit_pct": position_limit_pct,
            "risk_category": risk_category,
            "explanation": explanation,
            "volatility_level": f"{annualized_volatility:.1%}",
        }

        return json.dumps(analysis)

    except Exception as e:
        return json.dumps(
            {
                "base_limit_pct": 0.20,
                "volatility_multiplier": 1.0,
                "position_limit_pct": 0.20,
                "risk_category": "Unknown",
                "explanation": f"Error in calculation: {str(e)}",
                "volatility_level": "Unknown",
            }
        )


def analyze_correlation_risk(returns_data: str, active_positions: str) -> str:
    """
    Analyze correlation risk between securities.

    Args:
        returns_data: JSON string with returns data for multiple tickers
        active_positions: JSON string with list of tickers that have active positions

    Returns:
        JSON string with correlation analysis
    """
    try:
        returns_dict = json.loads(returns_data)
        active_tickers = json.loads(active_positions)

        if not returns_dict or len(returns_dict) < 2:
            return json.dumps(
                {
                    "correlation_matrix": {},
                    "avg_correlations": {},
                    "max_correlations": {},
                    "risk_assessment": "Insufficient data for correlation analysis",
                }
            )

        # Convert to DataFrame
        returns_df = pd.DataFrame(returns_dict).dropna(how="any")

        if returns_df.shape[1] < 2 or returns_df.shape[0] < 5:
            return json.dumps(
                {
                    "correlation_matrix": {},
                    "avg_correlations": {},
                    "max_correlations": {},
                    "risk_assessment": "Insufficient data points for reliable correlation analysis",
                }
            )

        # Calculate correlation matrix
        correlation_matrix = returns_df.corr()

        # Analyze correlations for each ticker
        correlation_analysis = {}

        for ticker in correlation_matrix.columns:
            # Get correlations with other tickers (excluding self)
            other_tickers = [t for t in correlation_matrix.columns if t != ticker]

            if other_tickers:
                correlations = correlation_matrix.loc[ticker, other_tickers].dropna()

                if len(correlations) > 0:
                    avg_corr = float(correlations.mean())
                    max_corr = float(correlations.max())

                    # Calculate correlation multiplier
                    if avg_corr >= 0.80:
                        corr_multiplier = 0.70
                        risk_level = "Very High"
                    elif avg_corr >= 0.60:
                        corr_multiplier = 0.85
                        risk_level = "High"
                    elif avg_corr >= 0.40:
                        corr_multiplier = 1.00
                        risk_level = "Medium"
                    elif avg_corr >= 0.20:
                        corr_multiplier = 1.05
                        risk_level = "Low"
                    else:
                        corr_multiplier = 1.10
                        risk_level = "Very Low"

                    # Top correlated tickers
                    top_correlated = correlations.sort_values(ascending=False).head(3)

                    correlation_analysis[ticker] = {
                        "avg_correlation": avg_corr,
                        "max_correlation": max_corr,
                        "correlation_multiplier": corr_multiplier,
                        "risk_level": risk_level,
                        "top_correlations": {
                            str(t): float(c) for t, c in top_correlated.items()
                        },
                    }

        analysis = {
            "correlation_matrix": correlation_matrix.to_dict(),
            "ticker_analysis": correlation_analysis,
            "active_positions": active_tickers,
            "analysis_quality": f"Based on {returns_df.shape[0]} data points across {returns_df.shape[1]} tickers",
        }

        return json.dumps(analysis, default=str)

    except Exception as e:
        return json.dumps(
            {
                "correlation_matrix": {},
                "ticker_analysis": {},
                "active_positions": [],
                "error": f"Error in correlation analysis: {str(e)}",
            }
        )


def calculate_position_limits(
    portfolio_data: str, price_data: str, volatility_data: str
) -> str:
    """
    Calculate comprehensive position limits based on portfolio value, volatility, and current positions.

    Args:
        portfolio_data: JSON string with portfolio information (cash, positions, etc.)
        price_data: JSON string with current prices for all tickers
        volatility_data: JSON string with volatility metrics for all tickers

    Returns:
        JSON string with position limit analysis
    """
    try:
        portfolio = json.loads(portfolio_data)
        prices = json.loads(price_data)
        volatilities = json.loads(volatility_data)

        # Calculate total portfolio value
        total_portfolio_value = portfolio.get("cash", 0.0)

        for ticker, position in portfolio.get("positions", {}).items():
            if ticker in prices:
                # Add market value of long positions
                total_portfolio_value += position.get("long", 0) * prices[ticker]
                # Subtract market value of short positions (they're liabilities)
                total_portfolio_value -= position.get("short", 0) * prices[ticker]

        position_limits = {}

        for ticker in prices:
            if ticker in volatilities:
                current_price = prices[ticker]
                vol_data = volatilities[ticker]

                # Current position value
                position = portfolio.get("positions", {}).get(ticker, {})
                long_value = position.get("long", 0) * current_price
                short_value = position.get("short", 0) * current_price
                current_position_value = abs(long_value - short_value)

                # Calculate volatility-adjusted limit
                annualized_vol = vol_data.get("annualized_volatility", 0.25)
                base_limit_pct = 0.20  # 20% baseline

                # Volatility adjustment
                if annualized_vol < 0.15:
                    vol_multiplier = 1.25
                elif annualized_vol < 0.30:
                    vol_multiplier = 1.0 - (annualized_vol - 0.15) * 0.5
                elif annualized_vol < 0.50:
                    vol_multiplier = 0.75 - (annualized_vol - 0.30) * 0.5
                else:
                    vol_multiplier = 0.50

                vol_multiplier = max(0.25, min(1.25, vol_multiplier))
                position_limit_pct = base_limit_pct * vol_multiplier
                position_limit_dollars = total_portfolio_value * position_limit_pct

                # Calculate remaining limit
                remaining_limit = position_limit_dollars - current_position_value
                max_position_size = min(remaining_limit, portfolio.get("cash", 0))

                position_limits[ticker] = {
                    "current_price": current_price,
                    "current_position_value": current_position_value,
                    "position_limit_pct": position_limit_pct,
                    "position_limit_dollars": position_limit_dollars,
                    "remaining_limit": remaining_limit,
                    "max_new_position": max(0, max_position_size),
                    "volatility_multiplier": vol_multiplier,
                    "annualized_volatility": annualized_vol,
                }

        analysis = {
            "total_portfolio_value": total_portfolio_value,
            "available_cash": portfolio.get("cash", 0),
            "position_limits": position_limits,
            "summary": f"Portfolio value: ${total_portfolio_value:,.2f}, Available cash: ${portfolio.get('cash', 0):,.2f}",
        }

        return json.dumps(analysis)

    except Exception as e:
        return json.dumps(
            {
                "total_portfolio_value": 0,
                "available_cash": 0,
                "position_limits": {},
                "error": f"Error calculating position limits: {str(e)}",
            }
        )


def assess_portfolio_risk_concentration(
    portfolio_data: str, correlation_data: str
) -> str:
    """
    Assess overall portfolio risk concentration and diversification.

    Args:
        portfolio_data: JSON string with current portfolio positions
        correlation_data: JSON string with correlation analysis

    Returns:
        JSON string with portfolio risk assessment
    """
    try:
        portfolio = json.loads(portfolio_data)
        correlations = json.loads(correlation_data)

        positions = portfolio.get("positions", {})
        total_positions = len(
            [
                p
                for p in positions.values()
                if abs(p.get("long", 0) - p.get("short", 0)) > 0
            ]
        )

        # Analyze concentration risk
        if total_positions == 0:
            concentration_risk = "None - No positions"
        elif total_positions == 1:
            concentration_risk = "Very High - Single position"
        elif total_positions <= 3:
            concentration_risk = "High - Few positions"
        elif total_positions <= 7:
            concentration_risk = "Medium - Moderate diversification"
        else:
            concentration_risk = "Low - Well diversified"

        # Analyze correlation risk from correlation data
        correlation_risk = "Unknown"
        if "ticker_analysis" in correlations:
            high_corr_pairs = 0
            total_pairs = 0

            for ticker, analysis in correlations["ticker_analysis"].items():
                if ticker in positions:
                    avg_corr = analysis.get("avg_correlation", 0)
                    if avg_corr > 0.6:
                        high_corr_pairs += 1
                    total_pairs += 1

            if total_pairs > 0:
                high_corr_ratio = high_corr_pairs / total_pairs
                if high_corr_ratio > 0.7:
                    correlation_risk = "Very High - Many highly correlated positions"
                elif high_corr_ratio > 0.5:
                    correlation_risk = "High - Several correlated positions"
                elif high_corr_ratio > 0.3:
                    correlation_risk = "Medium - Some correlation present"
                else:
                    correlation_risk = "Low - Low correlation between positions"

        # Overall risk assessment
        risk_factors = []
        if "Very High" in concentration_risk or "High" in concentration_risk:
            risk_factors.append("concentration")
        if "Very High" in correlation_risk or "High" in correlation_risk:
            risk_factors.append("correlation")

        if len(risk_factors) >= 2:
            overall_risk = "Very High"
        elif len(risk_factors) == 1:
            overall_risk = "High"
        elif "Medium" in concentration_risk or "Medium" in correlation_risk:
            overall_risk = "Medium"
        else:
            overall_risk = "Low"

        assessment = {
            "total_positions": total_positions,
            "concentration_risk": concentration_risk,
            "correlation_risk": correlation_risk,
            "overall_risk": overall_risk,
            "risk_factors": risk_factors,
            "recommendations": [],
        }

        # Add recommendations
        if total_positions < 5:
            assessment["recommendations"].append(
                "Consider increasing diversification with additional positions"
            )

        if "High" in correlation_risk:
            assessment["recommendations"].append(
                "Reduce correlation risk by diversifying across uncorrelated assets"
            )

        if overall_risk in ["Very High", "High"]:
            assessment["recommendations"].append(
                "Consider reducing position sizes or increasing diversification"
            )

        return json.dumps(assessment)

    except Exception as e:
        return json.dumps(
            {
                "total_positions": 0,
                "concentration_risk": "Unknown",
                "correlation_risk": "Unknown",
                "overall_risk": "Unknown",
                "error": f"Error assessing portfolio risk: {str(e)}",
            }
        )
