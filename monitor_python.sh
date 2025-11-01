#!/bin/bash
export PATH=$PATH:/usr/bin:/bin
VENV_PATH="myenv"
# sudo ./monitor_python.sh > cron.log
PROGRAM="display.py"

LOG_FILE="program.log"

source "/home/adeeb/EInkDisplay/$VENV_PATH/bin/activate"

if ! pgrep -f "$PROGRAM" > /dev/null; then
    echo "[$(date)] Program is not running. Restarting..."
    python3 -u /home/adeeb/EInkDisplay/display.py > $LOG_FILE 2>&1 & 
else
    echo "[$(date)] Program is running."
fi
