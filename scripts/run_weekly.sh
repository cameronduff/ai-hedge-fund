#!/bin/bash
set -euo pipefail

# Directory of this repository
REPO_DIR="/home/cd_server/repositories/ai-hedge-fund"
cd "$REPO_DIR"

# Logs directory
LOGS_DIR="$REPO_DIR/logs"
mkdir -p "$LOGS_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOGS_DIR/run_$TIMESTAMP.log"

echo "==========================================================" | tee -a "$LOG_FILE"
echo "AI Hedge Fund Weekly Run — Started at $(date)" | tee -a "$LOG_FILE"
echo "==========================================================" | tee -a "$LOG_FILE"

# Run production runner (defaults to dry-run unless --live passed)
# To run in live mode, pass --live to this script
MODE_FLAG="${1:---dry-run}"

uv run python -m app.production_runner "$MODE_FLAG" 2>&1 | tee -a "$LOG_FILE"

echo "==========================================================" | tee -a "$LOG_FILE"
echo "AI Hedge Fund Weekly Run — Finished at $(date)" | tee -a "$LOG_FILE"
echo "Log saved to: $LOG_FILE" | tee -a "$LOG_FILE"
echo "==========================================================" | tee -a "$LOG_FILE"
