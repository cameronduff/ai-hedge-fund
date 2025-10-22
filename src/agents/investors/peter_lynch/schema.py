from pydantic import BaseModel
from typing_extensions import Literal


class PeterLynchSignal(BaseModel):
    """Signal output from Peter Lynch Growth at Reasonable Price (GARP) analysis."""

    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float  # 0-100, representing confidence level
    reasoning: str  # Detailed analysis in Lynch's practical, folksy style
