from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.genai import types

from loguru import logger
from dotenv import load_dotenv

from src.agents.michael_burry.prompt import MICHAEL_BURRY_PROMPT

load_dotenv()

model = "gemini-2.5-pro"

detector_agent = LlmAgent(
    model=model,
    name="michael_burry_agent",
    instruction=MICHAEL_BURRY_PROMPT,
)
