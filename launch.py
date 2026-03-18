"""
launch.py — Start the NSDDD v3 document search interface as a standalone web app.

Usage:
    python launch.py

This opens document_metadata_search.ipynb as a clean browser-based GUI
using Voilà (no Jupyter notebook cells visible).
"""

import subprocess
import webbrowser
import threading
import time
import sys

HOST = "localhost"
PORT = 8866
NOTEBOOK = "document_metadata_search.ipynb"
URL = f"http://{HOST}:{PORT}"
BROWSER_DELAY = 3  # seconds to wait for the Voilà server to start before opening the browser


def open_browser():
    time.sleep(BROWSER_DELAY)
    webbrowser.open(URL)


def main():
    print("=" * 60)
    print("  NSDDD v3 — Document Search Interface")
    print("=" * 60)
    print(f"\nStarting search interface...")
    print(f"Opening browser at: {URL}")
    print(f"\nPress Ctrl+C to stop the server.\n")

    threading.Thread(target=open_browser, daemon=True).start()

    try:
        subprocess.run([
            sys.executable, "-m", "voila",
            NOTEBOOK,
            f"--port={PORT}",
            "--no-browser",
            "--Voila.ip=localhost"
        ])
    except FileNotFoundError:
        print("\nError: Voilà is not installed.")
        print("Install it with:  pip install voila")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nServer stopped. Goodbye!")


if __name__ == "__main__":
    main()
