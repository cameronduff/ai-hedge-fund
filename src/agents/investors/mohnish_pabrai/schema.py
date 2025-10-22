from pydantic import BaseModel
from typing_extensions import Literal


class MohnishPabraiSignal(BaseModel):
    """Signal output from Mohnish Pabrai 'heads I win, tails I don't lose much' analysis."""

    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float  # 0-100, representing confidence level
    reasoning: str  # Detailed checklist-driven analysis in Pabrai's style
