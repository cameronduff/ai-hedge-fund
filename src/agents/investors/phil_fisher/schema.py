from pydantic import BaseModel, model_validator
from typing_extensions import Literal
from typing import Any
from src.utils.schema_validators import strip_markdown_fences


class PhilFisherSignal(BaseModel):
    """Signal output from Phil Fisher long-term growth and management excellence analysis."""

    @model_validator(mode="before")
    @classmethod
    def validate_and_strip_markdown(cls, data: Any) -> Any:
        """Strip markdown code fences if the LLM wraps JSON in them."""
        return strip_markdown_fences(data)

    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float  # 0-100, representing confidence level
    reasoning: str  # Detailed analysis in Fisher's methodical, growth-focused style
