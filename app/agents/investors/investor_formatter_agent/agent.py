from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types
from app.models.investors_models import InvestorResponse

from app.core.config import settings
from app.agents.investors.investor_formatter_agent.prompt import INVESTOR_FORMATTING_PROMPT

def build_investor_formatter_agent(investor_name: str):
    i = investor_name.replace(".", "_")
    investor_formatter_agent = LlmAgent(
        name=f"investor_formatter_agent_{i}",
        model=settings.FORMATTING_MODEL,
        instruction=INVESTOR_FORMATTING_PROMPT,
        output_schema=InvestorResponse,
        output_key=f"{i}_agent_output",
        generate_content_config=types.GenerateContentConfig(
            temperature=0.2,
            http_options=types.HttpOptions(
            timeout=180000,
                retry_options=types.HttpRetryOptions(
                attempts=3,
                initial_delay=5.0,
                max_delay=30.0,
                exp_base=2.0,
            )
            ),
        ),
    )

    return investor_formatter_agent