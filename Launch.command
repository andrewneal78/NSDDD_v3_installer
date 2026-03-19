#!/bin/bash
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

# Kill any existing instance on this port
lsof -ti tcp:8866 | xargs kill -TERM 2>/dev/null
sleep 1

echo "================================================"
echo "  NSDDD v3 Search Interface"
echo "  http://127.0.0.1:8866"
echo "  Close this window to stop the server."
echo "================================================"
echo ""

# Open browser after 3 seconds (background)
(sleep 3 && open "http://127.0.0.1:8866") &

# Run Voilà in foreground — closing this window stops the server
"$PYTHON" -m voila document_metadata_search_voila.ipynb \
    --port=8866 \
    --Voila.ip=127.0.0.1 \
    --no-browser \
    --strip_sources=True \
    --progressive_rendering=True
