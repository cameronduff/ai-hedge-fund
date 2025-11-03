import os

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
from src.utils.model_selector import select_model

load_dotenv()

# Use Azure for this agent - has get_company_news tool, doesn't need google_search
model_preference = os.getenv("MODEL_PREFERENCE")
selected_model = select_model(model_preference=model_preference)

# Sentiment Agent with tools for analyzing market sentiment from various sources
sentiment_agent = LlmAgent(
    model=selected_model,
    name="sentiment_agent",
    instruction=SENTIMENT_AGENT_PROMPT,
    tools=[
        get_company_news,
        analyze_article_sentiment,
        calculate_sentiment_metrics,
        generate_sentiment_signal,
        assess_market_sentiment,
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.3,  # Moderate temperature to capture nuanced sentiment
    ),
    output_schema=SentimentAgentOutput,
    output_key="sentiment_agent_output",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

if __name__ == "__main__":
    import asyncio
    import uuid
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService

    async def test_agent():
        test_ticker = "TSLA"
        print(f"Testing sentiment agent with ticker: {test_ticker}")

        user_id = str(uuid.uuid4())
        app_name = "sentiment_agent_test"

        session_service = InMemorySessionService()
        session = await session_service.create_session(
            app_name=app_name, user_id=user_id
        )
        runner = Runner(
            app_name=app_name, agent=sentiment_agent, session_service=session_service
        )

        new_message = types.Content(
            role="user",
            parts=[
                types.Part(text=f"Analyze market sentiment and news for {test_ticker}")
            ],
        )

        print("\n" + "=" * 50)
        print("Agent Response:")
        print("=" * 50)

        async for event in runner.run_async(
            user_id=user_id,
            session_id=session.id,
            new_message=new_message,
        ):
            if getattr(event, "is_final_response", lambda: False)():
                if event.content and event.content.parts:
                    print(event.content.parts[0].text)

    asyncio.run(test_agent())
