#!/bin/bash
cd "$(dirname "$0")"

# Kill any existing instance on this port
lsof -ti tcp:8867 | xargs kill -TERM 2>/dev/null
sleep 1

echo "================================================"
echo "  NSDDD Search Interface"
echo "  http://127.0.0.1:8867"
echo "  Close this window to stop the server."
echo "================================================"
echo ""

# Open browser after 3 seconds (background)
(sleep 3 && open "http://127.0.0.1:8867") &

# Run Voilà in foreground — closing this window stops the server
~/.venv/bin/python3 -m voila document_metadata_search_voila.ipynb \
    --port=8867 \
    --Voila.ip=127.0.0.1 \
    --no-browser \
    --strip_sources=True \
    --progressive_rendering=True
