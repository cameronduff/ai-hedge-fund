from pydantic import BaseModel, Field
from typing_extensions import Literal


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
