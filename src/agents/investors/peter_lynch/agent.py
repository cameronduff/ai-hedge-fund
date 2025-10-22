from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.genai import types

from loguru import logger
from dotenv import load_dotenv

from src.agents.peter_lynch.prompt import PETER_LYNCH_PROMPT

load_dotenv()


model = "gemini-2.5-pro"

detector_agent = LlmAgent(
    model=model,
    name="peter_lynch_agent",
    instruction=PETER_LYNCH_PROMPT,
    generate_content_config=types.GenerateContentConfig(temperature=0.2),
)
