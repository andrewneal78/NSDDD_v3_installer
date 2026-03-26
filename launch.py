"""
Launch the Voilà interface for document_metadata_search_voila.ipynb.

Usage:
    python3 launch_voila.py            # blocking (Ctrl+C to stop)
    python3 launch_voila.py --detach   # background, opens browser, exits
"""

import argparse
import os
import signal
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

HOST = '127.0.0.1'
PORT = 8867  # distinct from installer (8866)
URL = f'http://{HOST}:{PORT}'
NOTEBOOK = 'document_metadata_search_voila.ipynb'


def find_python():
    """Return a Python executable that has voila importable."""
    # Prefer the user-level venv
    candidates = [
        Path.home() / '.venv' / 'bin' / 'python3',
        Path(sys.executable),
    ]
    for py in candidates:
        if py.exists():
            r = subprocess.run([str(py), '-c', 'import voila'], capture_output=True)
            if r.returncode == 0:
                return str(py)
    return sys.executable


def stop_existing():
    killed = False
    try:
        result = subprocess.run(['lsof', '-ti', f'tcp:{PORT}'], capture_output=True, text=True)
        for pid_str in result.stdout.split():
            try:
                os.kill(int(pid_str), signal.SIGTERM)
                killed = True
            except (ProcessLookupError, ValueError):
                pass
    except FileNotFoundError:
        pass
    if killed:
        time.sleep(1)


def main():
    parser = argparse.ArgumentParser(description='Launch NSDDD Voilà search interface')
    parser.add_argument('--detach', action='store_true',
                        help='Start in background, open browser, then exit')
    args = parser.parse_args()

    stop_existing()

    py = find_python()
    cwd = Path(__file__).parent

    cmd = [
        py, '-m', 'voila',
        NOTEBOOK,
        f'--port={PORT}',
        f'--Voila.ip={HOST}',
        '--no-browser',
        '--strip_sources=True',
        '--progressive_rendering=True',
    ]

    if args.detach:
        proc = subprocess.Popen(
            cmd, cwd=str(cwd),
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f'Starting NSDDD search interface... (PID {proc.pid})')
        time.sleep(3)
        webbrowser.open(URL)
        sys.exit(0)
    else:
        print(f'NSDDD Search Interface')
        print(f'  URL : {URL}')
        print(f'  Stop: Ctrl+C')
        print()
        try:
            subprocess.run(cmd, cwd=str(cwd))
        except KeyboardInterrupt:
            print('\nServer stopped.')


if __name__ == '__main__':
    main()
