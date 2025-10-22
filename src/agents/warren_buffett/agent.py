from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.genai import types

from loguru import logger
from dotenv import load_dotenv

from src.agents.warren_buffett.prompt import WARREN_BUFFETT_PROMPT

load_dotenv()


model = "gemini-2.5-pro"

detector_agent = LlmAgent(
    model=model,
    name="warren_buffett",
    instruction=WARREN_BUFFETT_PROMPT,
)
