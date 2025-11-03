import os

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.genai import types

from src.agents.fundamentals_agent.prompt import FUNDAMENTALS_AGENT_PROMPT
from src.agents.fundamentals_agent.schema import FundamentalsAgentOutput
from src.tools.fundamental_analysis import (
    analyze_profitability_metrics,
    analyze_growth_metrics,
    analyze_financial_health,
    analyze_valuation_ratios,
    calculate_fundamental_score,
)
from src.utils.model_selector import select_model

# Automatically select the appropriate model based on available API credentials
# You can override by setting MODEL_PREFERENCE env var to "azure", "openai", or "gemini"
model_preference = os.getenv("MODEL_PREFERENCE")
selected_model = select_model(model_preference=model_preference)

# Fundamentals Agent with comprehensive financial analysis tools
fundamentals_agent = LlmAgent(
    model=selected_model,
    name="fundamentals_agent",
    instruction=FUNDAMENTALS_AGENT_PROMPT,
    tools=[
        analyze_profitability_metrics,
        analyze_growth_metrics,
        analyze_financial_health,
        analyze_valuation_ratios,
        calculate_fundamental_score,
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1,  # Very low temperature for precise fundamental analysis
    ),
    output_schema=FundamentalsAgentOutput,
    output_key="fundamentals_agent_output",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

if __name__ == "__main__":
    import asyncio
    import uuid
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService

    async def test_agent():
        # Test the fundamentals agent
        test_ticker = "AAPL"
        print(f"Testing fundamentals agent with ticker: {test_ticker}")

        user_id = str(uuid.uuid4())
        app_name = "fundamentals_agent_test"

        session_service = InMemorySessionService()
        session = await session_service.create_session(
            app_name=app_name, user_id=user_id
        )
        runner = Runner(
            app_name=app_name, agent=fundamentals_agent, session_service=session_service
        )

        new_message = types.Content(
            role="user",
            parts=[
                types.Part(text=f"Analyze the fundamental metrics for {test_ticker}")
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
