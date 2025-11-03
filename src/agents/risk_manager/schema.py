from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class CorrelationEntry(BaseModel):
    ticker: str
    correlation: float


class CorrelationMetrics(BaseModel):
    avg_correlation_with_active: Optional[float] = None
    max_correlation_with_active: Optional[float] = None
    top_correlated_tickers: List[CorrelationEntry] = []


class VolatilityMetrics(BaseModel):
    daily_volatility: float
    annualized_volatility: float
    volatility_percentile: float
    data_points: int


class RiskReasoning(BaseModel):
    portfolio_value: float
    current_position_value: float
    base_position_limit_pct: float
    correlation_multiplier: float
    combined_position_limit_pct: float
    position_limit: float
    remaining_limit: float
    available_cash: float
    risk_adjustment: str
    error: Optional[str] = None


class RiskAnalysis(BaseModel):
    remaining_position_limit: float
    current_price: float
    volatility_metrics: Optional[VolatilityMetrics] = None
    correlation_metrics: Optional[CorrelationMetrics] = None
    reasoning: RiskReasoning


class RiskManagerOutput(BaseModel):
    """Output from Risk Manager's volatility and correlation analysis."""

    risk_analysis: Dict[str, Optional[RiskAnalysis]] = Field(
        default_factory=dict,
        description="Risk analysis for each ticker (None if analysis could not be completed)",
    )
