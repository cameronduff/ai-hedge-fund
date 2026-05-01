from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Literal

class InvestmentStance(str, Enum):
    STRONG_BUY = "Strong Buy"
    BUY = "Buy"
    HOLD = "Hold"
    SELL = "Sell"
    STRONG_SELL = "Strong Sell"

class InvestorEvaluation(BaseModel):
    trading212_ticker: str = Field(
        ..., description="The exact trading212_ticker being evaluated (e.g., 'AAPL' or 'MSFT')"
    )
    investor_name: str = Field(
        ..., description="The name or persona of the investor (e.g., Warren Buffett, Cathie Wood)"
    )
    stance: InvestmentStance = Field(
        ..., description="The definitive investment stance on the ticker"
    )
    conviction_score: int = Field(
        ..., ge=1, le=10, description="Conviction level from 1 (lowest) to 10 (highest)"
    )
    core_thesis: str = Field(
        ..., description="A 2-3 sentence summary of the investment rationale based on this persona's philosophy."
    )
    key_metrics_cited: List[str] = Field(
        ..., description="Specific JSON paths from the TickerDossier driving this decision (e.g., 'valuations.multiples.peg_ratio')"
    )
    primary_concern: str = Field(
        ..., description="The biggest risk factor or counter-argument this investor acknowledges based on the dossier."
    )

class InvestorResponse(BaseModel):
    evaluations: List[InvestorEvaluation] = Field(
        ..., 
        description="A comprehensive list of evaluations. You MUST provide exactly one evaluation for EVERY ticker present in the input dossier."
    )

class InvestorPosition(BaseModel):
    investor_name: str = Field(..., description="Name of the investor")
    rating: Literal["BUY", "HOLD", "SELL"] = Field(..., description="Investor's rating")
    conviction: Literal["HIGH", "MEDIUM", "LOW"] = Field(..., description="Conviction level")
    key_thesis: str = Field(..., description="One sentence summary of their thesis")

class InvestmentDecision(BaseModel):
    trading212_ticker: str
    yfinance_ticker: str
    final_rating: Literal["BUY", "HOLD", "SELL"]
    consensus_strength: Literal["UNANIMOUS", "STRONG", "SPLIT"] = Field(
        ..., description="How unified the board was on this decision"
    )
    position_size_pct: float = Field(
        ..., description="Recommended portfolio allocation as a percentage"
    )
    target_price: float = Field(
        ..., description="CIO's target price based on board debate"
    )
    time_horizon_months: int = Field(
        ..., description="Recommended holding period in months"
    )
    key_catalysts: list[str] = Field(
        ..., description="Key catalysts that would validate the thesis"
    )
    key_risks: list[str] = Field(
        ..., description="Primary risks that could invalidate the thesis"
    )
    investor_positions: list[InvestorPosition] = Field(
        ..., description="Each investor's final position after debate"
    )
    dissenting_views: str = Field(
        ..., description="Summary of any minority dissenting views and why they were overruled"
    )
    debate_summary: str = Field(
        ..., description="Brief summary of the key points of debate that shaped the final decision"
    )

class CIOOutput(BaseModel):
    decisions: list[InvestmentDecision]
    portfolio_notes: str = Field(
        ..., description="High level notes for the portfolio manager on overall market positioning and correlations between positions"
    )