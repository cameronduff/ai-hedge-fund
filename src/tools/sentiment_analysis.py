import json
import math
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta


def get_company_news(ticker_data: str) -> str:
    """
    Fetch recent news articles for a company ticker.

    Args:
        ticker_data: JSON string containing ticker and date parameters

    Returns:
        JSON string with news articles data
    """
    try:
        data = json.loads(ticker_data)
        ticker = data.get("ticker", "")
        end_date = data.get("end_date", "")
        limit = data.get("limit", 20)

        # Simulate fetching news data - in real implementation, this would call an API
        # For now, return mock structure that matches expected format
        news_articles = [
            {
                "id": f"news_{i}",
                "title": f"Sample news article {i} for {ticker}",
                "published_date": end_date,
                "source": "Financial News",
                "sentiment": None,  # Will be analyzed
                "url": f"https://example.com/news/{i}",
            }
            for i in range(min(limit, 10))
        ]

        return json.dumps(
            {
                "ticker": ticker,
                "articles": news_articles,
                "total_count": len(news_articles),
            }
        )

    except Exception as e:
        return json.dumps(
            {
                "ticker": ticker if "ticker" in locals() else "",
                "articles": [],
                "total_count": 0,
                "error": f"Error fetching news: {str(e)}",
            }
        )


def analyze_article_sentiment(article_data: str) -> str:
    """
    Analyze the sentiment of individual news articles.

    Args:
        article_data: JSON string containing article information

    Returns:
        JSON string with sentiment analysis results
    """
    try:
        data = json.loads(article_data)
        articles = data.get("articles", [])

        analyzed_articles = []

        for article in articles:
            title = article.get("title", "")

            # Simple keyword-based sentiment analysis
            # In real implementation, this would use more sophisticated NLP
            positive_keywords = [
                "growth",
                "profit",
                "gain",
                "success",
                "beat",
                "exceed",
                "positive",
                "strong",
                "rise",
                "increase",
                "expansion",
                "partnership",
            ]
            negative_keywords = [
                "loss",
                "decline",
                "fall",
                "miss",
                "weak",
                "negative",
                "drop",
                "lawsuit",
                "scandal",
                "layoff",
                "bankruptcy",
                "risk",
            ]

            title_lower = title.lower()
            positive_count = sum(1 for word in positive_keywords if word in title_lower)
            negative_count = sum(1 for word in negative_keywords if word in title_lower)

            if positive_count > negative_count:
                sentiment = "positive"
                confidence = min(85 + (positive_count * 5), 95)
            elif negative_count > positive_count:
                sentiment = "negative"
                confidence = min(85 + (negative_count * 5), 95)
            else:
                sentiment = "neutral"
                confidence = 60

            analyzed_article = {
                **article,
                "sentiment": sentiment,
                "confidence": confidence,
                "positive_signals": positive_count,
                "negative_signals": negative_count,
            }
            analyzed_articles.append(analyzed_article)

        return json.dumps(
            {
                "analyzed_articles": analyzed_articles,
                "total_analyzed": len(analyzed_articles),
            }
        )

    except Exception as e:
        return json.dumps(
            {
                "analyzed_articles": [],
                "total_analyzed": 0,
                "error": f"Error analyzing sentiment: {str(e)}",
            }
        )


def calculate_sentiment_metrics(sentiment_data: str) -> str:
    """
    Calculate aggregated sentiment metrics from analyzed articles.

    Args:
        sentiment_data: JSON string containing sentiment analysis results

    Returns:
        JSON string with aggregated metrics
    """
    try:
        data = json.loads(sentiment_data)
        articles = data.get("analyzed_articles", [])

        if not articles:
            return json.dumps(
                {
                    "total_articles": 0,
                    "bullish_articles": 0,
                    "bearish_articles": 0,
                    "neutral_articles": 0,
                    "average_confidence": 0.0,
                    "sentiment_score": 0.0,
                }
            )

        # Count sentiment categories
        positive_count = sum(
            1 for article in articles if article.get("sentiment") == "positive"
        )
        negative_count = sum(
            1 for article in articles if article.get("sentiment") == "negative"
        )
        neutral_count = sum(
            1 for article in articles if article.get("sentiment") == "neutral"
        )

        # Calculate average confidence
        confidences = [article.get("confidence", 0) for article in articles]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0

        # Calculate sentiment score (-1 to 1)
        total_articles = len(articles)
        sentiment_score = (
            (positive_count - negative_count) / total_articles
            if total_articles > 0
            else 0
        )

        metrics = {
            "total_articles": total_articles,
            "bullish_articles": positive_count,
            "bearish_articles": negative_count,
            "neutral_articles": neutral_count,
            "average_confidence": round(avg_confidence, 2),
            "sentiment_score": round(sentiment_score, 3),
            "positive_ratio": (
                round(positive_count / total_articles, 3) if total_articles > 0 else 0
            ),
            "negative_ratio": (
                round(negative_count / total_articles, 3) if total_articles > 0 else 0
            ),
        }

        return json.dumps(metrics)

    except Exception as e:
        return json.dumps(
            {
                "total_articles": 0,
                "bullish_articles": 0,
                "bearish_articles": 0,
                "neutral_articles": 0,
                "average_confidence": 0.0,
                "sentiment_score": 0.0,
                "error": f"Error calculating metrics: {str(e)}",
            }
        )


def generate_sentiment_signal(metrics_data: str) -> str:
    """
    Generate trading signals from sentiment metrics.

    Args:
        metrics_data: JSON string containing sentiment metrics

    Returns:
        JSON string with trading signal and confidence
    """
    try:
        data = json.loads(metrics_data)

        sentiment_score = data.get("sentiment_score", 0)
        avg_confidence = data.get("average_confidence", 0)
        total_articles = data.get("total_articles", 0)
        positive_ratio = data.get("positive_ratio", 0)
        negative_ratio = data.get("negative_ratio", 0)

        # Minimum article threshold for reliable signal
        if total_articles < 3:
            return json.dumps(
                {
                    "signal": "neutral",
                    "confidence": 30,
                    "reasoning": "Insufficient news coverage for reliable sentiment signal",
                }
            )

        # Determine signal based on sentiment score and ratios
        if sentiment_score > 0.2 and positive_ratio > 0.4:
            signal = "bullish"
            base_confidence = min(avg_confidence * (positive_ratio + 0.3), 95)
        elif sentiment_score < -0.2 and negative_ratio > 0.4:
            signal = "bearish"
            base_confidence = min(avg_confidence * (negative_ratio + 0.3), 95)
        else:
            signal = "neutral"
            base_confidence = 50 + (avg_confidence * 0.2)

        # Adjust confidence based on article volume
        volume_multiplier = min(1.0 + (total_articles - 3) * 0.05, 1.2)
        final_confidence = min(base_confidence * volume_multiplier, 95)

        result = {
            "signal": signal,
            "confidence": round(final_confidence, 2),
            "sentiment_score": sentiment_score,
            "reasoning": f"Signal based on {total_articles} articles with {positive_ratio:.1%} positive, {negative_ratio:.1%} negative sentiment",
        }

        return json.dumps(result)

    except Exception as e:
        return json.dumps(
            {
                "signal": "neutral",
                "confidence": 0,
                "error": f"Error generating signal: {str(e)}",
            }
        )


def assess_market_sentiment(multi_ticker_data: str) -> str:
    """
    Evaluate overall market sentiment across multiple tickers.

    Args:
        multi_ticker_data: JSON string containing sentiment data for multiple tickers

    Returns:
        JSON string with market-wide sentiment assessment
    """
    try:
        data = json.loads(multi_ticker_data)
        ticker_signals = data.get("ticker_signals", {})

        if not ticker_signals:
            return json.dumps(
                {
                    "market_sentiment": "neutral",
                    "confidence": 0,
                    "bullish_tickers": 0,
                    "bearish_tickers": 0,
                    "neutral_tickers": 0,
                }
            )

        # Count signals across tickers
        bullish_count = 0
        bearish_count = 0
        neutral_count = 0
        total_confidence = 0

        for ticker, signal_data in ticker_signals.items():
            signal = signal_data.get("signal", "neutral")
            confidence = signal_data.get("confidence", 0)

            if signal == "bullish":
                bullish_count += 1
            elif signal == "bearish":
                bearish_count += 1
            else:
                neutral_count += 1

            total_confidence += confidence

        total_tickers = len(ticker_signals)
        avg_confidence = total_confidence / total_tickers if total_tickers > 0 else 0

        # Determine overall market sentiment
        bullish_ratio = bullish_count / total_tickers if total_tickers > 0 else 0
        bearish_ratio = bearish_count / total_tickers if total_tickers > 0 else 0

        if bullish_ratio > 0.6:
            market_sentiment = "bullish"
            market_confidence = min(avg_confidence * (bullish_ratio + 0.2), 90)
        elif bearish_ratio > 0.6:
            market_sentiment = "bearish"
            market_confidence = min(avg_confidence * (bearish_ratio + 0.2), 90)
        else:
            market_sentiment = "neutral"
            market_confidence = avg_confidence * 0.7

        assessment = {
            "market_sentiment": market_sentiment,
            "confidence": round(market_confidence, 2),
            "bullish_tickers": bullish_count,
            "bearish_tickers": bearish_count,
            "neutral_tickers": neutral_count,
            "total_tickers": total_tickers,
            "bullish_ratio": round(bullish_ratio, 3),
            "bearish_ratio": round(bearish_ratio, 3),
            "average_confidence": round(avg_confidence, 2),
        }

        return json.dumps(assessment)

    except Exception as e:
        return json.dumps(
            {
                "market_sentiment": "neutral",
                "confidence": 0,
                "error": f"Error assessing market sentiment: {str(e)}",
            }
        )
