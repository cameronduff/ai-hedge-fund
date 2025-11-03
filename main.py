"""
Main execution script for the AI Hedge Fund pipeline.
Runs the complete analysis pipeline and saves results to output directory.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from loguru import logger

from src.pipeline import get_pipeline
from src.runner import run_pipeline
from src.clients.Trading212 import get_agent
from src.utils.context_builder import build_account_context, build_pies_context


def ensure_output_dir() -> Path:
    """Create output directory if it doesn't exist."""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    return output_dir


def save_results(
    result: dict, output_dir: Path, prefix: str = "pipeline_result"
) -> Path:
    """
    Save pipeline results to a JSON file with timestamp.

    Args:
        result: The pipeline output dictionary
        output_dir: Directory to save the output
        prefix: Filename prefix

    Returns:
        Path to the saved file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.json"
    filepath = output_dir / filename

    with open(filepath, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    logger.info(f"Results saved to: {filepath}")
    return filepath


def main():
    """Main execution function."""
    # Configuration
    PIE_ID = 5855432  # set to None to include all pies
    APP_NAME = "ai_hedge_fund"

    # Ensure output directory exists
    output_dir = ensure_output_dir()

    logger.info("=" * 60)
    logger.info("AI Hedge Fund Pipeline Starting")
    logger.info("=" * 60)

    # Build Trading 212 context
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
        # keep only the focused pie's plan if present
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

    # Run the pipeline
    logger.info("Starting AI Hedge Fund pipeline...")
    pipeline = get_pipeline()

    try:
        result = run_pipeline(pipeline, APP_NAME, query)

        # Save results
        output_file = save_results(result, output_dir)

        logger.success("=" * 60)
        logger.success("Pipeline completed successfully!")
        logger.success(f"Results saved to: {output_file}")
        logger.success("=" * 60)

        # Print summary
        if result.get("output"):
            output = result["output"]

            if "recommendations" in output:
                logger.info(
                    f"\nRecommendations: {len(output['recommendations'])} stocks"
                )
                for rec in output["recommendations"]:
                    logger.info(
                        f"  - {rec.get('ticker', 'N/A')}: {rec.get('reason', 'N/A')[:100]}"
                    )

            if "actions" in output:
                logger.info(f"\nActions: {len(output['actions'])} trades")
                for action in output["actions"]:
                    logger.info(
                        f"  - {action.get('type', 'N/A')} {action.get('ticker', 'N/A')}: {action.get('qty', 0)}"
                    )

        return result

    except Exception as e:
        logger.error(f"Pipeline failed with error: {e}")

        # Save error information
        error_result = {
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "task": task_text,
        }
        error_file = save_results(error_result, output_dir, prefix="pipeline_error")
        logger.error(f"Error details saved to: {error_file}")
        raise


if __name__ == "__main__":
    main()
