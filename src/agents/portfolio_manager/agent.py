import os

from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext
from google.genai import types

from src.agents.portfolio_manager.prompt import PORTFOLIO_MANAGER_PROMPT
from src.agents.portfolio_manager.schema import PortfolioManagerOutput
from src.tools.portfolio_management import (
    analyze_signal_consensus,
    calculate_position_size,
    assess_portfolio_risk,
    optimize_trade_timing,
)
from src.utils.model_selector import select_model


def exit_loop(tool_context: ToolContext):
    """Call this function ONLY when the critique indicates no further changes are needed, signaling the iterative process should end."""
    print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
    tool_context.actions.escalate = True
    # Return empty dict as tools should typically return JSON-serializable output
    return {}


# Automatically select the appropriate model
model_preference = os.getenv("MODEL_PREFERENCE")
selected_model = select_model(model_preference=model_preference)

# Portfolio Manager Agent with advanced portfolio management and risk assessment tools
portfolio_manager_agent = LlmAgent(
    model=selected_model,
    name="portfolio_manager_agent",
    instruction=PORTFOLIO_MANAGER_PROMPT,
    tools=[
        analyze_signal_consensus,
        calculate_position_size,
        assess_portfolio_risk,
        optimize_trade_timing,
        exit_loop,
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.5,  # Moderate temperature for balanced decision-making
    ),
    output_schema=PortfolioManagerOutput,
    output_key="portfolio_manager_output",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

if __name__ == "__main__":
    import asyncio
    import uuid
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService

    async def test_agent():
        print("Testing portfolio manager agent")

        user_id = str(uuid.uuid4())
        app_name = "portfolio_manager_test"

        session_service = InMemorySessionService()
        session = await session_service.create_session(
            app_name=app_name, user_id=user_id
        )
        runner = Runner(
            app_name=app_name,
            agent=portfolio_manager_agent,
            session_service=session_service,
        )

        new_message = types.Content(
            role="user",
            parts=[
                types.Part(
                    text="Analyze portfolio allocation and optimize position sizing for a tech-heavy portfolio"
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
