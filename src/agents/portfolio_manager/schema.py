from pydantic import BaseModel, Field, model_validator
from typing_extensions import Literal
from typing import Any

from src.utils.schema_validators import strip_markdown_fences


class PortfolioDecision(BaseModel):
    action: Literal["buy", "sell", "short", "cover", "hold"]
    quantity: int = Field(description="Number of shares to trade")
    confidence: int = Field(description="Confidence 0-100")
    reasoning: str = Field(description="Reasoning for the decision")


class PortfolioManagerOutput(BaseModel):
    """Output from Portfolio Manager's trading decision analysis."""

    decisions: dict[str, PortfolioDecision] = Field(
        default_factory=dict, description="Dictionary of ticker to trading decisions"
    )

    @model_validator(mode="before")
    @classmethod
    def validate_and_strip_markdown(cls, data: Any) -> Any:
        """Strip markdown code fences if the LLM wraps JSON in them."""
        return strip_markdown_fences(data)
