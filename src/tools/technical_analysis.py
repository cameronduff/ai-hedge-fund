import json
import math
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Tuple


def safe_float(value, default=0.0):
    """
    Safely convert a value to float, handling NaN cases

    Args:
        value: The value to convert (can be pandas scalar, numpy value, etc.)
        default: Default value to return if the input is NaN or invalid

    Returns:
        float: The converted value or default if NaN/invalid
    """
    try:
        if pd.isna(value) or np.isnan(value):
            return default
        return float(value)
    except (ValueError, TypeError, OverflowError):
        return default


def calculate_trend_indicators(price_data: str) -> str:
    """
    Calculate trend following indicators including EMAs and ADX.

    Args:
        price_data: JSON string containing OHLCV price data

    Returns:
        JSON string with trend analysis
    """
    try:
        data = json.loads(price_data)

        # Convert to DataFrame
        df = pd.DataFrame(data)
        if df.empty or len(df) < 55:  # Need enough data for longest EMA
            return json.dumps(
                {
                    "signal": "neutral",
                    "confidence": 0.0,
                    "error": "Insufficient data for trend analysis",
                }
            )

        # Calculate EMAs
        ema_8 = df["close"].ewm(span=8, adjust=False).mean()
        ema_21 = df["close"].ewm(span=21, adjust=False).mean()
        ema_55 = df["close"].ewm(span=55, adjust=False).mean()

        # Calculate ADX
        adx_data = calculate_adx_series(df)

        # Determine trend direction and strength
        short_trend = ema_8.iloc[-1] > ema_21.iloc[-1]
        medium_trend = ema_21.iloc[-1] > ema_55.iloc[-1]

        # Get trend strength from ADX
        adx_value = adx_data["adx"].iloc[-1] if not adx_data.empty else 20
        trend_strength = min(adx_value / 50.0, 1.0)  # Normalize ADX to 0-1

        # Determine signal
        if short_trend and medium_trend:
            signal = "bullish"
            confidence = trend_strength
        elif not short_trend and not medium_trend:
            signal = "bearish"
            confidence = trend_strength
        else:
            signal = "neutral"
            confidence = 0.5

        analysis = {
            "signal": signal,
            "confidence": confidence,
            "adx": safe_float(adx_value),
            "trend_strength": safe_float(trend_strength),
            "ema_8": safe_float(ema_8.iloc[-1]),
            "ema_21": safe_float(ema_21.iloc[-1]),
            "ema_55": safe_float(ema_55.iloc[-1]),
            "short_trend": short_trend,
            "medium_trend": medium_trend,
        }

        return json.dumps(analysis)

    except Exception as e:
        return json.dumps(
            {
                "signal": "neutral",
                "confidence": 0.0,
                "error": f"Error calculating trend indicators: {str(e)}",
            }
        )


def calculate_mean_reversion_indicators(price_data: str) -> str:
    """
    Calculate mean reversion indicators including Z-score, Bollinger Bands, and RSI.

    Args:
        price_data: JSON string containing OHLCV price data

    Returns:
        JSON string with mean reversion analysis
    """
    try:
        data = json.loads(price_data)
        df = pd.DataFrame(data)

        if df.empty or len(df) < 50:
            return json.dumps(
                {
                    "signal": "neutral",
                    "confidence": 0.0,
                    "error": "Insufficient data for mean reversion analysis",
                }
            )

        # Calculate Z-score
        ma_50 = df["close"].rolling(window=50).mean()
        std_50 = df["close"].rolling(window=50).std()
        z_score = (df["close"] - ma_50) / std_50

        # Calculate Bollinger Bands
        bb_middle = df["close"].rolling(window=20).mean()
        bb_std = df["close"].rolling(window=20).std()
        bb_upper = bb_middle + (bb_std * 2)
        bb_lower = bb_middle - (bb_std * 2)

        # Calculate price position within Bollinger Bands
        price_vs_bb = (df["close"].iloc[-1] - bb_lower.iloc[-1]) / (
            bb_upper.iloc[-1] - bb_lower.iloc[-1]
        )

        # Calculate RSI
        rsi_14 = calculate_rsi_series(df, 14)
        rsi_28 = calculate_rsi_series(df, 28)

        # Mean reversion signals
        z_current = z_score.iloc[-1]

        # Generate signal
        if z_current < -2 and price_vs_bb < 0.2:
            signal = "bullish"  # Oversold
            confidence = min(abs(z_current) / 4, 1.0)
        elif z_current > 2 and price_vs_bb > 0.8:
            signal = "bearish"  # Overbought
            confidence = min(abs(z_current) / 4, 1.0)
        else:
            signal = "neutral"
            confidence = 0.5

        analysis = {
            "signal": signal,
            "confidence": confidence,
            "z_score": safe_float(z_current),
            "price_vs_bb": safe_float(price_vs_bb),
            "rsi_14": safe_float(rsi_14.iloc[-1]),
            "rsi_28": safe_float(rsi_28.iloc[-1]),
            "bb_upper": safe_float(bb_upper.iloc[-1]),
            "bb_lower": safe_float(bb_lower.iloc[-1]),
            "bb_middle": safe_float(bb_middle.iloc[-1]),
        }

        return json.dumps(analysis)

    except Exception as e:
        return json.dumps(
            {
                "signal": "neutral",
                "confidence": 0.0,
                "error": f"Error calculating mean reversion indicators: {str(e)}",
            }
        )


def calculate_momentum_indicators(price_data: str) -> str:
    """
    Calculate momentum indicators across multiple timeframes.

    Args:
        price_data: JSON string containing OHLCV price data

    Returns:
        JSON string with momentum analysis
    """
    try:
        data = json.loads(price_data)
        df = pd.DataFrame(data)

        if df.empty or len(df) < 126:  # Need 6 months of data
            return json.dumps(
                {
                    "signal": "neutral",
                    "confidence": 0.0,
                    "error": "Insufficient data for momentum analysis",
                }
            )

        # Calculate returns
        returns = df["close"].pct_change()

        # Multi-period momentum
        mom_1m = returns.rolling(21).sum().iloc[-1]  # 1 month
        mom_3m = returns.rolling(63).sum().iloc[-1]  # 3 months
        mom_6m = returns.rolling(126).sum().iloc[-1]  # 6 months

        # Volume momentum
        volume_ma = df["volume"].rolling(21).mean()
        volume_momentum = (df["volume"] / volume_ma).iloc[-1]

        # Calculate weighted momentum score
        momentum_score = 0.4 * mom_1m + 0.3 * mom_3m + 0.3 * mom_6m

        # Volume confirmation
        volume_confirmation = volume_momentum > 1.0

        # Generate signal
        if momentum_score > 0.05 and volume_confirmation:
            signal = "bullish"
            confidence = min(abs(momentum_score) * 5, 1.0)
        elif momentum_score < -0.05 and volume_confirmation:
            signal = "bearish"
            confidence = min(abs(momentum_score) * 5, 1.0)
        else:
            signal = "neutral"
            confidence = 0.5

        analysis = {
            "signal": signal,
            "confidence": confidence,
            "momentum_1m": safe_float(mom_1m),
            "momentum_3m": safe_float(mom_3m),
            "momentum_6m": safe_float(mom_6m),
            "volume_momentum": safe_float(volume_momentum),
            "momentum_score": safe_float(momentum_score),
            "volume_confirmation": volume_confirmation,
        }

        return json.dumps(analysis)

    except Exception as e:
        return json.dumps(
            {
                "signal": "neutral",
                "confidence": 0.0,
                "error": f"Error calculating momentum indicators: {str(e)}",
            }
        )


def calculate_volatility_indicators(price_data: str) -> str:
    """
    Calculate volatility-based indicators and regime analysis.

    Args:
        price_data: JSON string containing OHLCV price data

    Returns:
        JSON string with volatility analysis
    """
    try:
        data = json.loads(price_data)
        df = pd.DataFrame(data)

        if df.empty or len(df) < 63:
            return json.dumps(
                {
                    "signal": "neutral",
                    "confidence": 0.0,
                    "error": "Insufficient data for volatility analysis",
                }
            )

        # Calculate returns
        returns = df["close"].pct_change()

        # Historical volatility (21-day, annualized)
        hist_vol = returns.rolling(21).std() * math.sqrt(252)

        # Volatility regime detection
        vol_ma = hist_vol.rolling(63).mean()
        vol_regime = hist_vol / vol_ma

        # Volatility mean reversion
        vol_std = hist_vol.rolling(63).std()
        vol_z_score = (hist_vol - vol_ma) / vol_std

        # Calculate ATR
        atr = calculate_atr_series(df)
        atr_ratio = atr / df["close"]

        # Generate signal based on volatility regime
        current_vol_regime = vol_regime.iloc[-1]
        vol_z = vol_z_score.iloc[-1]

        if current_vol_regime < 0.8 and vol_z < -1:
            signal = "bullish"  # Low volatility regime, potential expansion
            confidence = min(abs(vol_z) / 3, 1.0)
        elif current_vol_regime > 1.2 and vol_z > 1:
            signal = "bearish"  # High volatility regime, potential contraction
            confidence = min(abs(vol_z) / 3, 1.0)
        else:
            signal = "neutral"
            confidence = 0.5

        analysis = {
            "signal": signal,
            "confidence": confidence,
            "historical_volatility": safe_float(hist_vol.iloc[-1]),
            "volatility_regime": safe_float(current_vol_regime),
            "volatility_z_score": safe_float(vol_z),
            "atr_ratio": safe_float(atr_ratio.iloc[-1]),
            "vol_ma": safe_float(vol_ma.iloc[-1]),
        }

        return json.dumps(analysis)

    except Exception as e:
        return json.dumps(
            {
                "signal": "neutral",
                "confidence": 0.0,
                "error": f"Error calculating volatility indicators: {str(e)}",
            }
        )


def calculate_statistical_indicators(price_data: str) -> str:
    """
    Calculate statistical arbitrage indicators including Hurst exponent and distribution analysis.

    Args:
        price_data: JSON string containing OHLCV price data

    Returns:
        JSON string with statistical analysis
    """
    try:
        data = json.loads(price_data)
        df = pd.DataFrame(data)

        if df.empty or len(df) < 63:
            return json.dumps(
                {
                    "signal": "neutral",
                    "confidence": 0.0,
                    "error": "Insufficient data for statistical analysis",
                }
            )

        # Calculate returns
        returns = df["close"].pct_change().dropna()

        # Calculate Hurst exponent
        hurst = calculate_hurst_exponent(df["close"])

        # Calculate skewness and kurtosis
        skew = returns.rolling(63).skew().iloc[-1]
        kurt = returns.rolling(63).kurt().iloc[-1]

        # Generate signal based on statistical properties
        if hurst < 0.4 and skew > 1:
            signal = "bullish"  # Mean reverting with positive skew
            confidence = (0.5 - hurst) * 2
        elif hurst < 0.4 and skew < -1:
            signal = "bearish"  # Mean reverting with negative skew
            confidence = (0.5 - hurst) * 2
        else:
            signal = "neutral"
            confidence = 0.5

        analysis = {
            "signal": signal,
            "confidence": confidence,
            "hurst_exponent": safe_float(hurst),
            "skewness": safe_float(skew),
            "kurtosis": safe_float(kurt),
            "mean_reverting": hurst < 0.5,
            "trending": hurst > 0.5,
        }

        return json.dumps(analysis)

    except Exception as e:
        return json.dumps(
            {
                "signal": "neutral",
                "confidence": 0.0,
                "error": f"Error calculating statistical indicators: {str(e)}",
            }
        )


def combine_technical_signals(signals_data: str) -> str:
    """
    Combine multiple technical signals using weighted ensemble approach.

    Args:
        signals_data: JSON string containing all individual strategy signals

    Returns:
        JSON string with combined signal analysis
    """
    try:
        signals = json.loads(signals_data)

        # Strategy weights
        weights = {
            "trend": 0.25,
            "mean_reversion": 0.20,
            "momentum": 0.25,
            "volatility": 0.15,
            "statistical": 0.15,
        }

        # Convert signals to numeric values
        signal_values = {"bullish": 1, "neutral": 0, "bearish": -1}

        weighted_sum = 0
        total_confidence = 0

        for strategy in weights.keys():
            if strategy in signals:
                numeric_signal = signal_values.get(
                    signals[strategy].get("signal", "neutral"), 0
                )
                weight = weights[strategy]
                confidence = signals[strategy].get("confidence", 0.5)

                weighted_sum += numeric_signal * weight * confidence
                total_confidence += weight * confidence

        # Normalize the weighted sum
        if total_confidence > 0:
            final_score = weighted_sum / total_confidence
        else:
            final_score = 0

        # Convert back to signal
        if final_score > 0.2:
            signal = "bullish"
        elif final_score < -0.2:
            signal = "bearish"
        else:
            signal = "neutral"

        analysis = {
            "signal": signal,
            "confidence": abs(final_score),
            "final_score": final_score,
            "total_confidence": total_confidence,
            "strategy_weights": weights,
            "individual_signals": signals,
        }

        return json.dumps(analysis)

    except Exception as e:
        return json.dumps(
            {
                "signal": "neutral",
                "confidence": 0.0,
                "error": f"Error combining signals: {str(e)}",
            }
        )


# Helper functions for technical calculations


def calculate_rsi_series(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Calculate RSI indicator."""
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_adx_series(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """Calculate ADX indicator."""
    # Calculate True Range
    high_low = df["high"] - df["low"]
    high_close = abs(df["high"] - df["close"].shift())
    low_close = abs(df["low"] - df["close"].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)

    # Calculate Directional Movement
    up_move = df["high"] - df["high"].shift()
    down_move = df["low"].shift() - df["low"]

    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)

    # Calculate ADX
    plus_di = 100 * (
        pd.Series(plus_dm).ewm(span=period).mean() / tr.ewm(span=period).mean()
    )
    minus_di = 100 * (
        pd.Series(minus_dm).ewm(span=period).mean() / tr.ewm(span=period).mean()
    )
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    adx = dx.ewm(span=period).mean()

    return pd.DataFrame({"adx": adx, "plus_di": plus_di, "minus_di": minus_di})


def calculate_atr_series(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Calculate Average True Range."""
    high_low = df["high"] - df["low"]
    high_close = abs(df["high"] - df["close"].shift())
    low_close = abs(df["low"] - df["close"].shift())

    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)

    return true_range.rolling(period).mean()


def calculate_hurst_exponent(price_series: pd.Series, max_lag: int = 20) -> float:
    """Calculate Hurst Exponent for mean reversion detection."""
    try:
        lags = range(2, min(max_lag, len(price_series) // 4))
        tau = []

        for lag in lags:
            diff = np.subtract(price_series[lag:].values, price_series[:-lag].values)
            tau.append(max(1e-8, np.sqrt(np.var(diff))))

        # Return the Hurst exponent from linear fit
        if len(tau) > 1:
            reg = np.polyfit(np.log(lags), np.log(tau), 1)
            return max(0.1, min(0.9, reg[0]))  # Bound between 0.1 and 0.9
        else:
            return 0.5

    except (ValueError, RuntimeWarning, Exception):
        return 0.5  # Return random walk if calculation fails
