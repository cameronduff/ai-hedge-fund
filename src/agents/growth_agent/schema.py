from pydantic import BaseModel, Field
from typing_extensions import Literal
from typing import Dict, Optional


class GrowthTrendAnalysis(BaseModel):
    score: float
    revenue_growth: Optional[float] = None
    revenue_trend: float
    eps_growth: Optional[float] = None
    eps_trend: float
    fcf_growth: Optional[float] = None
    fcf_trend: float


class ValuationAnalysis(BaseModel):
    score: float
    peg_ratio: Optional[float] = None
    price_to_sales_ratio: Optional[float] = None


class MarginAnalysis(BaseModel):
    score: float
    gross_margin: Optional[float] = None
    gross_margin_trend: float
    operating_margin: Optional[float] = None
    operating_margin_trend: float
    net_margin: Optional[float] = None
    net_margin_trend: float


class InsiderConvictionAnalysis(BaseModel):
    score: float
    net_flow_ratio: float
    buys: float
    sells: float


class FinancialHealthAnalysis(BaseModel):
    score: float
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None


class FinalAnalysis(BaseModel):
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float
    weighted_score: float


class GrowthReasoning(BaseModel):
    historical_growth: GrowthTrendAnalysis
    growth_valuation: ValuationAnalysis
    margin_expansion: MarginAnalysis
    insider_conviction: InsiderConvictionAnalysis
    financial_health: FinancialHealthAnalysis
    final_analysis: FinalAnalysis


class GrowthAnalysis(BaseModel):
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float
    reasoning: GrowthReasoning


class GrowthAgentOutput(BaseModel):
    """Output from Growth Agent's comprehensive growth analysis."""

    analysis: Dict[str, Optional[GrowthAnalysis]] = Field(
        description="Growth analysis for each ticker (None if analysis could not be completed)"
    )
