#!/bin/bash
set -euo pipefail

SERVICE_FILE="/etc/systemd/system/ai-hedge-fund.service"
TIMER_FILE="/etc/systemd/system/ai-hedge-fund.timer"

echo "Creating systemd service: $SERVICE_FILE..."

sudo bash -c "cat << 'EOF' > $SERVICE_FILE
[Unit]
Description=AI Hedge Fund Weekly Run
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
User=cd_server
WorkingDirectory=/home/cd_server/repositories/ai-hedge-fund
EnvironmentFile=/home/cd_server/repositories/ai-hedge-fund/.env.local
ExecStart=/home/cd_server/repositories/ai-hedge-fund/scripts/run_weekly.sh --live
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF"

echo "Creating systemd timer: $TIMER_FILE (Every Monday at 15:00 UK Time / Europe/London)..."

sudo bash -c "cat << 'EOF' > $TIMER_FILE
[Unit]
Description=Run AI Hedge Fund Weekly (Monday 15:00 UK / Transatlantic Overlap)
Requires=ai-hedge-fund.service

[Timer]
# Runs every Monday at 15:00 UK time (30 min after US market open with EU/UK overlap)
OnCalendar=Mon *-*-* 15:00:00 Europe/London
Persistent=true

[Install]
WantedBy=timers.target
EOF"

echo "Reloading systemd daemon and enabling timer..."
sudo systemctl daemon-reload
sudo systemctl enable --now ai-hedge-fund.timer

echo "Systemd timer status:"
sudo systemctl status ai-hedge-fund.timer --no-pager
echo ""
echo "Setup complete! To trigger a run manually now: sudo systemctl start ai-hedge-fund.service"
echo "To check logs: journalctl -u ai-hedge-fund.service -f"
