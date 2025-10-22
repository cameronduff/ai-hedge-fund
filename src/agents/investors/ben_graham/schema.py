"""
Ben Graham agent response schema.
"""

from pydantic import BaseModel, Field
from typing import Literal


class BenGrahamSignal(BaseModel):
    """
    Ben Graham-style value investing signal following his defensive investor principles.
    """

    signal: Literal["bullish", "bearish", "neutral"] = Field(
        description="Investment signal based on Ben Graham's conservative value criteria"
    )

    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence level in the signal (0-1)"
    )

    reasoning: str = Field(
        description="Detailed explanation of Graham analysis including earnings stability, financial strength, and valuation assessment"
    )
