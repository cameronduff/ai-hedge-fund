# app/tools/calculation_tools.py

from loguru import logger
import math


def calculate_position_size(
    portfolio_value_gbp: float,
    target_position_pct: float,
    limit_price_gbp: float,
) -> dict:
    """
    Calculates the quantity of shares to buy based on a target percentage of the portfolio.

    Args:
        portfolio_value_gbp: Total value of the portfolio in GBP.
        target_position_pct: The desired percentage of the portfolio for this position (0-100).
        limit_price_gbp: The price per share in GBP.

    Returns:
        A dict with:
            - quantity: Number of shares (rounded down to 2 decimal places).
            - position_value_gbp: Total value of the position in GBP.
            - actual_position_pct: The actual percentage of the portfolio this position represents.
    """
    logger.info(f"Calling calculate_position_size(portfolio_value_gbp={portfolio_value_gbp}, target_position_pct={target_position_pct}, limit_price_gbp={limit_price_gbp})")
    position_value = (portfolio_value_gbp * target_position_pct / 100)
    quantity = position_value / limit_price_gbp
    quantity_rounded = math.floor(quantity * 100) / 100  # floor to 2 decimal places
    actual_pct = (quantity_rounded * limit_price_gbp / portfolio_value_gbp) * 100

    return {
        "quantity": quantity_rounded,
        "position_value_gbp": round(quantity_rounded * limit_price_gbp, 2),
        "actual_position_pct": round(actual_pct, 2),
    }


def calculate_remaining_cash(
    cash_available_gbp: float,
    trade_value_gbp: float,
) -> dict:
    """
    Calculates remaining cash after a trade and whether minimum cash reserve is maintained.

    Args:
        cash_available_gbp: Current free cash available in GBP.
        trade_value_gbp: Total value of the proposed trade in GBP.

    Returns:
        A dict with:
            - remaining_cash_gbp: Cash remaining after the trade.
            - cash_consumed_gbp: Total cost of the trade.
            - reserve_maintained: Boolean indicating if remaining cash is non-negative.
    """
    logger.info(f"Calling calculate_remaining_cash(cash_available_gbp={cash_available_gbp}, trade_value_gbp={trade_value_gbp})")
    remaining = cash_available_gbp - trade_value_gbp
    return {
        "remaining_cash_gbp": round(remaining, 2),
        "cash_consumed_gbp": round(trade_value_gbp, 2),
        "reserve_maintained": remaining >= 0,
    }


def calculate_position_value(
    quantity: float,
    price_gbp: float,
) -> dict:
    """
    Calculates the total value of a position.

    Args:
        quantity: Number of shares.
        price_gbp: Price per share in GBP.

    Returns:
        A dict with:
            - total_value_gbp: Total value of the position.
    """
    logger.info(f"Calling calculate_position_value(quantity={quantity}, price_gbp={price_gbp})")
    return {
        "total_value_gbp": round(quantity * price_gbp, 2),
    }


def calculate_portfolio_concentration(
    position_value_gbp: float,
    portfolio_value_gbp: float,
) -> dict:
    """
    Calculates what percentage of the portfolio a position represents.

    Args:
        position_value_gbp: Value of the position in GBP.
        portfolio_value_gbp: Total portfolio value in GBP.

    Returns:
        A dict with:
            - position_pct: Percentage of the portfolio.
            - breaches_15pct_limit: Boolean indicating if the position exceeds 15% of the portfolio.
    """
    logger.info(f"Calling calculate_portfolio_concentration(position_value_gbp={position_value_gbp}, portfolio_value_gbp={portfolio_value_gbp})")
    pct = (position_value_gbp / portfolio_value_gbp) * 100
    return {
        "position_pct": round(pct, 2),
        "breaches_15pct_limit": pct > 15.0,
    }


def calculate_annualised_volatility(daily_returns: list[float]) -> dict:
    """
    Calculates annualised volatility from a list of daily returns.

    Args:
        daily_returns: List of daily return values (e.g. [0.01, -0.02, 0.005, ...]).

    Returns:
        A dict with:
            - annualised_volatility_pct: Annualised volatility as a percentage.
            - volatility_classification: LOW, MEDIUM, HIGH, or EXTREME.
            - size_reduction_pct: Suggested position size reduction percentage based on volatility.
    """
    logger.info(f"Calling calculate_annualised_volatility(num_returns={len(daily_returns)})")
    import math

    n = len(daily_returns)
    if n < 2:
        return {
            "annualised_volatility_pct": 0.0,
            "volatility_classification": "UNKNOWN",
            "size_reduction_pct": 0,
        }

    mean = sum(daily_returns) / n
    variance = sum((r - mean) ** 2 for r in daily_returns) / (n - 1)
    daily_std = math.sqrt(variance)
    annualised_vol = daily_std * math.sqrt(252) * 100

    if annualised_vol < 20:
        classification = "LOW"
        reduction = 0
    elif annualised_vol < 40:
        classification = "MEDIUM"
        reduction = 25
    elif annualised_vol < 60:
        classification = "HIGH"
        reduction = 50
    else:
        classification = "EXTREME"
        reduction = 75

    return {
        "annualised_volatility_pct": round(annualised_vol, 2),
        "volatility_classification": classification,
        "size_reduction_pct": reduction,
    }


def calculate_unrealised_pnl(
    average_cost_gbp: float,
    current_price_gbp: float,
    quantity: float,
) -> dict:
    """
    Calculates unrealised P&L for an open position.

    Args:
        average_cost_gbp: Average cost per share in GBP.
        current_price_gbp: Current market price per share in GBP.
        quantity: Number of shares held.

    Returns:
        A dict with:
            - unrealised_pnl_gbp: Unrealised profit or loss in GBP.
            - pnl_pct: Profit or loss as a percentage of cost.
            - stop_loss_flag: Boolean indicating if P&L is below -15%.
            - take_profit_flag: Boolean indicating if P&L is above 50%.
    """
    logger.info(f"Calling calculate_unrealised_pnl(average_cost_gbp={average_cost_gbp}, current_price_gbp={current_price_gbp}, quantity={quantity})")
    pnl_per_share = current_price_gbp - average_cost_gbp
    total_pnl = pnl_per_share * quantity
    pnl_pct = (pnl_per_share / average_cost_gbp) * 100

    return {
        "unrealised_pnl_gbp": round(total_pnl, 2),
        "pnl_pct": round(pnl_pct, 2),
        "stop_loss_flag": pnl_pct < -15.0,
        "take_profit_flag": pnl_pct > 50.0,
    }
