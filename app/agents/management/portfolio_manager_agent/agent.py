from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types
from google.adk.tools.agent_tool import AgentTool

from app.core.config import settings
from app.agents.management.portfolio_manager_agent.prompt import (
    PORTFOLIO_MANAGER_PROMPT,
    PORTFOLIO_MANAGER_FORMATTER_PROMPT,
)
from app.agents.management.risk_manager_agent.agent import risk_manager_agent
from app.tools.trading212_tools import fetch_all_open_positions, get_account_summary
from app.tools.calculation_tools import (
    calculate_position_size,
    calculate_remaining_cash,
    calculate_position_value,
    calculate_portfolio_concentration,
)
from app.models.management_models import PortfolioManagerOutput

portfolio_manager = LlmAgent(
    name="portfolio_manager",
    model=settings.REASONING_MODEL,
    instruction=PORTFOLIO_MANAGER_PROMPT,
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_level=types.ThinkingLevel.HIGH,
        )
    ),
    generate_content_config=types.GenerateContentConfig(
        temperature=0.0,
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                attempts=5,
                initial_delay=10.0,
                max_delay=360.0,
                exp_base=2.0,
            )
        ),
    ),
    tools=[
        fetch_all_open_positions, 
        get_account_summary,
        calculate_position_size,
        calculate_remaining_cash,
        calculate_position_value,
        calculate_portfolio_concentration,
        AgentTool(agent=risk_manager_agent),
    ],
    sub_agents=[risk_manager_agent],
    output_key="portfolio_manager_raw_output"
)

porfolio_manager_formatter_agent = LlmAgent(
    name="porfolio_manager_formatter_agent",
    model=settings.FORMATTING_MODEL,
    instruction=PORTFOLIO_MANAGER_FORMATTER_PROMPT,
    output_schema=PortfolioManagerOutput,
    output_key="portfolio_manager_output",
    generate_content_config=types.GenerateContentConfig(
        temperature=0.2,
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                attempts=5,
                initial_delay=10.0,
                max_delay=360.0,
                exp_base=2.0,
            )
        ),
    ),
)

portfolio_manager_agent = SequentialAgent(
    name="portfolio_manager_agent",
    sub_agents=[
        portfolio_manager,
        porfolio_manager_formatter_agent
    ]
)


if __name__ == "__main__":
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.adk.plugins import ReflectAndRetryToolPlugin
    from uuid import uuid4
    import asyncio
    from dotenv import load_dotenv
    from google.genai import types
    from loguru import logger

    from app.models.investors_models import (
        CIOOutput,
        InvestmentDecision,
        InvestorPosition,
    )

    load_dotenv(".env.local")

    APP_NAME = "ai_hedge_fund"
    USER_ID = str(uuid4())
    SESSION_ID = str(uuid4())

    # --- Dummy CIO Output ---
    dummy_cio_output = CIOOutput(
        decisions=[
            InvestmentDecision(
                trading212_ticker="AAPL",
                yfinance_ticker="AAPL",
                final_rating="SELL",
                consensus_strength="STRONG",
                position_size_pct=0.0,
                target_price=245.0,
                time_horizon_months=12,
                key_catalysts=[
                    "Miss in iPhone sell-through data relative to super-cycle expectations.",
                    "Multiple contraction as market re-rates AAPL from AI Growth to Hardware Mature.",
                    "Technical reversal as price fails to break 52-week high of $288.35.",
                ],
                key_risks=[
                    "Non-linear surge in high-margin Services revenue.",
                    "Continued aggressive buybacks supporting share price regardless of valuation.",
                    "Widespread Apple Intelligence adoption leading to unexpected hardware replacement.",
                ],
                investor_positions=[
                    InvestorPosition(
                        investor_name="Benjamin Graham",
                        rating="SELL",
                        conviction="HIGH",
                        key_thesis="Current valuation represents a triumph of optimism over arithmetic with no margin of safety.",
                    ),
                    InvestorPosition(
                        investor_name="Michael Burry",
                        rating="SELL",
                        conviction="HIGH",
                        key_thesis="Market is paying for thin air while ignoring consumer credit exhaustion.",
                    ),
                    InvestorPosition(
                        investor_name="Warren Buffett",
                        rating="HOLD",
                        conviction="MEDIUM",
                        key_thesis="Moat is wide but current price lacks a fat pitch margin of safety.",
                    ),
                    InvestorPosition(
                        investor_name="Phil Fisher",
                        rating="BUY",
                        conviction="MEDIUM",
                        key_thesis="Premier compounder satisfying market potential through AI-led upgrade cycle.",
                    ),
                ],
                dissenting_views="Fisher's BUY overruled due to extreme 47x book value entry price. Buffett's HOLD overruled due to clear capital impairment risk.",
                debate_summary="Board debated whether Apple's ecosystem moat justifies extreme valuation. Value camp argued PEG and P/B ratios are mathematically indefensible. CIO determined AI premium is fully priced in.",
            ),
            InvestmentDecision(
                trading212_ticker="MSFT",
                yfinance_ticker="MSFT",
                final_rating="BUY",
                consensus_strength="UNANIMOUS",
                position_size_pct=15.0,
                target_price=550.0,
                time_horizon_months=36,
                key_catalysts=[
                    "Reclaiming SMA_200 at $465, triggering institutional momentum buying.",
                    "Azure growth acceleration driven by Tier-1 enterprise AI migrations.",
                    "EPS growth exceeding 19.15% estimate as Copilot transitions to standard licensing.",
                ],
                key_risks=[
                    "Massive AI CapEx fails to yield ROIC above 15% in the medium term.",
                    "Regulatory intervention in cloud/AI market.",
                    "Broader macro liquidity crunch forcing sell-off in tech.",
                ],
                investor_positions=[
                    InvestorPosition(
                        investor_name="Warren Buffett",
                        rating="BUY",
                        conviction="HIGH",
                        key_thesis="Essential digital plumbing of the modern world trading as a wonderful company at a fair price.",
                    ),
                    InvestorPosition(
                        investor_name="Charlie Munger",
                        rating="BUY",
                        conviction="HIGH",
                        key_thesis="Demonstrates Lollapalooza effect of scale and pricing power with elite balance sheet.",
                    ),
                    InvestorPosition(
                        investor_name="Benjamin Graham",
                        rating="HOLD",
                        conviction="MEDIUM",
                        key_thesis="Superior financial fortitude but current ratio below defensive benchmark.",
                    ),
                    InvestorPosition(
                        investor_name="Nassim Taleb",
                        rating="BUY",
                        conviction="MEDIUM",
                        key_thesis="Exhibits robustness through low leverage and high cash generation.",
                    ),
                ],
                dissenting_views="Graham's HOLD overruled — demand for 2.0 current ratio is antiquated for SaaS-heavy business model with high deferred revenue.",
                debate_summary="Board debated waiting for technical confirmation vs buying on fundamental value. CIO sided with majority viewing reinvestment as competitive advantage.",
            ),
        ],
        portfolio_notes="Portfolio skewed toward Software/Infrastructure (MSFT) and away from Consumer Hardware (AAPL). Liquidate AAPL to capture euphoria premium and redeploy 15% into MSFT.",
    )

    session_service = InMemorySessionService()
    asyncio.run(
        session_service.create_session(
            app_name=APP_NAME,
            session_id=SESSION_ID,
            user_id=USER_ID,
            state={
                "chief_investment_officer_output": dummy_cio_output.model_dump(),
            },
        )
    )

    runner = Runner(
        agent=portfolio_manager_agent,
        app_name=APP_NAME,
        session_service=session_service,
        plugins=[ReflectAndRetryToolPlugin(max_retries=3)],
    )

    content = types.Content(
        role="user",
        parts=[types.Part(text="Review the CIO recommendations and manage the portfolio accordingly.")],
    )

    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    for event in events:
        logger.info(f"[{event.author}] is_final={event.is_final_response()} content={bool(event.content)}")
        if event.is_final_response() and event.content:
            logger.info(event.content.parts[0].text.strip()[:300])

    final_session = asyncio.run(
        session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )
    )

    from app.models.management_models import PortfolioManagerOutput
    portfolio_output = PortfolioManagerOutput.model_validate(
        final_session.state["portfolio_manager_output"]
    )
    logger.info("======================================================")
    logger.info(portfolio_output.model_dump_json(indent=2))