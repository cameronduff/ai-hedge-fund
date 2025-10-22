from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.genai import types

from loguru import logger
from dotenv import load_dotenv

from src.agents.technicals_agent.prompt import TECHNICALS_AGENT_PROMPT

load_dotenv()


model = "gemini-2.5-pro"

detector_agent = LlmAgent(
    model=model,
    name="technicals_agent",
    instruction=TECHNICALS_AGENT_PROMPT,
)
