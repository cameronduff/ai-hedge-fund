import os

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.genai import types
from google.adk.models.lite_llm import LiteLlm, LiteLLMClient

from dotenv import load_dotenv

from src.agents.technicals_agent.prompt import TECHNICAL_AGENT_PROMPT
from src.agents.technicals_agent.schema import TechnicalAgentOutput
from src.tools.technical_analysis import (
    calculate_trend_indicators,
    calculate_mean_reversion_indicators,
    calculate_momentum_indicators,
    calculate_volatility_indicators,
    calculate_statistical_indicators,
    combine_technical_signals,
)

load_dotenv()

DEPLOYMENT = os.environ["AZURE_DEPLOYMENT_NAME"]  # e.g. "gpt-4o-mini"

# 1) one-time setup
# model must be your Azure *deployment name*, prefixed with 'azure/'
azure_llm = LiteLlm(model=f"azure/{DEPLOYMENT}", llm_client=LiteLLMClient())

# 2) use it in your agents
# Technicals Agent with a suite of technical analysis tools
technical_agent = LlmAgent(
    model=azure_llm,  # pass the instance, not a string
    name="technical_agent",
    instruction=TECHNICAL_AGENT_PROMPT,
    tools=[
        google_search,
        calculate_trend_indicators,
        calculate_mean_reversion_indicators,
        calculate_momentum_indicators,
        calculate_volatility_indicators,
        calculate_statistical_indicators,
        combine_technical_signals,
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.2,  # Low temperature for precise technical analysis
    ),
    output_schema=TechnicalAgentOutput,
    output_key="technical_agent_output",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

if __name__ == "__main__":
    import asyncio
    import uuid
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService

    async def test_agent():
        test_ticker = "SPY"
        print(f"Testing technical agent with ticker: {test_ticker}")

        user_id = str(uuid.uuid4())
        app_name = "technical_agent_test"

        session_service = InMemorySessionService()
        session = await session_service.create_session(
            app_name=app_name, user_id=user_id
        )
        runner = Runner(
            app_name=app_name, agent=technical_agent, session_service=session_service
        )

        new_message = types.Content(
            role="user",
            parts=[
                types.Part(
                    text=f"Analyze technical indicators and price patterns for {test_ticker}"
                )
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
