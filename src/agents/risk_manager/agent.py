import os

from google.adk.agents import LlmAgent
from google.genai import types

from src.agents.risk_manager.prompt import RISK_MANAGER_PROMPT
from src.agents.risk_manager.schema import RiskManagerOutput
from src.tools.risk_analysis import (
    calculate_volatility_metrics,
    calculate_volatility_adjusted_limit,
    analyze_correlation_risk,
    calculate_position_limits,
    assess_portfolio_risk_concentration,
)
from src.utils.model_selector import select_model

# Automatically select the appropriate model
model_preference = os.getenv("MODEL_PREFERENCE")
selected_model = select_model(model_preference=model_preference)

# Risk Manager Agent with comprehensive risk analysis and position sizing tools
risk_manager_agent = LlmAgent(
    model=selected_model,
    name="risk_manager_agent",
    instruction=RISK_MANAGER_PROMPT,
    tools=[
        calculate_volatility_metrics,
        calculate_volatility_adjusted_limit,
        analyze_correlation_risk,
        calculate_position_limits,
        assess_portfolio_risk_concentration,
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.0,  # Very low temperature for precise risk calculations
    ),
    output_schema=RiskManagerOutput,
    output_key="risk_manager_output",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

if __name__ == "__main__":
    import asyncio
    import uuid
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService

    async def test_agent():
        test_ticker = "GOOGL"
        print(f"Testing risk manager agent with ticker: {test_ticker}")

        user_id = str(uuid.uuid4())
        app_name = "risk_manager_test"

        session_service = InMemorySessionService()
        session = await session_service.create_session(
            app_name=app_name, user_id=user_id
        )
        runner = Runner(
            app_name=app_name, agent=risk_manager_agent, session_service=session_service
        )

        new_message = types.Content(
            role="user",
            parts=[
                types.Part(
                    text=f"Assess risk metrics and position limits for {test_ticker}"
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
