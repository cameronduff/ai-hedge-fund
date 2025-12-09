from pydantic import BaseModel, Field, model_validator
from typing_extensions import Literal
from typing import Dict, Optional, Any

from src.utils.schema_validators import strip_markdown_fences


class TrendMetrics(BaseModel):
    adx: float
    trend_strength: float


class MeanReversionMetrics(BaseModel):
    z_score: float
    price_vs_bb: float
    rsi_14: float
    rsi_28: float


class MomentumMetrics(BaseModel):
    momentum_1m: float
    momentum_3m: float
    momentum_6m: float
    volume_momentum: float


class VolatilityMetrics(BaseModel):
    historical_volatility: float
    volatility_regime: float
    volatility_z_score: float
    atr_ratio: float


class StatArbMetrics(BaseModel):
    hurst_exponent: float
    skewness: float
    kurtosis: float


class StrategyAnalysis(BaseModel):
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: int = Field(description="Confidence level 0-100")


class TrendAnalysis(StrategyAnalysis):
    metrics: TrendMetrics


class MeanReversionAnalysis(StrategyAnalysis):
    metrics: MeanReversionMetrics


class MomentumAnalysis(StrategyAnalysis):
    metrics: MomentumMetrics


class VolatilityAnalysis(StrategyAnalysis):
    metrics: VolatilityMetrics


class StatArbAnalysis(StrategyAnalysis):
    metrics: StatArbMetrics


class TechnicalReasoning(BaseModel):
    trend_following: TrendAnalysis
    mean_reversion: MeanReversionAnalysis
    momentum: MomentumAnalysis
    volatility: VolatilityAnalysis
    statistical_arbitrage: StatArbAnalysis


class TechnicalAnalysis(BaseModel):
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: int = Field(description="Confidence level 0-100")
    reasoning: TechnicalReasoning


class TechnicalAgentOutput(BaseModel):
    """Output from Technical Agent's comprehensive technical analysis."""

    analysis: Dict[str, Optional[TechnicalAnalysis]] = Field(
        default_factory=dict,
        description="Technical analysis for each ticker (None if analysis could not be completed)",
    )

    @model_validator(mode="before")
    @classmethod
    def validate_and_strip_markdown(cls, data: Any) -> Any:
        """Strip markdown code fences if the LLM wraps JSON in them."""
        return strip_markdown_fences(data)
