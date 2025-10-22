from __future__ import annotations
from typing_extensions import Literal
from pydantic import BaseModel


class AswathDamodaranSignal(BaseModel):
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float  # 0-100
    reasoning: str
