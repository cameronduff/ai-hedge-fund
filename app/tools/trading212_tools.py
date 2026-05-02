from app.clients.trading212_client import Trading212Client
from app.models.trading212_models import (
    LimitOrderPayload,
    MarketOrderPayload,
    StopLimitOrderPayload,
)

trading212_client = Trading212Client()


# Read only tools


def get_account_summary() -> dict:
    """
    Retrieves the current account summary from Trading 212.
    Use this tool to check available free cash, blocked funds, total portfolio value,
    and overall account health before making trade decisions.
    """
    return trading212_client.get_account_summary()


def get_all_pending_orders() -> dict:
    """
    Fetches a list of all currently active pending orders that have not yet been executed.
    Use this to verify if there are already open limit or stop orders in the queue.
    """
    return trading212_client.get_all_pending_orders()


def get_pending_order_by_id(id: int) -> dict:
    """
    Retrieves the exact details of a specific pending order.

    Args:
        id (int): The unique integer identifier of the pending order.
    """
    return trading212_client.get_pending_order_by_id(id)


def get_all_available_instruments() -> dict:
    """
    Fetches the complete directory of all tradable instruments (stocks, ETFs) on Trading 212.
    Use this to verify if a ticker exists on the platform or to check asset metadata (like currency).
    """
    return trading212_client.get_all_available_instruments()


def fetch_all_open_positions(query: dict | None = None) -> dict:
    """
    Fetches all currently open positions in the portfolio.
    Use this to see existing holdings, average buy prices, current values, 
    and unrealised P&L.

    Args:
        query (dict, optional): Optional filter parameters. Pass None to 
        retrieve all open positions.
    """
    return trading212_client.fetch_all_open_positions(query)


# Execution tools


def place_limit_order(payload: LimitOrderPayload) -> dict:
    """
    Places a limit order on Trading 212.
    Use this to buy or sell a specific quantity of an asset at a strictly specified price or better.

    Args:
        payload (LimitOrderPayload): Contains the ticker, quantity, and extended hours preference.
    """
    return trading212_client.place_limit_order(payload)


def place_market_order(payload: MarketOrderPayload) -> dict:
    """
    Places a market order on Trading 212.
    Use this to buy or sell a specific quantity of an asset immediately at the best available current price.

    Args:
        payload (MarketOrderPayload): Contains the ticker, quantity, limit price constraints, and time validity.
    """
    return trading212_client.place_market_order(payload)


def place_stop_order(payload: MarketOrderPayload) -> dict:
    """
    Places a stop order on Trading 212.
    Use this to trigger a market order execution only once a specific price threshold is crossed.

    Args:
        payload (MarketOrderPayload): Contains the ticker, quantity, and limit/trigger price logic.
    """
    return trading212_client.place_stop_order(payload)


def place_stop_limit_order(payload: StopLimitOrderPayload) -> dict:
    """
    Places a stop-limit order on Trading 212.
    Use this to combine a stop trigger with a specific limit execution price to tightly control entry/exit.

    Args:
        payload (StopLimitOrderPayload): Contains the ticker, quantity, stop trigger price, and limit execution price.
    """
    return trading212_client.place_stop_limit_order(payload)


def cancel_pending_order(id: int) -> dict:
    """
    Cancels an existing pending order on Trading 212.

    Args:
        id (int): The unique integer identifier of the pending order to be canceled.
    """
    return trading212_client.cancel_pending_order(id)
