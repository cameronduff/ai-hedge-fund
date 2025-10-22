"""
Bill Ackman agent response schema.
"""

from pydantic import BaseModel, Field
from typing import Literal


class BillAckmanSignal(BaseModel):
    """
    Bill Ackman-style concentrated value investing signal with activism potential.
    """

    signal: Literal["bullish", "bearish", "neutral"] = Field(
        description="Investment signal based on Ackman's high-quality business and activism criteria"
    )

    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence level in the signal (0-1)"
    )

    reasoning: str = Field(
        description="Detailed explanation of Ackman analysis including business quality, financial discipline, activism potential, and valuation assessment"
    )
