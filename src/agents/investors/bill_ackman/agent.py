from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.genai import types

from loguru import logger
from dotenv import load_dotenv

from src.agents.bill_ackman.prompt import BILL_ACKMAN_PROMPT

load_dotenv()


model = "gemini-2.5-pro"

detector_agent = LlmAgent(
    model=model,
    name="bill_ackman_agent",
    instruction=BILL_ACKMAN_PROMPT,
)
