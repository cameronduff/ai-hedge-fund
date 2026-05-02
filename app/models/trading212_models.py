from pydantic import BaseModel, Field
from typing import Literal
import json


class LimitOrderPayload(BaseModel):
    limitPrice: float = Field(..., gt=0)
    extendedHours: bool = Field(False)
    quantity: float = Field(..., gt=0)
    ticker: str = Field(...)


class MarketOrderPayload(BaseModel):
    limitPrice: float = Field(..., gt=0)
    quantity: float = Field(...)
    ticker: str = Field(...)
    timeValidity: Literal["DAY", "GOOD_TILL_CANCEL"]


class StopLimitOrderPayload(BaseModel):
    limitPrice: float = Field(..., gt=0)
    quantity: float = Field(...)
    stopPrice: float = Field(..., gt=0)
    ticker: str = Field(...)
    timeValidity: Literal["DAY", "GOOD_TILL_CANCEL"]


if __name__ == "__main__":
    payload = LimitOrderPayload(
        limitPrice=100.0, quantity=0.5, ticker="APPL", timeValidity="DAY"
    )

    print(payload.model_dump_json())
