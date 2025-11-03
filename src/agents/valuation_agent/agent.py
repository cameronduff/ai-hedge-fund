import os

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.genai import types
from google.adk.models.lite_llm import LiteLlm, LiteLLMClient

from dotenv import load_dotenv

from src.agents.valuation_agent.prompt import VALUATION_AGENT_PROMPT
from src.agents.valuation_agent.schema import ValuationAgentOutput
from src.tools.valuation_analysis import (
    calculate_enhanced_dcf,
    calculate_owner_earnings,
    calculate_ev_ebitda_valuation,
    calculate_residual_income,
    aggregate_valuation_methods,
)

load_dotenv()

DEPLOYMENT = os.environ["AZURE_DEPLOYMENT_NAME"]  # e.g. "gpt-4o-mini"

# 1) one-time setup
# model must be your Azure *deployment name*, prefixed with 'azure/'
azure_llm = LiteLlm(model=f"azure/{DEPLOYMENT}", llm_client=LiteLLMClient())

# 2) use it in your agents
# Valuation Agent with a variety of valuation model tools
valuation_agent = LlmAgent(
    model=azure_llm,  # pass the instance, not a string
    name="valuation_agent",
    instruction=VALUATION_AGENT_PROMPT,
    tools=[
        google_search,
        calculate_enhanced_dcf,
        calculate_owner_earnings,
        calculate_ev_ebitda_valuation,
        calculate_residual_income,
        aggregate_valuation_methods,
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=1.0,  # Low temperature for precise, data-driven valuation
    ),
    output_schema=ValuationAgentOutput,
    output_key="valuation_agent_output",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

if __name__ == "__main__":
    import asyncio
    import uuid
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService

    async def test_agent():
        test_ticker = "MSFT"
        print(f"Testing valuation agent with ticker: {test_ticker}")

        user_id = str(uuid.uuid4())
        app_name = "valuation_agent_test"

        session_service = InMemorySessionService()
        session = await session_service.create_session(
            app_name=app_name, user_id=user_id
        )
        runner = Runner(
            app_name=app_name, agent=valuation_agent, session_service=session_service
        )

        new_message = types.Content(
            role="user",
            parts=[
                types.Part(
                    text=f"Perform comprehensive valuation analysis for {test_ticker}"
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
