from google.adk.agents import LlmAgent

from app.core.config import settings
from app.agents.news_sentiment_agent.prompt import NEWS_SENTIMENT_PROMPT

news_sentiment_agent = LlmAgent(
    name="news_sentiment_agent",
    model=settings.REASONING_MODEL,
    instruction=NEWS_SENTIMENT_PROMPT,
)
