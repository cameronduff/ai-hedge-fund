from pydantic import BaseModel
from typing_extensions import Literal


class PhilFisherSignal(BaseModel):
    """Signal output from Phil Fisher long-term growth and management excellence analysis."""

    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float  # 0-100, representing confidence level
    reasoning: str  # Detailed analysis in Fisher's methodical, growth-focused style
