from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types
from app.models.investors_models import InvestorResponse

from app.core.config import settings
from app.agents.investors.investor_formatter_agent.prompt import INVESTOR_FORMATTING_PROMPT

def build_investor_formatter_agent(investor_name: str):
    investor_formatter_agent = LlmAgent(
        name=f"investor_formatter_agent_{investor_name}",
        model=settings.FORMATTING_MODEL,
        instruction=INVESTOR_FORMATTING_PROMPT,
        output_schema=InvestorResponse,
        output_key=f"{investor_name}_agent_output",
        generate_content_config=types.GenerateContentConfig(
            temperature=0.2,
            http_options=types.HttpOptions(
                retry_options=types.HttpRetryOptions(
                    attempts=5,
                    initial_delay=10.0,
                    max_delay=360.0,
                    multiplier=2.0,
                )
            ),
        ),
    )

    return investor_formatter_agent