from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.genai import types

from loguru import logger
from dotenv import load_dotenv

load_dotenv()


model = "gemini-2.5-pro"

detector_agent = LlmAgent(
    model=model,
    name="compliance_detector_agent",
    description="Watches content and notes any categories that DO appear in the content.",
    instruction="""""",
    generate_content_config=types.GenerateContentConfig(temperature=0.2),
)
