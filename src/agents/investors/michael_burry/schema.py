from pydantic import BaseModel, model_validator
from typing_extensions import Literal
from typing import Any
from src.utils.schema_validators import strip_markdown_fences


class MichaelBurrySignal(BaseModel):
    """Signal output from Michael Burry deep value analysis."""

    @model_validator(mode="before")
    @classmethod
    def validate_and_strip_markdown(cls, data: Any) -> Any:
        """Strip markdown code fences if the LLM wraps JSON in them."""
        return strip_markdown_fences(data)

    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float  # 0-100, representing confidence level
    reasoning: str  # Detailed analysis in Burry's data-driven style
