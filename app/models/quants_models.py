from typing import List, Optional
from pydantic import BaseModel, Field

# --- Base Ticker Model ---


class Ticker(BaseModel):
    name: str = Field(...)
    trading212_ticker: str = Field(...)
    yfinance_ticker: str = Field(...)


# --- Sub-Metric Models ---


class FundamentalsMetrics(BaseModel):
    total_debt: float = Field(..., description="Total debt of the company")
    cash_and_equivalents: float = Field(..., description="Total cash and liquid assets")
    debt_to_equity: float = Field(..., description="Debt-to-equity ratio")
    net_income_ttm: float = Field(
        ..., description="Net income for the trailing twelve months"
    )
    return_on_equity_pct: float = Field(
        ..., description="Return on equity expressed as a percentage"
    )
    operating_margin_pct: float = Field(
        ..., description="Operating margin expressed as a percentage"
    )
    current_ratio: float = Field(..., description="Current ratio (assets/liabilities)")


class TechnicalMetrics(BaseModel):
    current_price: float = Field(..., description="Current market price")
    rsi_14: float = Field(..., description="14-day Relative Strength Index")
    macd: str = Field(..., description="Current MACD signal (e.g., Bullish Crossover)")
    sma_50: float = Field(..., description="50-day Simple Moving Average")
    sma_200: float = Field(..., description="200-day Simple Moving Average")
    fifty_two_week_high: float = Field(..., description="52-week high price")
    volume_24h_change_pct: float = Field(
        ..., description="Percentage change in volume over the last 24 hours"
    )


class GrowthMetrics(BaseModel):
    revenue_growth_yoy_pct: float = Field(
        ..., description="Year-over-year revenue growth percentage"
    )
    analyst_mean_target: float = Field(..., description="Average analyst price target")
    analyst_consensus: str = Field(
        ..., description="Wall Street consensus rating (e.g., Strong Buy)"
    )
    next_earnings_date: str = Field(
        ..., description="Projected date for the next earnings report"
    )
    estimated_eps_growth_next_5y: float = Field(
        ..., description="Estimated EPS growth over the next 5 years"
    )


class ValuationMetrics(BaseModel):
    trailing_pe: float = Field(..., description="Trailing Price-to-Earnings ratio")
    forward_pe: float = Field(..., description="Forward Price-to-Earnings ratio")
    peg_ratio: float = Field(..., description="Price/Earnings to Growth ratio")
    price_to_book: float = Field(..., description="Price-to-Book ratio")
    intrinsic_value_estimate: float = Field(
        ..., description="Estimated intrinsic value of the stock"
    )
    valuation_status: str = Field(
        ..., description="Status of valuation (e.g., Undervalued, Fairly Valued)"
    )


# --- Final Agent Output Models ---


class FundamentalsAgentOutput(BaseModel):
    trading212_ticker: str = Field(
        ..., description="The Trading 212 ticker for the evaluation in question"
    )
    yfinance_ticker: str = Field(
        ..., description="The Yahoo Finance ticker for the evaluation in question"
    )
    metrics: FundamentalsMetrics = Field(
        ..., description="Financial health and margin data"
    )
    summary: str = Field(
        ..., description="Qualitative summary of the company's fundamentals"
    )


class TechnicalAgentOutput(BaseModel):
    trading212_ticker: str = Field(
        ..., description="The Trading 212 ticker for the evaluation in question"
    )
    yfinance_ticker: str = Field(
        ..., description="The Yahoo Finance ticker for the evaluation in question"
    )
    indicators: TechnicalMetrics = Field(
        ..., description="Price action and momentum indicators"
    )
    trend: str = Field(
        ..., description="Qualitative description of the current price trend"
    )


class GrowthAgentOutput(BaseModel):
    trading212_ticker: str = Field(
        ..., description="The Trading 212 ticker for the evaluation in question"
    )
    yfinance_ticker: str = Field(
        ..., description="The Yahoo Finance ticker for the evaluation in question"
    )
    forecast: GrowthMetrics = Field(
        ..., description="Future earnings and growth projections"
    )
    catalysts: str = Field(..., description="Key drivers for future growth")


class ValuationAgentOutput(BaseModel):
    trading212_ticker: str = Field(
        ..., description="The Trading 212 ticker for the evaluation in question"
    )
    yfinance_ticker: str = Field(
        ..., description="The Yahoo Finance ticker for the evaluation in question"
    )
    multiples: ValuationMetrics = Field(
        ..., description="Valuation ratios and intrinsic assessments"
    )
    assessment: str = Field(
        ..., description="Qualitative assessment of the current valuation"
    )
