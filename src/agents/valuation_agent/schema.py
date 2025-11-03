from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class DCFScenarioAnalysis(BaseModel):
    """DCF scenario analysis results"""

    bear_case: float = Field(description="Bear case valuation")
    base_case: float = Field(description="Base case valuation")
    bull_case: float = Field(description="Bull case valuation")
    expected_value: float = Field(description="Probability-weighted expected value")
    wacc_used: float = Field(description="Weighted average cost of capital used")
    terminal_growth: float = Field(description="Terminal growth rate assumption")
    value_range: float = Field(description="Range between bull and bear cases")


class ValuationMethodAnalysis(BaseModel):
    """Individual valuation method analysis"""

    value: float = Field(description="Calculated intrinsic value")
    market_cap: float = Field(description="Current market capitalization")
    value_gap: float = Field(
        description="Percentage gap between intrinsic value and market cap"
    )
    weight: float = Field(
        description="Weight assigned to this method in final calculation"
    )
    signal: str = Field(
        description="Signal from this method: bullish, bearish, or neutral"
    )
    confidence: float = Field(description="Confidence in this valuation method (0-100)")
    details: str = Field(
        description="Detailed explanation of the valuation calculation"
    )


class EnhancedDCFAnalysis(ValuationMethodAnalysis):
    """Enhanced DCF analysis with scenarios"""

    dcf_scenarios: DCFScenarioAnalysis = Field(
        description="Multi-scenario DCF analysis"
    )
    fcf_quality_score: float = Field(
        description="Free cash flow quality assessment (0-100)"
    )
    growth_sustainability: float = Field(
        description="Growth sustainability score (0-100)"
    )


class OwnerEarningsAnalysis(ValuationMethodAnalysis):
    """Buffett-style owner earnings analysis"""

    owner_earnings: float = Field(description="Calculated owner earnings")
    margin_of_safety: float = Field(description="Margin of safety applied")
    required_return: float = Field(description="Required return assumption")
    growth_assumptions: str = Field(description="Growth rate assumptions used")


class EVEBITDAAnalysis(ValuationMethodAnalysis):
    """EV/EBITDA multiple-based analysis"""

    current_multiple: float = Field(description="Current EV/EBITDA multiple")
    peer_median_multiple: float = Field(
        description="Peer group median EV/EBITDA multiple"
    )
    multiple_premium_discount: float = Field(description="Premium/discount to peers")
    ebitda_quality: str = Field(description="EBITDA quality assessment")


class ResidualIncomeAnalysis(ValuationMethodAnalysis):
    """Residual income model analysis"""

    current_roe: float = Field(description="Current return on equity")
    cost_of_equity: float = Field(description="Cost of equity assumption")
    book_value_growth: float = Field(description="Book value growth assumption")
    excess_return_sustainability: str = Field(
        description="Assessment of excess return sustainability"
    )


class ValuationAnalysis(BaseModel):
    """Comprehensive valuation analysis for a ticker"""

    signal: str = Field(
        description="Overall valuation signal: bullish, bearish, or neutral"
    )
    confidence: float = Field(description="Overall confidence score (0-100)")
    weighted_value_gap: float = Field(
        description="Weighted average value gap across all methods"
    )
    intrinsic_value_estimate: float = Field(
        description="Best estimate of intrinsic value"
    )

    # Individual method analyses
    dcf_analysis: Optional[EnhancedDCFAnalysis] = Field(
        description="Enhanced DCF analysis"
    )
    owner_earnings_analysis: Optional[OwnerEarningsAnalysis] = Field(
        description="Owner earnings analysis"
    )
    ev_ebitda_analysis: Optional[EVEBITDAAnalysis] = Field(
        description="EV/EBITDA analysis"
    )
    residual_income_analysis: Optional[ResidualIncomeAnalysis] = Field(
        description="Residual income analysis"
    )

    # Summary insights
    key_value_drivers: list[str] = Field(
        description="Primary factors driving valuation"
    )
    risk_factors: list[str] = Field(description="Key risks to valuation thesis")
    catalysts: list[str] = Field(
        description="Potential catalysts for value realization"
    )
    reasoning: str = Field(
        description="Comprehensive valuation reasoning and conclusion"
    )


class ValuationAgentOutput(BaseModel):
    """Output schema for valuation analysis agent"""

    valuation_analysis: Dict[str, Optional[ValuationAnalysis]] = Field(
        description="Comprehensive valuation analysis results for each ticker (None if analysis could not be completed)"
    )
    summary: str = Field(description="Portfolio-level valuation summary and insights")
    methodology_notes: str = Field(
        description="Notes on valuation methodologies and assumptions used"
    )
    market_context: str = Field(
        description="Current market valuation context and environment"
    )
    top_value_opportunities: list[str] = Field(
        description="Tickers with highest upside potential"
    )
    valuation_concerns: list[str] = Field(
        description="Tickers with significant overvaluation risks"
    )
