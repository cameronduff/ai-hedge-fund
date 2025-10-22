from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.genai import types

from loguru import logger
from dotenv import load_dotenv

from src.agents.mohnish_pabrai.prompt import MOHNISH_PABRAI_PROMPT

load_dotenv()


model = "gemini-2.5-pro"

detector_agent = LlmAgent(
    model=model,
    name="mohnish_pabrai",
    instruction=MOHNISH_PABRAI_PROMPT,
)
