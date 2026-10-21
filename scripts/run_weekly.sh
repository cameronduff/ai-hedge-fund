#!/bin/bash
set -euo pipefail

# Ensure standard user binary paths (e.g. uv) are present in PATH for non-interactive shells and systemd
export PATH="/home/cd_server/.local/bin:$HOME/.local/bin:$PATH"

# Directory of this repository
REPO_DIR="/home/cd_server/repositories/ai-hedge-fund"
cd "$REPO_DIR"

# Source environment variables if present
if [ -f "$REPO_DIR/.env.local" ]; then
    set -a
    source "$REPO_DIR/.env.local"
    set +a
fi

# Logs directory
LOGS_DIR="$REPO_DIR/logs"
mkdir -p "$LOGS_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOGS_DIR/run_$TIMESTAMP.log"

echo "==========================================================" | tee -a "$LOG_FILE"
echo "AI Hedge Fund Weekly Run — Started at $(date)" | tee -a "$LOG_FILE"
echo "==========================================================" | tee -a "$LOG_FILE"

# Run production runner (defaults to --live unless --dry-run passed)
MODE_FLAG="${1:---live}"

PYTHONUNBUFFERED=1 uv run python -m app.production_runner "$MODE_FLAG" 2>&1 | tee -a "$LOG_FILE"



echo "==========================================================" | tee -a "$LOG_FILE"
echo "AI Hedge Fund Weekly Run — Finished at $(date)" | tee -a "$LOG_FILE"
echo "Log saved to: $LOG_FILE" | tee -a "$LOG_FILE"
echo "==========================================================" | tee -a "$LOG_FILE"
