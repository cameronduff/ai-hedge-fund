from pydantic import BaseModel, Field
from typing import Literal

class TradeInstruction(BaseModel):
    trading212_ticker: str
    action: Literal["BUY", "SELL", "HOLD", "REDUCE", "ADD"]
    order_type: Literal["MARKET", "LIMIT", "STOP_LIMIT"]
    quantity: float  # remove gt=0
    limit_price: float | None = None
    stop_price: float | None = None
    time_validity: Literal["DAY", "GOOD_TILL_CANCEL"] = "DAY"
    extended_hours: bool = False
    target_position_size_pct: float
    rationale: str
    risk_approved: bool
    risk_notes: str | None = None

class PortfolioManagerOutput(BaseModel):
    account_value: float
    cash_available: float
    current_positions_summary: str = Field(
        ..., description="Brief summary of current open positions before any trades"
    )
    instructions: list[TradeInstruction]
    deferred_instructions: list[str] = Field(
        default_factory=list,
        description="Instructions deferred pending risk approval or market conditions"
    )
    portfolio_summary: str = Field(
        ..., description="Summary of proposed portfolio changes and expected outcome"
    )
    next_review_trigger: str = Field(
        ..., description="Event or condition that should trigger the next review"
    )