from pydantic import BaseModel
from typing_extensions import Literal


class WarrenBuffettSignal(BaseModel):
    """Signal output from Warren Buffett's value investing and business quality analysis."""

    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float  # 0-100, representing confidence level
    reasoning: str  # Detailed analysis in Buffett's disciplined, long-term value style
