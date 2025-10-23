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
from src.agents.growth_agent.agent import growth_agent
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
    """
    Constructs the AI Hedge Fund pipeline using Google ADK.

    The pipeline is structured as a loop to allow for iterative refinement
    of analysis until a final decision is made.

    The pipeline is structured as follows:
    1.  A parallel research agent gathers insights on a stock from multiple perspectives.
    2.  A parallel investors agent simulates getting opinions from a team of world-class investors.
    3.  A sequential execution agent that first assesses risk and then makes a portfolio decision.
    4.  These agents are placed in a LoopAgent to iterate until the portfolio manager
        is confident enough to make a decision and exit the loop.
    """

    research = ParallelAgent(
        name="research_agent",
        sub_agents=[
            fundamentals_agent,
            growth_agent,
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
        max_iterations=5,  # The portfolio_manager's exit tool will be the primary exit condition
    )

    pipeline_with_retry = wrap_llm_agents_with_retry(
        pipeline,
        max_429_retries=10,  # single retry for 429; Vertex queues automatically
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
    from src.clients.Trading212 import get_agent
    from src.utils.context_builder import build_account_context, build_pies_context

    # Optional: focus on a specific pie
    PIE_ID = 5855432  # set to None to include all pies

    APP_NAME = "ai_hedge_fund"  # change if you have a specific ADK app name

    logger.info("Building Trading 212 context...")
    agent = get_agent()

    # 1) Build the two context JSONs
    account_ctx = build_account_context(agent, top_n_positions=60)
    pies_ctx = build_pies_context(agent, include_plans=True)

    # Optionally filter to just one pie (and its plan)
    if PIE_ID is not None:
        pies_list = pies_ctx.get("pies", [])
        pies_ctx["pies"] = [p for p in pies_list if p.get("id") == PIE_ID]
        plans = pies_ctx.get("rebalance_plans", {})
        # keep only the focused pie’s plan if present
        key_str = str(PIE_ID)
        pies_ctx["rebalance_plans"] = (
            {key_str: plans.get(key_str) or plans.get(PIE_ID)}
            if plans and (plans.get(key_str) or plans.get(PIE_ID))
            else {}
        )

    # 2) Author the task envelope (what you want the pipeline to do)
    task_text = (
        "Using my Trading 212 account context and pies, identify 3 dividend stocks to add. "
        "Propose target weights per pie (weights sum to 1.0 per pie) and produce market orders "
        "to move toward the targets while respecting risk. Prefer instruments available on Trading 212 "
        "(LSE or US)."
    )

    task_cfg = {
        "min_dividend_yield": 0.02,
        "risk_budget": "moderate",
        "max_positions_per_pie": 25,
        "execution": {
            "order_type": "MARKET",
            "env": account_ctx.get("account", {}).get("env", "demo"),
        },
        "fx": "account_currency",
        "focus_pie_id": PIE_ID,
    }

    task_envelope = {
        "schema_version": "1.0",
        "task": task_text,
        "constraints": task_cfg,
        "output_contract": {
            "recommendations": [
                {
                    "ticker": "string",
                    "exchange": "string",
                    "weight": 0.10,
                    "reason": "string",
                }
            ],
            "actions": [
                {"type": "BUY|SELL", "ticker": "string", "qty": 0.0, "why": "string"}
            ],
            "notes": "string",
        },
        "instructions": [
            "Use t212_account and t212_pies JSON as the single source of portfolio truth.",
            "If recommending new assets, include ticker, exchange, rationale, and target weight (0..1).",
            "Return ONLY a single JSON object that matches output_contract.",
        ],
    }

    # 3) Build a single query string with three JSON blocks
    query = (
        "BEGIN_JSON t212_account\n"
        + json.dumps(account_ctx, separators=(",", ":"), ensure_ascii=False)
        + "\nEND_JSON t212_account\n\n"
        "BEGIN_JSON t212_pies\n"
        + json.dumps(pies_ctx, separators=(",", ":"), ensure_ascii=False)
        + "\nEND_JSON t212_pies\n\n"
        "BEGIN_JSON task\n"
        + json.dumps(task_envelope, separators=(",", ":"), ensure_ascii=False)
        + "\nEND_JSON task"
    )

    logger.info("Starting pipeline...")
    pipeline = get_pipeline()
    result = run_pipeline(pipeline, APP_NAME, query)
    logger.success(result)
