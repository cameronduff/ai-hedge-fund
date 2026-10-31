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
Environment=\"PATH=/home/cd_server/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\"
EnvironmentFile=/home/cd_server/repositories/ai-hedge-fund/.env.local
TimeoutStartSec=7200
ExecStart=/home/cd_server/repositories/ai-hedge-fund/scripts/run_weekly.sh --live
StandardOutput=journal
StandardError=journal
EOF"

echo "Creating systemd timer: $TIMER_FILE (Every Monday at 11:00 UK Time / Europe/London)..."

sudo bash -c "cat << 'EOF' > $TIMER_FILE
[Unit]
Description=Run AI Hedge Fund Weekly (Monday 11:00 UK / Between UK and US market open)

[Timer]
# Runs every Monday at 11:00 UK time (between UK market open at 08:00 and US open at 14:30)
OnCalendar=Mon *-*-* 11:00:00 Europe/London
Persistent=false
Unit=ai-hedge-fund.service

[Install]
WantedBy=timers.target
EOF"

echo "Reloading systemd daemon and enabling timer..."
sudo systemctl daemon-reload
sudo systemctl disable ai-hedge-fund.service 2>/dev/null || true
sudo systemctl stop ai-hedge-fund.timer 2>/dev/null || true
sudo systemctl enable --now ai-hedge-fund.timer

echo "Systemd timer status:"
SYSTEMD_PAGER=cat sudo systemctl status ai-hedge-fund.timer --no-pager
echo ""
echo "Setup complete! Next scheduled run:"
SYSTEMD_PAGER=cat sudo systemctl list-timers ai-hedge-fund.timer --no-pager
echo ""
echo "To trigger a run manually now: sudo systemctl start ai-hedge-fund.service"
echo "To check logs: journalctl -u ai-hedge-fund.service -f"

