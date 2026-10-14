from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

from app.core.config import settings
from app.agents.quants.news_agent.prompt import NEWS_PROMPT
from app.models.quants_models import Ticker, NewsAgentOutput
from app.tools.news_tools import get_company_news, search_market_news


def build_news_agent(ticker_name: str, company_name: str | None = None) -> LlmAgent:
    t = ticker_name.replace(".", "_")
    planner = BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_level=types.ThinkingLevel.HIGH,
        )
    )

    generate_content_config = types.GenerateContentConfig(
        temperature=0.2,
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                attempts=5,
                initial_delay=10.0,
                max_delay=360.0,
                exp_base=2.0,
            )
        ),
    )

    company_hint = f" (Company Name: '{company_name}')" if company_name else ""
    target_instruction = (
        f"TARGET TICKER: You must strictly analyze news and sentiment for ticker '{ticker_name}'{company_hint}. "
        f"Do NOT analyze any other tickers.\n\n"
        + NEWS_PROMPT
    )

    news_agent = LlmAgent(
        name=f"news_agent_{t}",
        model=settings.QUANTS_MODEL,
        description="A market intelligence specialist that analyzes news articles, online headlines, public sentiment, catalysts, and regulatory risks.",
        instruction=target_instruction,
        planner=planner,
        tools=[
            get_company_news,
            search_market_news,
        ],
        generate_content_config=generate_content_config,
        input_schema=Ticker,
        output_schema=NewsAgentOutput,
        output_key=f"news_agent_output_{t}",
    )

    return news_agent
