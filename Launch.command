#!/bin/bash
# NSDDD v3 — Mac launcher
# Double-click this file to start the search interface.
# The terminal window will close automatically once the browser opens.
#
# One-time setup: chmod +x Launch.command
cd "$(dirname "$0")"

# Resolve Python: prefer install_config.json, then local .venv, then system python3
if [ -f "install_config.json" ]; then
    PYTHON=$(python3 -c "import json; print(json.load(open('install_config.json')).get('python',''))" 2>/dev/null)
fi
if [ -z "$PYTHON" ] || [ ! -f "$PYTHON" ]; then
    if [ -f ".venv/bin/python3" ]; then
        PYTHON=".venv/bin/python3"
    elif [ -f "$HOME/.venv/bin/python3" ]; then
        PYTHON="$HOME/.venv/bin/python3"
    else
        PYTHON="python3"
    fi
fi

"$PYTHON" launch.py --detach
