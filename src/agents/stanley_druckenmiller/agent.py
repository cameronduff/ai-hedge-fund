from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.genai import types

from loguru import logger
from dotenv import load_dotenv

from src.agents.stanley_druckenmiller.prompt import STANLEY_DRUCKENMILLER_PROMPT

load_dotenv()


model = "gemini-2.5-pro"

detector_agent = LlmAgent(
    model=model,
    name="stanley_druckenmiller_agent",
    instruction=STANLEY_DRUCKENMILLER_PROMPT,
)
