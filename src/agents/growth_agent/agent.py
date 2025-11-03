import os

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.genai import types

from src.agents.growth_agent.prompt import GROWTH_AGENT_PROMPT
from src.agents.growth_agent.schema import GrowthAgentOutput
from src.tools.growth_analysis import (
    calculate_trend_slope,
    analyze_historical_growth,
    analyze_growth_valuation,
    analyze_margin_expansion,
    analyze_insider_activity,
    assess_financial_stability,
)
from src.utils.model_selector import select_model

# Force Gemini for this agent to enable google_search tool
selected_model = select_model(model_preference="gemini")

# Growth Agent with tools for analyzing growth drivers and projecting future performance
growth_agent = LlmAgent(
    model=selected_model,
    name="growth_agent",
    instruction=GROWTH_AGENT_PROMPT,
    tools=[
        google_search,
        calculate_trend_slope,
        analyze_historical_growth,
        analyze_growth_valuation,
        analyze_margin_expansion,
        analyze_insider_activity,
        assess_financial_stability,
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.3,  # Moderate temperature for balanced growth analysis
    ),
    output_schema=GrowthAgentOutput,
    output_key="growth_agent_output",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

if __name__ == "__main__":
    import asyncio
    import uuid
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService

    async def test_agent():
        test_ticker = "NVDA"
        print(f"Testing growth agent with ticker: {test_ticker}")

        user_id = str(uuid.uuid4())
        app_name = "growth_agent_test"

        session_service = InMemorySessionService()
        session = await session_service.create_session(
            app_name=app_name, user_id=user_id
        )
        runner = Runner(
            app_name=app_name, agent=growth_agent, session_service=session_service
        )

        new_message = types.Content(
            role="user",
            parts=[
                types.Part(
                    text=f"Analyze the growth metrics and prospects for {test_ticker}"
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
