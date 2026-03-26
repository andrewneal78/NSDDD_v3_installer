"""
NSDDD v3 Installer launcher.

- Starts the Voilà interface.
- Checks for updates at startup.
  - Git installs: uses `git fetch` + `git pull --ff-only`.
  - Download/ZIP installs: compares local VERSION with remote VERSION,
    then downloads and overlays the latest repo zip while preserving user data.
"""

import argparse
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import urllib.request
import zipfile
from pathlib import Path

HOST = "127.0.0.1"
PORT = 8867
URL = f"http://{HOST}:{PORT}"
NOTEBOOK = "document_metadata_search_voila.ipynb"

REPO_OWNER = "andrewneal78"
REPO_NAME = "NSDDD_v3_installer"
DEFAULT_BRANCH = "main"

RAW_VERSION_URL = (
    f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{DEFAULT_BRANCH}/VERSION"
)
ZIP_URL = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/archive/refs/heads/{DEFAULT_BRANCH}.zip"

# Set NSDDD_AUTO_UPDATE=0 to disable automatic update application.
AUTO_UPDATE_ENABLED = os.environ.get("NSDDD_AUTO_UPDATE", "1") != "0"
HTTP_TIMEOUT_SECONDS = 8

# Preserve local data/environments when overlaying ZIP updates.
PRESERVE_TOP_LEVEL = {
    ".git",
    ".venv",
    "NSDDD_v3_workspace",
    "outputs",
    "__pycache__",
    ".ipynb_checkpoints",
}


def find_python():
    """Return a Python executable that has voila importable."""
    candidates = [
        Path.home() / ".venv" / "bin" / "python3",
        Path(sys.executable),
    ]
    for py in candidates:
        if py.exists():
            r = subprocess.run([str(py), "-c", "import voila"], capture_output=True)
            if r.returncode == 0:
                return str(py)
    return sys.executable


def stop_existing():
    """Terminate any process already bound to the launch port."""
    killed = False
    try:
        result = subprocess.run(["lsof", "-ti", f"tcp:{PORT}"], capture_output=True, text=True)
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


def fetch_text(url: str) -> str | None:
    try:
        with urllib.request.urlopen(url, timeout=HTTP_TIMEOUT_SECONDS) as resp:
            return resp.read().decode("utf-8").strip()
    except Exception:
        return None


def local_version(cwd: Path) -> str:
    vf = cwd / "VERSION"
    if not vf.exists():
        return ""
    return vf.read_text(encoding="utf-8").strip()


def write_local_version(cwd: Path, version: str):
    (cwd / "VERSION").write_text(version.strip() + "\n", encoding="utf-8")


def is_git_install(cwd: Path) -> bool:
    return (cwd / ".git").exists()


def git_rev(cwd: Path, ref: str) -> str:
    r = subprocess.run(
        ["git", "-C", str(cwd), "rev-parse", ref],
        capture_output=True,
        text=True,
    )
    return r.stdout.strip() if r.returncode == 0 else ""


def check_git_update(cwd: Path) -> tuple[bool, str, str]:
    fetch = subprocess.run(
        ["git", "-C", str(cwd), "fetch", "origin", DEFAULT_BRANCH],
        capture_output=True,
        text=True,
    )
    if fetch.returncode != 0:
        return False, "", ""

    local = git_rev(cwd, "HEAD")
    remote = git_rev(cwd, f"origin/{DEFAULT_BRANCH}")
    if not local or not remote:
        return False, local, remote
    return local != remote, local, remote


def apply_git_update(cwd: Path) -> bool:
    pull = subprocess.run(
        ["git", "-C", str(cwd), "pull", "--ff-only", "origin", DEFAULT_BRANCH],
        capture_output=True,
        text=True,
    )
    if pull.returncode == 0:
        print("✓ Git update applied.")
        return True

    print("⚠️  Git update failed:")
    if pull.stderr.strip():
        print(pull.stderr.strip())
    return False


def check_zip_update(cwd: Path) -> tuple[bool, str, str]:
    local = local_version(cwd)
    remote = fetch_text(RAW_VERSION_URL) or ""
    if not remote:
        return False, local, remote
    return remote != local, local, remote


def remove_path(path: Path):
    if not path.exists():
        return
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()


def overlay_tree(src: Path, dst: Path):
    for item in src.iterdir():
        if item.name in PRESERVE_TOP_LEVEL:
            continue
        target = dst / item.name
        if item.is_dir():
            if target.exists() and not target.is_dir():
                remove_path(target)
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


def apply_zip_update(cwd: Path, remote_version: str) -> bool:
    try:
        with tempfile.TemporaryDirectory(prefix="nsddd_update_") as td:
            tmp = Path(td)
            zip_path = tmp / "update.zip"

            with urllib.request.urlopen(ZIP_URL, timeout=HTTP_TIMEOUT_SECONDS) as resp:
                zip_path.write_bytes(resp.read())

            extract_dir = tmp / "extract"
            extract_dir.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(extract_dir)

            roots = [p for p in extract_dir.iterdir() if p.is_dir()]
            if not roots:
                print("⚠️  Update failed: could not find extracted root directory.")
                return False

            overlay_tree(roots[0], cwd)
            if remote_version:
                write_local_version(cwd, remote_version)

        print("✓ Download-install update applied.")
        return True
    except Exception as e:
        print(f"⚠️  Download-install update failed: {e}")
        return False


def maybe_update(cwd: Path, no_update: bool) -> bool:
    """Check/apply updates. Returns True when files were updated."""
    if no_update:
        return False

    if is_git_install(cwd):
        available, local, remote = check_git_update(cwd)
        if not available:
            return False
        print(f"🔄 Update available (git): {local[:7]} -> {remote[:7]}")
        if AUTO_UPDATE_ENABLED:
            return apply_git_update(cwd)
        print("ℹ️  Auto-update disabled (NSDDD_AUTO_UPDATE=0).")
        return False

    available, local, remote = check_zip_update(cwd)
    if not available:
        return False

    local_label = local or "(none)"
    print(f"🔄 Update available (download install): {local_label} -> {remote}")
    if AUTO_UPDATE_ENABLED:
        return apply_zip_update(cwd, remote)
    print("ℹ️  Auto-update disabled (NSDDD_AUTO_UPDATE=0).")
    return False


def restart_self():
    print("↻ Restarting launcher to use updated files...")
    os.execv(sys.executable, [sys.executable, str(Path(__file__))] + sys.argv[1:])


def build_voila_command(py: str) -> list[str]:
    return [
        py,
        "-m",
        "voila",
        NOTEBOOK,
        f"--port={PORT}",
        f"--Voila.ip={HOST}",
        "--no-browser",
        "--strip_sources=True",
        "--progressive_rendering=True",
    ]


def main():
    parser = argparse.ArgumentParser(description="Launch NSDDD search interface")
    parser.add_argument("--detach", action="store_true", help="Start in background, open browser, then exit")
    parser.add_argument("--no-update", action="store_true", help="Skip update check on this run")
    args = parser.parse_args()

    cwd = Path(__file__).parent

    if maybe_update(cwd, args.no_update):
        restart_self()

    stop_existing()

    py = find_python()
    cmd = build_voila_command(py)

    if args.detach:
        proc = subprocess.Popen(
            cmd,
            cwd=str(cwd),
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"Starting NSDDD search interface... (PID {proc.pid})")
        time.sleep(3)
        import webbrowser

        webbrowser.open(URL)
        sys.exit(0)

    print("NSDDD Search Interface")
    print(f"  URL : {URL}")
    print("  Stop: Ctrl+C")
    print("  Note: browser may show 'server not found' for a few seconds.")
    print("  Please be patient and refresh once the server is ready.")
    print()

    try:
        subprocess.run(cmd, cwd=str(cwd))
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    main()
