from pydantic import BaseModel, Field, model_validator
from typing_extensions import Literal
from typing import Dict, Optional, Any

from src.utils.schema_validators import strip_markdown_fences


class FundamentalSignalDetail(BaseModel):
    signal: Literal["bullish", "bearish", "neutral"]
    details: str


class FundamentalReasoning(BaseModel):
    profitability_signal: FundamentalSignalDetail
    growth_signal: FundamentalSignalDetail
    financial_health_signal: FundamentalSignalDetail
    price_ratios_signal: FundamentalSignalDetail


class FundamentalAnalysis(BaseModel):
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float = Field(description="Confidence level 0-100")
    reasoning: FundamentalReasoning


class FundamentalsAgentOutput(BaseModel):
    """Output from Fundamentals Agent's financial analysis."""

    analysis: Dict[str, Optional[FundamentalAnalysis]] = Field(
        default_factory=dict,
        description="Fundamental analysis for each ticker (None if analysis could not be completed)",
    )

    @model_validator(mode="before")
    @classmethod
    def validate_and_strip_markdown(cls, data: Any) -> Any:
        """Strip markdown code fences if the LLM wraps JSON in them."""
        return strip_markdown_fences(data)
