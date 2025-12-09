"""
Cathie Wood agent response schema.
"""

from pydantic import BaseModel, Field, model_validator
from typing import Literal, Any
from src.utils.schema_validators import strip_markdown_fences


class CathieWoodSignal(BaseModel):
    """
    Cathie Wood-style disruptive innovation investment signal focusing on exponential growth potential.
    """

    @model_validator(mode="before")
    @classmethod
    def validate_and_strip_markdown(cls, data: Any) -> Any:
        """Strip markdown code fences if the LLM wraps JSON in them."""
        return strip_markdown_fences(data)

    signal: Literal["bullish", "bearish", "neutral"] = Field(
        description="Investment signal based on Wood's disruptive innovation and exponential growth criteria"
    )

    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence level in the signal (0-1)"
    )

    reasoning: str = Field(
        description="Detailed explanation of Wood's analysis including disruptive potential, innovation growth, and high-growth valuation assessment"
    )
