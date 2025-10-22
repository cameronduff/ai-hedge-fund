from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.genai import types

from loguru import logger
from dotenv import load_dotenv

from src.agents.cathie_wood.prompt import CATHIE_WOOD_PROMPT

load_dotenv()


model = "gemini-2.5-pro"

detector_agent = LlmAgent(
    model=model,
    name="cathie_wood",
    instruction=CATHIE_WOOD_PROMPT,
    generate_content_config=types.GenerateContentConfig(temperature=0.2),
)
