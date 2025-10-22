"""
Cathie Wood agent response schema.
"""

from pydantic import BaseModel, Field
from typing import Literal


class CathieWoodSignal(BaseModel):
    """
    Cathie Wood-style disruptive innovation investment signal focusing on exponential growth potential.
    """

    signal: Literal["bullish", "bearish", "neutral"] = Field(
        description="Investment signal based on Wood's disruptive innovation and exponential growth criteria"
    )

    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence level in the signal (0-1)"
    )

    reasoning: str = Field(
        description="Detailed explanation of Wood's analysis including disruptive potential, innovation growth, and high-growth valuation assessment"
    )
