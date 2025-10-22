from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class SentimentMetrics(BaseModel):
    """Metrics for sentiment analysis"""

    total_articles: int = Field(description="Total number of articles analyzed")
    bullish_articles: int = Field(description="Number of bullish articles")
    bearish_articles: int = Field(description="Number of bearish articles")
    neutral_articles: int = Field(description="Number of neutral articles")
    articles_classified_by_llm: int = Field(
        description="Number of articles classified by LLM"
    )
    average_confidence: float = Field(
        description="Average confidence score from LLM classifications"
    )


class SentimentAnalysis(BaseModel):
    """Individual sentiment analysis for a ticker"""

    signal: str = Field(
        description="Overall sentiment signal: bullish, bearish, or neutral"
    )
    confidence: float = Field(description="Confidence score between 0-100")
    metrics: SentimentMetrics = Field(description="Detailed sentiment metrics")
    reasoning: str = Field(description="Explanation of the sentiment analysis")


class SentimentAgentOutput(BaseModel):
    """Output schema for sentiment analysis agent"""

    sentiment_analysis: Dict[str, SentimentAnalysis] = Field(
        description="Sentiment analysis results for each ticker"
    )
    summary: str = Field(
        description="Overall summary of sentiment analysis across all tickers"
    )
    market_sentiment: str = Field(
        description="Overall market sentiment: bullish, bearish, or neutral"
    )
    total_tickers_analyzed: int = Field(description="Total number of tickers analyzed")
