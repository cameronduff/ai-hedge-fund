from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.genai import types

from loguru import logger
from dotenv import load_dotenv

from src.agents.portfolio_manager.prompt import PORTFOLIO_MANAGER_PROMPT

load_dotenv()


model = "gemini-2.5-pro"

detector_agent = LlmAgent(
    model=model,
    name="portfolio_manager",
    instruction=PORTFOLIO_MANAGER_PROMPT,
)
