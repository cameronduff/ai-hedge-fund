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


def exit_loop(tool_context: ToolContext):
    """Call this function ONLY when the critique indicates no further changes are needed, signaling the iterative process should end."""
    print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
    tool_context.actions.escalate = True
    # Return empty dict as tools should typically return JSON-serializable output
    return {}


# Portfolio Manager Agent with advanced portfolio management and risk assessment tools
portfolio_manager_agent = LlmAgent(
    model="gemini-2.5-pro",
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
        temperature=0.2,  # Low temperature for disciplined, systematic portfolio management
    ),
    output_schema=PortfolioManagerOutput,
)
