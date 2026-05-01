from pydantic import BaseModel, Field
from enum import Enum
from typing import List

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