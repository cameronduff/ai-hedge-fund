from pydantic import BaseModel, model_validator
from typing_extensions import Literal
from typing import Any

from src.utils.schema_validators import strip_markdown_fences


class WarrenBuffettSignal(BaseModel):
    """Signal output from Warren Buffett's value investing and business quality analysis."""

    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float  # 0-100, representing confidence level
    reasoning: str  # Detailed analysis in Buffett's disciplined, long-term value style

    @model_validator(mode="before")
    @classmethod
    def validate_and_strip_markdown(cls, data: Any) -> Any:
        """Strip markdown code fences if the LLM wraps JSON in them."""
        return strip_markdown_fences(data)
