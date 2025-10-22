import json
from typing import Dict, Any, Optional


def analyze_profitability_metrics(financial_data: str) -> str:
    """
    Analyze profitability metrics from financial data.

    Args:
        financial_data: JSON string containing financial metrics including ROE, net_margin, operating_margin

    Returns:
        JSON string with profitability analysis
    """
    try:
        metrics = json.loads(financial_data)

        return_on_equity = metrics.get("return_on_equity")
        net_margin = metrics.get("net_margin")
        operating_margin = metrics.get("operating_margin")

        # Define thresholds for strong profitability
        roe_threshold = 0.15  # 15%
        net_margin_threshold = 0.20  # 20%
        operating_margin_threshold = 0.15  # 15%

        profitability_score = 0
        details = []

        # Analyze ROE
        if return_on_equity is not None:
            if return_on_equity > roe_threshold:
                profitability_score += 1
                details.append(f"Strong ROE: {return_on_equity:.2%}")
            else:
                details.append(f"Weak ROE: {return_on_equity:.2%}")
        else:
            details.append("ROE: N/A")

        # Analyze Net Margin
        if net_margin is not None:
            if net_margin > net_margin_threshold:
                profitability_score += 1
                details.append(f"Strong Net Margin: {net_margin:.2%}")
            else:
                details.append(f"Weak Net Margin: {net_margin:.2%}")
        else:
            details.append("Net Margin: N/A")

        # Analyze Operating Margin
        if operating_margin is not None:
            if operating_margin > operating_margin_threshold:
                profitability_score += 1
                details.append(f"Strong Operating Margin: {operating_margin:.2%}")
            else:
                details.append(f"Weak Operating Margin: {operating_margin:.2%}")
        else:
            details.append("Operating Margin: N/A")

        # Determine signal
        if profitability_score >= 2:
            signal = "bullish"
            interpretation = "Strong profitability across multiple metrics"
        elif profitability_score == 0:
            signal = "bearish"
            interpretation = "Weak profitability indicators"
        else:
            signal = "neutral"
            interpretation = "Mixed profitability signals"

        analysis = {
            "signal": signal,
            "profitability_score": profitability_score,
            "max_score": 3,
            "details": ", ".join(details),
            "interpretation": interpretation,
            "metrics": {
                "return_on_equity": return_on_equity,
                "net_margin": net_margin,
                "operating_margin": operating_margin,
            },
        }

        return json.dumps(analysis)

    except Exception as e:
        return json.dumps(
            {
                "signal": "neutral",
                "error": f"Error analyzing profitability: {str(e)}",
                "details": "Unable to analyze profitability metrics",
            }
        )


def analyze_growth_metrics(financial_data: str) -> str:
    """
    Analyze growth metrics from financial data.

    Args:
        financial_data: JSON string containing growth metrics

    Returns:
        JSON string with growth analysis
    """
    try:
        metrics = json.loads(financial_data)

        revenue_growth = metrics.get("revenue_growth")
        earnings_growth = metrics.get("earnings_growth")
        book_value_growth = metrics.get("book_value_growth")

        growth_threshold = 0.10  # 10% growth threshold

        growth_score = 0
        details = []

        # Analyze Revenue Growth
        if revenue_growth is not None:
            if revenue_growth > growth_threshold:
                growth_score += 1
                details.append(f"Strong Revenue Growth: {revenue_growth:.2%}")
            else:
                details.append(f"Weak Revenue Growth: {revenue_growth:.2%}")
        else:
            details.append("Revenue Growth: N/A")

        # Analyze Earnings Growth
        if earnings_growth is not None:
            if earnings_growth > growth_threshold:
                growth_score += 1
                details.append(f"Strong Earnings Growth: {earnings_growth:.2%}")
            else:
                details.append(f"Weak Earnings Growth: {earnings_growth:.2%}")
        else:
            details.append("Earnings Growth: N/A")

        # Analyze Book Value Growth
        if book_value_growth is not None:
            if book_value_growth > growth_threshold:
                growth_score += 1
                details.append(f"Strong Book Value Growth: {book_value_growth:.2%}")
            else:
                details.append(f"Weak Book Value Growth: {book_value_growth:.2%}")
        else:
            details.append("Book Value Growth: N/A")

        # Determine signal
        if growth_score >= 2:
            signal = "bullish"
            interpretation = "Strong growth momentum across multiple metrics"
        elif growth_score == 0:
            signal = "bearish"
            interpretation = "Weak or declining growth"
        else:
            signal = "neutral"
            interpretation = "Mixed growth signals"

        analysis = {
            "signal": signal,
            "growth_score": growth_score,
            "max_score": 3,
            "details": ", ".join(details),
            "interpretation": interpretation,
            "metrics": {
                "revenue_growth": revenue_growth,
                "earnings_growth": earnings_growth,
                "book_value_growth": book_value_growth,
            },
        }

        return json.dumps(analysis)

    except Exception as e:
        return json.dumps(
            {
                "signal": "neutral",
                "error": f"Error analyzing growth: {str(e)}",
                "details": "Unable to analyze growth metrics",
            }
        )


def analyze_financial_health(financial_data: str) -> str:
    """
    Analyze financial health and stability metrics.

    Args:
        financial_data: JSON string containing financial health metrics

    Returns:
        JSON string with financial health analysis
    """
    try:
        metrics = json.loads(financial_data)

        current_ratio = metrics.get("current_ratio")
        debt_to_equity = metrics.get("debt_to_equity")
        free_cash_flow_per_share = metrics.get("free_cash_flow_per_share")
        earnings_per_share = metrics.get("earnings_per_share")

        health_score = 0
        details = []

        # Analyze Current Ratio (Liquidity)
        if current_ratio is not None:
            if current_ratio > 1.5:
                health_score += 1
                details.append(f"Strong Liquidity: Current Ratio {current_ratio:.2f}")
            else:
                details.append(f"Weak Liquidity: Current Ratio {current_ratio:.2f}")
        else:
            details.append("Current Ratio: N/A")

        # Analyze Debt-to-Equity (Leverage)
        if debt_to_equity is not None:
            if debt_to_equity < 0.5:
                health_score += 1
                details.append(f"Conservative Debt: D/E {debt_to_equity:.2f}")
            else:
                details.append(f"High Debt: D/E {debt_to_equity:.2f}")
        else:
            details.append("D/E Ratio: N/A")

        # Analyze Free Cash Flow Conversion
        if (
            free_cash_flow_per_share is not None
            and earnings_per_share is not None
            and earnings_per_share > 0
        ):
            fcf_conversion = free_cash_flow_per_share / earnings_per_share
            if fcf_conversion > 0.8:
                health_score += 1
                details.append(f"Strong FCF Conversion: {fcf_conversion:.1%}")
            else:
                details.append(f"Weak FCF Conversion: {fcf_conversion:.1%}")
        else:
            details.append("FCF Conversion: N/A")

        # Determine signal
        if health_score >= 2:
            signal = "bullish"
            interpretation = "Strong financial health and stability"
        elif health_score == 0:
            signal = "bearish"
            interpretation = "Poor financial health indicators"
        else:
            signal = "neutral"
            interpretation = "Adequate financial health"

        analysis = {
            "signal": signal,
            "health_score": health_score,
            "max_score": 3,
            "details": ", ".join(details),
            "interpretation": interpretation,
            "metrics": {
                "current_ratio": current_ratio,
                "debt_to_equity": debt_to_equity,
                "fcf_per_share": free_cash_flow_per_share,
                "eps": earnings_per_share,
            },
        }

        return json.dumps(analysis)

    except Exception as e:
        return json.dumps(
            {
                "signal": "neutral",
                "error": f"Error analyzing financial health: {str(e)}",
                "details": "Unable to analyze financial health metrics",
            }
        )


def analyze_valuation_ratios(financial_data: str) -> str:
    """
    Analyze valuation ratios to assess if stock is overvalued or undervalued.

    Args:
        financial_data: JSON string containing valuation ratios

    Returns:
        JSON string with valuation analysis
    """
    try:
        metrics = json.loads(financial_data)

        pe_ratio = metrics.get("price_to_earnings_ratio")
        pb_ratio = metrics.get("price_to_book_ratio")
        ps_ratio = metrics.get("price_to_sales_ratio")

        # Define thresholds for reasonable valuations
        pe_threshold = 25
        pb_threshold = 3
        ps_threshold = 5

        overvaluation_score = 0
        details = []

        # Analyze P/E Ratio
        if pe_ratio is not None:
            if pe_ratio > pe_threshold:
                overvaluation_score += 1
                details.append(f"High P/E: {pe_ratio:.2f}")
            else:
                details.append(f"Reasonable P/E: {pe_ratio:.2f}")
        else:
            details.append("P/E: N/A")

        # Analyze P/B Ratio
        if pb_ratio is not None:
            if pb_ratio > pb_threshold:
                overvaluation_score += 1
                details.append(f"High P/B: {pb_ratio:.2f}")
            else:
                details.append(f"Reasonable P/B: {pb_ratio:.2f}")
        else:
            details.append("P/B: N/A")

        # Analyze P/S Ratio
        if ps_ratio is not None:
            if ps_ratio > ps_threshold:
                overvaluation_score += 1
                details.append(f"High P/S: {ps_ratio:.2f}")
            else:
                details.append(f"Reasonable P/S: {ps_ratio:.2f}")
        else:
            details.append("P/S: N/A")

        # Determine signal (note: high valuation ratios are bearish)
        if overvaluation_score >= 2:
            signal = "bearish"
            interpretation = "Appears overvalued based on multiple metrics"
        elif overvaluation_score == 0:
            signal = "bullish"
            interpretation = "Appears reasonably valued or undervalued"
        else:
            signal = "neutral"
            interpretation = "Mixed valuation signals"

        analysis = {
            "signal": signal,
            "overvaluation_score": overvaluation_score,
            "max_score": 3,
            "details": ", ".join(details),
            "interpretation": interpretation,
            "metrics": {
                "pe_ratio": pe_ratio,
                "pb_ratio": pb_ratio,
                "ps_ratio": ps_ratio,
            },
        }

        return json.dumps(analysis)

    except Exception as e:
        return json.dumps(
            {
                "signal": "neutral",
                "error": f"Error analyzing valuation: {str(e)}",
                "details": "Unable to analyze valuation ratios",
            }
        )


def calculate_fundamental_score(analysis_results: str) -> str:
    """
    Calculate overall fundamental score and signal from individual analysis components.

    Args:
        analysis_results: JSON string containing results from all fundamental analysis components

    Returns:
        JSON string with overall fundamental assessment
    """
    try:
        results = json.loads(analysis_results)

        signals = []
        component_details = {}

        # Extract signals from each component
        for component in ["profitability", "growth", "financial_health", "valuation"]:
            if component in results:
                component_signal = results[component].get("signal", "neutral")
                signals.append(component_signal)
                component_details[component] = {
                    "signal": component_signal,
                    "details": results[component].get("details", ""),
                    "interpretation": results[component].get("interpretation", ""),
                }

        # Count signal types
        bullish_count = signals.count("bullish")
        bearish_count = signals.count("bearish")
        neutral_count = signals.count("neutral")
        total_signals = len(signals)

        # Determine overall signal
        if bullish_count > bearish_count:
            overall_signal = "bullish"
            confidence = (bullish_count / total_signals) * 100
        elif bearish_count > bullish_count:
            overall_signal = "bearish"
            confidence = (bearish_count / total_signals) * 100
        else:
            overall_signal = "neutral"
            confidence = (
                max(bullish_count, bearish_count, neutral_count) / total_signals
            ) * 100

        # Create summary
        summary_parts = []
        if bullish_count > 0:
            summary_parts.append(f"{bullish_count} bullish signals")
        if bearish_count > 0:
            summary_parts.append(f"{bearish_count} bearish signals")
        if neutral_count > 0:
            summary_parts.append(f"{neutral_count} neutral signals")

        summary = f"Overall: {overall_signal.upper()} ({', '.join(summary_parts)})"

        analysis = {
            "overall_signal": overall_signal,
            "confidence": round(confidence, 1),
            "signal_breakdown": {
                "bullish": bullish_count,
                "bearish": bearish_count,
                "neutral": neutral_count,
                "total": total_signals,
            },
            "component_details": component_details,
            "summary": summary,
            "recommendation": (
                "Strong fundamental buy candidate"
                if overall_signal == "bullish" and confidence > 75
                else (
                    "Fundamental buy candidate"
                    if overall_signal == "bullish"
                    else (
                        "Strong fundamental sell candidate"
                        if overall_signal == "bearish" and confidence > 75
                        else (
                            "Fundamental sell candidate"
                            if overall_signal == "bearish"
                            else "Mixed fundamental signals - neutral stance"
                        )
                    )
                )
            ),
        }

        return json.dumps(analysis)

    except Exception as e:
        return json.dumps(
            {
                "overall_signal": "neutral",
                "confidence": 0,
                "error": f"Error calculating fundamental score: {str(e)}",
                "summary": "Unable to calculate fundamental score",
            }
        )
