from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class GrowthMomentumAnalysis(BaseModel):
    """Growth and momentum analysis metrics"""

    score: float = Field(description="Growth and momentum score (0-10)")
    revenue_growth: Optional[float] = Field(
        description="Annualized revenue growth rate"
    )
    eps_growth: Optional[float] = Field(description="Annualized EPS growth rate")
    price_momentum: Optional[float] = Field(description="Price momentum percentage")
    details: str = Field(description="Detailed analysis explanation")


class RiskRewardAnalysis(BaseModel):
    """Risk-reward analysis metrics"""

    score: float = Field(description="Risk-reward score (0-10)")
    debt_to_equity: Optional[float] = Field(description="Debt-to-equity ratio")
    volatility: Optional[float] = Field(description="Price volatility measure")
    upside_potential: Optional[float] = Field(description="Estimated upside potential")
    downside_risk: Optional[float] = Field(description="Estimated downside risk")
    details: str = Field(description="Detailed risk-reward explanation")


class ValuationAnalysis(BaseModel):
    """Valuation analysis metrics"""

    score: float = Field(description="Valuation score (0-10)")
    pe_ratio: Optional[float] = Field(description="Price-to-earnings ratio")
    pfcf_ratio: Optional[float] = Field(description="Price-to-free-cash-flow ratio")
    ev_ebit: Optional[float] = Field(description="EV-to-EBIT ratio")
    ev_ebitda: Optional[float] = Field(description="EV-to-EBITDA ratio")
    details: str = Field(description="Detailed valuation explanation")


class SentimentAnalysis(BaseModel):
    """Market sentiment analysis"""

    score: float = Field(description="Sentiment score (0-10)")
    positive_signals: int = Field(description="Number of positive sentiment indicators")
    negative_signals: int = Field(description="Number of negative sentiment indicators")
    overall_sentiment: str = Field(
        description="Overall sentiment: positive, negative, or neutral"
    )
    details: str = Field(description="Detailed sentiment explanation")


class InsiderActivityAnalysis(BaseModel):
    """Insider trading activity analysis"""

    score: float = Field(description="Insider activity score (0-10)")
    buy_transactions: int = Field(description="Number of insider buy transactions")
    sell_transactions: int = Field(description="Number of insider sell transactions")
    net_activity: str = Field(
        description="Net insider activity: buying, selling, or neutral"
    )
    details: str = Field(description="Detailed insider activity explanation")


class StanleyDruckenmillerAnalysis(BaseModel):
    """Individual Stanley Druckenmiller analysis for a ticker"""

    signal: str = Field(description="Investment signal: bullish, bearish, or neutral")
    confidence: float = Field(description="Confidence score (0-100)")
    total_score: float = Field(description="Total weighted analysis score")
    growth_momentum: GrowthMomentumAnalysis = Field(
        description="Growth and momentum analysis"
    )
    risk_reward: RiskRewardAnalysis = Field(description="Risk-reward analysis")
    valuation: ValuationAnalysis = Field(description="Valuation analysis")
    sentiment: SentimentAnalysis = Field(description="Sentiment analysis")
    insider_activity: InsiderActivityAnalysis = Field(
        description="Insider activity analysis"
    )
    reasoning: str = Field(description="Comprehensive investment thesis and reasoning")


class StanleyDruckenmillerOutput(BaseModel):
    """Output schema for Stanley Druckenmiller investment analysis"""

    analysis: Dict[str, StanleyDruckenmillerAnalysis] = Field(
        description="Stanley Druckenmiller analysis results for each ticker"
    )
    summary: str = Field(description="Overall portfolio-level summary and key insights")
    market_outlook: str = Field(
        description="Stanley Druckenmiller's market outlook and positioning strategy"
    )
    top_conviction_picks: list[str] = Field(
        description="List of highest conviction investment picks"
    )
    key_themes: list[str] = Field(
        description="Major investment themes and catalysts identified"
    )
