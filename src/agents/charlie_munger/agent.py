from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.genai import types

from loguru import logger
from dotenv import load_dotenv

from src.agents.charlie_munger.prompt import CHARLIE_MUNGER_PROMPT

load_dotenv()


model = "gemini-2.5-pro"

detector_agent = LlmAgent(
    model=model,
    name="charlie_munger_agent",
    instruction=CHARLIE_MUNGER_PROMPT,
)
