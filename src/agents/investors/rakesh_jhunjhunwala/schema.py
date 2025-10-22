from pydantic import BaseModel
from typing_extensions import Literal


class RakeshJhunjhunwalaSignal(BaseModel):
    """Signal output from Rakesh Jhunjhunwala quality-focused value with growth analysis."""

    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float  # 0-100, representing confidence level
    reasoning: str  # Detailed analysis in Jhunjhunwala's quality-focused, value-with-growth style
