"""
Charlie Munger agent response schema.
"""

from pydantic import BaseModel, Field
from typing import Literal


class CharlieMungerSignal(BaseModel):
    """
    Charlie Munger-style rational investment signal focusing on business quality and mental models.
    """

    signal: Literal["bullish", "bearish", "neutral"] = Field(
        description="Investment signal based on Munger's quality-focused criteria and mental models"
    )

    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence level in the signal (0-1)"
    )

    reasoning: str = Field(
        description="Detailed explanation of Munger analysis including moat strength, management quality, predictability, and rational valuation assessment"
    )
