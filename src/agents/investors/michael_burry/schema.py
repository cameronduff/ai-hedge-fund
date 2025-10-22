from pydantic import BaseModel
from typing_extensions import Literal


class MichaelBurrySignal(BaseModel):
    """Signal output from Michael Burry deep value analysis."""

    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float  # 0-100, representing confidence level
    reasoning: str  # Detailed analysis in Burry's data-driven style
