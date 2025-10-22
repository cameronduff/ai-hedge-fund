from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.genai import types

from loguru import logger
from dotenv import load_dotenv

from src.agents.rakesh_jhunjhunwala.prompt import RAKESH_JHUNJHUNWALA_PROMPT

load_dotenv()


model = "gemini-2.5-pro"

detector_agent = LlmAgent(
    model=model,
    name="rakesh_jhunjhunwala_agent",
    instruction=RAKESH_JHUNJHUNWALA_PROMPT,
)
