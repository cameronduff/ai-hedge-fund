from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.genai import types

from loguru import logger
from dotenv import load_dotenv

from src.agents.sentiment_agent.prompt import SENTIMENT_AGENT_PROMPT

load_dotenv()


model = "gemini-2.5-pro"

detector_agent = LlmAgent(
    model=model,
    name="sentiment_agent",
    instruction=SENTIMENT_AGENT_PROMPT,
)
