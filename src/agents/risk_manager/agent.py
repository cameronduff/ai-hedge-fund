from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.genai import types

from loguru import logger
from dotenv import load_dotenv

from src.agents.risk_manager.prompt import RISK_MANAGER_PROMPT

load_dotenv()


model = "gemini-2.5-pro"

detector_agent = LlmAgent(
    model=model,
    name="risk_manager_agent",
    instruction=RISK_MANAGER_PROMPT,
)
