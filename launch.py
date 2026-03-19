"""
NSDDD v3 — Launch Script

Starts the Voilà server for the document_metadata_search notebook.

Usage:
    python launch.py            # blocking mode (Ctrl+C to stop)
    python launch.py --detach   # background mode (terminal closes, browser opens)
"""

import argparse
import json
import os
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

HOST = '127.0.0.1'
PORT = 8866
URL = f'http://{HOST}:{PORT}'
NOTEBOOK = 'document_metadata_search_voila.ipynb'


def find_voila():
    """
    Return True if voila is importable via the current Python interpreter.
    Falls back to checking the PATH as well.
    """
    import shutil
    # Prefer module invocation (works inside any venv)
    try:
        import voila  # noqa: F401
        return True
    except ImportError:
        pass
    return shutil.which('voila') is not None


def stop_existing():
    """Kill any process already listening on PORT so launches don't stack up."""
    import signal
    killed = False
    try:
        result = subprocess.run(
            ['lsof', '-ti', f'tcp:{PORT}'],
            capture_output=True, text=True,
        )
        for pid_str in result.stdout.split():
            try:
                os.kill(int(pid_str), signal.SIGTERM)
                killed = True
            except (ProcessLookupError, ValueError):
                pass
    except FileNotFoundError:
        pass  # lsof not available (Windows); skip
    if killed:
        time.sleep(1)  # give the process a moment to exit


def build_voila_command() -> list:
    return [
        sys.executable, '-m', 'voila',
        NOTEBOOK,
        f'--port={PORT}',
        f'--Voila.ip={HOST}',
        '--no-browser',
        '--strip_sources=True',
        '--progressive_rendering=True',
    ]


def main():
    parser = argparse.ArgumentParser(description='Launch NSDDD v3 search interface')
    parser.add_argument(
        '--detach',
        action='store_true',
        help='Start Voilà in background, open browser, then exit',
    )
    args = parser.parse_args()

    stop_existing()

    if not find_voila():
        print('Error: voila not found. Run install.py first, or:')
        print(f'  {sys.executable} -m pip install voila')
        sys.exit(1)

    cwd = Path(__file__).parent
    cmd = build_voila_command()

    if args.detach:
        # Start Voilà detached — no console window, keep running after this script exits
        proc = subprocess.Popen(
            cmd,
            cwd=str(cwd),
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f'Starting NSDDD v3... (PID {proc.pid})')
        time.sleep(3)
        webbrowser.open(URL)
        sys.exit(0)
    else:
        # Blocking mode — Ctrl+C to stop
        print(f'NSDDD v3 Search Interface')
        print(f'  URL : {URL}')
        print(f'  Stop: Ctrl+C')
        print()
        try:
            proc = subprocess.run(cmd, cwd=str(cwd))
        except KeyboardInterrupt:
            print('\nServer stopped.')


if __name__ == '__main__':
    main()
