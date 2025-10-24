from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.genai import types

from dotenv import load_dotenv

from src.agents.sentiment_agent.prompt import SENTIMENT_AGENT_PROMPT
from src.agents.sentiment_agent.schema import SentimentAgentOutput
from src.tools.sentiment_analysis import (
    get_company_news,
    analyze_article_sentiment,
    calculate_sentiment_metrics,
    generate_sentiment_signal,
    assess_market_sentiment,
)

load_dotenv()

# Sentiment Agent with tools for analyzing market sentiment from various sources
sentiment_agent = LlmAgent(
    model="gemini-2.5-pro",
    name="sentiment_agent",
    instruction=SENTIMENT_AGENT_PROMPT,
    tools=[
        google_search,
        get_company_news,
        analyze_article_sentiment,
        calculate_sentiment_metrics,
        generate_sentiment_signal,
        assess_market_sentiment,
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.4,  # Higher temperature to capture nuanced sentiment
    ),
    output_schema=SentimentAgentOutput,
    output_key="sentiment_agent_output",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)
