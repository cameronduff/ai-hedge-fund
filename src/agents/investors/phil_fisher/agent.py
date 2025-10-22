from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.genai import types

from loguru import logger
from dotenv import load_dotenv

from src.agents.phil_fisher.prompt import PHIL_FISHER_PROMPT

load_dotenv()


model = "gemini-2.5-pro"

detector_agent = LlmAgent(
    model=model,
    name="phil_fisher_agent",
    instruction=PHIL_FISHER_PROMPT,
)
