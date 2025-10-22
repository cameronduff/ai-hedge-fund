from google.adk.agents import LlmAgent
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

sentiment_agent = LlmAgent(
    model="gemini-2.5-pro",
    name="sentiment_analysis_agent",
    instruction=SENTIMENT_AGENT_PROMPT,
    tools=[
        get_company_news,
        analyze_article_sentiment,
        calculate_sentiment_metrics,
        generate_sentiment_signal,
        assess_market_sentiment,
    ],
    response_config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=SentimentAgentOutput.model_json_schema(),
        temperature=0.1,
    ),
)
