import json

from typing import AsyncGenerator, Dict, List, Optional, Tuple
from collections import Counter
from loguru import logger
from google.adk.agents import SequentialAgent, ParallelAgent, BaseAgent, LoopAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.genai.types import Content, Part

from src.agents.retrying_agent.agent import wrap_llm_agents_with_retry

from src.agents.fundamentals_agent.agent import fundamentals_agent
from src.agents.technicals_agent.agent import technical_agent
from src.agents.sentiment_agent.agent import sentiment_agent
from src.agents.valuation_agent.agent import valuation_agent

from src.agents.investors.aswath_damodaran.agent import aswath_damodaran_agent
from src.agents.investors.ben_graham.agent import ben_graham_agent
from src.agents.investors.bill_ackman.agent import bill_ackman_agent
from src.agents.investors.cathie_wood.agent import cathie_wood_agent
from src.agents.investors.charlie_munger.agent import charlie_munger_agent
from src.agents.investors.michael_burry.agent import michael_burry_agent
from src.agents.investors.mohnish_pabrai.agent import mohnish_pabrai_agent
from src.agents.investors.peter_lynch.agent import peter_lynch_agent
from src.agents.investors.phil_fisher.agent import phil_fisher_agent
from src.agents.investors.rakesh_jhunjhunwala.agent import rakesh_jhunjhunwala_agent
from src.agents.investors.stanley_druckenmiller.agent import stanley_druckenmiller_agent
from src.agents.investors.warren_buffett.agent import warren_buffett_agent

from src.agents.risk_manager.agent import risk_manager_agent
from src.agents.portfolio_manager.agent import portfolio_manager_agent


# ---------------------------------------------------------------------
# Build the full parallel pipeline + collector
# ---------------------------------------------------------------------
def get_pipeline() -> BaseAgent:

    research = ParallelAgent(
        name="research_agent",
        sub_agents=[
            fundamentals_agent,
            technical_agent,
            sentiment_agent,
            valuation_agent,
        ],
    )

    investors = ParallelAgent(
        name="investors_agent",
        sub_agents=[
            aswath_damodaran_agent,
            ben_graham_agent,
            bill_ackman_agent,
            cathie_wood_agent,
            charlie_munger_agent,
            michael_burry_agent,
            mohnish_pabrai_agent,
            peter_lynch_agent,
            phil_fisher_agent,
            rakesh_jhunjhunwala_agent,
            stanley_druckenmiller_agent,
            warren_buffett_agent,
        ],
    )

    execution = SequentialAgent(
        name="executor_agent", sub_agents=[risk_manager_agent, portfolio_manager_agent]
    )

    pipeline = LoopAgent(
        sub_agents=[
            research,
            investors,
            execution,
        ],
        max_iterations=5,
    )

    pipeline_with_retry = wrap_llm_agents_with_retry(
        pipeline,
        max_429_retries=2,  # single retry for 429; Vertex queues automatically
        base_delay_429=1.0,  # minimal wait (s)
        max_transient_retries=2,  # at most two transient retries (5xx/UNAVAILABLE)
        base_delay_transient=1.0,  # smaller base delay
        backoff=1.5,  # gentler exponential increase
        max_delay=5.0,  # cap backoff at 10s (vs. 32s)
        pt_overage_policy="allow_spillover",  # continue to allow spillover to PayGo
    )

    return pipeline_with_retry


# ---------------------------------------------------------------------
# Example runner
# ---------------------------------------------------------------------
if __name__ == "__main__":
    from src.runner import run_pipeline

    APP_NAME = "compliance_tagging_demo"
    test_gcs_uri = "gs://compliance-poc-videos/M2428051-1080-7830.mp4"

    logger.info("Starting video description test...")
    pipeline = get_pipeline()
    result = run_pipeline(pipeline, APP_NAME, test_gcs_uri)
    logger.success(result)
