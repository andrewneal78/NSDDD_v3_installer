"""
NSDDD v3 — Interactive Installer

Run this script once to download and install the dataset:
    python3 install.py

Then double-click Launch.command (Mac) or Launch.vbs (Windows) to start.
"""

import json
import os
import platform
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Ensure we can import utils and config from the repo root
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent
sys.path.insert(0, str(REPO_ROOT))

from config import (
    DATASHARE_API_BASE,
    DATASHARE_HANDLE,
    DOWNLOADS,
    DEFAULT_INSTALL_DIR,
    DISK_SPACE_REQUIRED_MIN_GB,
    RAM_REQUIRED_GB,
    PYTHON_VERSION_MIN,
    DATASET_NAME,
)
from utils.datashare import DataShareClient
from utils.download import download_file, check_disk_space, calculate_total_size
from utils.extract import extract_with_progress
from utils.setup import create_directory_structure, validate_installation_directory
from utils.verify import verify_directory


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _separator():
    print('=' * 60)


def _header(title: str):
    _separator()
    print(f'  {title}')
    _separator()


def _check_python() -> bool:
    v = sys.version_info
    ok = (v.major, v.minor) >= PYTHON_VERSION_MIN
    status = '✓' if ok else '✗'
    print(f'  {status} Python {v.major}.{v.minor}', end='')
    if not ok:
        min_v = '.'.join(str(x) for x in PYTHON_VERSION_MIN)
        print(f' (requires {min_v}+)')
    else:
        print()
    return ok


def _check_disk(path: str) -> tuple:
    ok, available_gb, required_gb = check_disk_space(path, DISK_SPACE_REQUIRED_MIN_GB)
    status = '✓' if ok else '✗'
    print(f'  {status} Disk: {available_gb:.0f} GB available ({required_gb} GB required)')
    return ok, available_gb


def _check_ram() -> int:
    """Return detected RAM in GB (0 if unknown)."""
    try:
        import psutil
        ram_gb = psutil.virtual_memory().total / (1024 ** 3)
    except Exception:
        ram_gb = 0
    status = '✓' if ram_gb >= RAM_REQUIRED_GB or ram_gb == 0 else '⚠'
    if ram_gb > 0:
        print(f'  {status} RAM: {ram_gb:.0f} GB detected')
        if ram_gb < RAM_REQUIRED_GB:
            print(f'    (recommended {RAM_REQUIRED_GB} GB for loading model; may be slow)')
    else:
        print(f'  ? RAM: could not detect (psutil not installed)')
    return int(ram_gb)


def _prompt_install_dir() -> Path:
    default = REPO_ROOT / DEFAULT_INSTALL_DIR
    print()
    raw = input(f'Install directory [{default}]: ').strip()
    chosen = Path(raw) if raw else default
    return chosen



def _python_exe(venv_dir: Path) -> Path:
    """Return the Python executable path for a given venv directory."""
    if platform.system() == 'Windows':
        return venv_dir / 'Scripts' / 'python.exe'
    return venv_dir / 'bin' / 'python3'


def _find_existing_venvs() -> list:
    """
    Return list of (label, python_path) tuples for venvs that exist and have voila.
    Checks: currently active venv, common locations relative to repo and home.
    """
    found = []
    seen = set()

    candidates = []

    # Currently active venv (VIRTUAL_ENV env var)
    active = os.environ.get('VIRTUAL_ENV')
    if active:
        candidates.append(('Currently active venv', Path(active)))

    # Common locations
    candidates += [
        ('Repo .venv',  REPO_ROOT / '.venv'),
        ('Repo venv',   REPO_ROOT / 'venv'),
        ('~/.venv',     Path.home() / '.venv'),
        ('~/venv',      Path.home() / 'venv'),
    ]

    for label, venv_dir in candidates:
        py = _python_exe(venv_dir)
        key = str(py.resolve()) if py.exists() else str(py)
        if not py.exists() or key in seen:
            continue
        seen.add(key)
        # Check voila is importable
        result = subprocess.run(
            [str(py), '-c', 'import voila'],
            capture_output=True,
        )
        has_voila = result.returncode == 0
        found.append((label, py, has_voila))

    return found


def _prompt_venv() -> Path:
    """
    Prompt the user to choose an existing venv or create a new one.
    Returns the Python executable path to use.
    """
    existing = _find_existing_venvs()
    new_venv_dir = REPO_ROOT / '.venv'

    print()
    print('Python environment:')
    print()
    print('  The installer will set up a virtual environment — a self-contained')
    print('  folder that holds all the Python packages this tool needs. It has no')
    print('  effect on the rest of your system: nothing is changed globally, and')
    print('  you can remove it at any time by deleting the installer folder.')
    print()

    options = []
    for label, py, has_voila in existing:
        voila_tag = '✓ voila' if has_voila else '  no voila'
        print(f'  [{len(options) + 1}] Use {label} ({voila_tag})')
        print(f'      {py}')
        options.append(('existing', py))

    new_idx = len(options) + 1
    print(f'  [{new_idx}] Create new .venv inside installer directory')

    while True:
        raw = input(f'Choose [1-{new_idx}] (default {new_idx}): ').strip()
        if not raw:
            choice = new_idx
        elif raw.isdigit() and 1 <= int(raw) <= new_idx:
            choice = int(raw)
        else:
            print(f'  Please enter a number between 1 and {new_idx}.')
            continue
        break

    if choice == new_idx:
        return None  # Caller will create new venv
    else:
        _, py, _ = existing[choice - 1]
        return py


def _install_dependencies() -> Path:
    """
    Set up the Python environment and install dependencies.
    Returns the Python executable path used.
    """
    req_file = REPO_ROOT / 'requirements.txt'

    chosen_py = _prompt_venv()

    if chosen_py is None:
        # Create a new .venv
        venv_dir = REPO_ROOT / '.venv'
        venv_py = _python_exe(venv_dir)
        if not venv_py.exists():
            print('  Creating virtual environment (.venv)...')
            result = subprocess.run(
                [sys.executable, '-m', 'venv', str(venv_dir)],
                capture_output=True, text=True,
            )
            if result.returncode != 0:
                print('  ⚠ Could not create venv:')
                for line in result.stderr.splitlines()[-5:]:
                    print(f'    {line}')
                return sys.executable
            print('  ✓ Virtual environment created')
        else:
            print('  ✓ .venv already exists')
    else:
        venv_py = chosen_py
        print(f'  ✓ Using {venv_py}')

    # Install requirements
    if req_file.exists():
        print('  Installing Python dependencies...')
        result = subprocess.run(
            [str(venv_py), '-m', 'pip', 'install', '-r', str(req_file)],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            print('  ⚠ pip install reported errors:')
            for line in result.stderr.splitlines()[-5:]:
                print(f'    {line}')
        else:
            print('  ✓ Dependencies installed')
    else:
        print('  ⚠ requirements.txt not found — skipping')

    # Install voila
    result = subprocess.run(
        [str(venv_py), '-c', 'import voila'],
        capture_output=True,
    )
    if result.returncode != 0:
        print('  Installing voila...')
        result = subprocess.run(
            [str(venv_py), '-m', 'pip', 'install', 'voila'],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            print('  ✓ voila installed')
        else:
            print('  ⚠ voila install failed — install manually: pip install voila')
    else:
        print('  ✓ voila already installed')

    return venv_py


def _make_launcher_executable():
    launcher = REPO_ROOT / 'Launch.command'
    if launcher.exists() and platform.system() == 'Darwin':
        try:
            launcher.chmod(launcher.stat().st_mode | 0o111)
        except Exception:
            pass


def _is_already_extracted(spec: dict, install_dir: Path) -> bool:
    """Return True if this download's files are already present in any known workspace."""
    filename = spec['filename']
    subdir = spec['extract_to'].rstrip('/')

    # Candidate locations: chosen install dir + repo-local workspace
    candidates = [
        install_dir / subdir,
        REPO_ROOT / DEFAULT_INSTALL_DIR / subdir,
    ]

    for extract_to in candidates:
        if filename.endswith('.zip'):
            if extract_to.is_dir() and any(f.is_file() for f in extract_to.rglob('*')):
                return True
        else:
            if (extract_to / filename).exists():
                return True

    return False


def _download_encoder(install_dir: Path, venv_py: Path):
    """Download the sentence encoder model from HuggingFace into the workspace."""
    model_dir = install_dir / 'model' / 'all-mpnet-base-v2'

    if model_dir.exists() and any(model_dir.iterdir()):
        print('  ✓ Encoder already present — skipping')
        return

    print('  Downloading sentence encoder (all-mpnet-base-v2, ~420 MB)...', flush=True)
    result = subprocess.run(
        [str(venv_py), '-c',
         f'from sentence_transformers import SentenceTransformer; '
         f'm = SentenceTransformer("sentence-transformers/all-mpnet-base-v2"); '
         f'm.save(r"{model_dir}")'],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        print('  ✓ Encoder downloaded')
    else:
        print('  ⚠ Encoder download failed — semantic search will download it on first use')


def _write_install_config(install_path: Path, python_path: Path):
    config = {
        'install_path': str(install_path),
        'installer_root': str(REPO_ROOT),
        'python': str(python_path),
    }
    config_path = REPO_ROOT / 'install_config.json'
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)


def _cleanup_stale_archives(downloads_dir: Path):
    """
    Remove leftover ZIP archives from downloads directory.

    Extraction already removes ZIP files on success, but older installer runs
    may have left archives behind. This pass keeps workspace size predictable.
    """
    if not downloads_dir.exists():
        return

    removed = []
    for spec in DOWNLOADS.values():
        filename = spec.get('filename', '')
        if not filename.endswith('.zip'):
            continue
        archive = downloads_dir / filename
        if archive.exists():
            try:
                archive.unlink()
                removed.append(filename)
            except Exception:
                pass

    if removed:
        print('  ✓ Cleaned leftover archives from downloads/:')
        for name in removed:
            print(f'    - {name}')


# ---------------------------------------------------------------------------
# Main installer flow
# ---------------------------------------------------------------------------

def main():
    _header(f'NSDDD v3 — Installer')
    print()
    print('Checking system requirements...')

    py_ok = _check_python()
    if not py_ok:
        print()
        print('Python version too old. Please upgrade Python and try again.')
        sys.exit(1)

    # Determine install dir before disk check (need path to check disk)
    install_dir = _prompt_install_dir()

    disk_ok, available_gb = _check_disk(str(install_dir))
    _check_ram()

    if not disk_ok:
        print()
        print(f'Insufficient disk space at {install_dir}.')
        print(f'Free up space and try again.')
        sys.exit(1)

    # Compute all downloads: required files only
    required_keys = [k for k, v in DOWNLOADS.items() if v.get('required')]
    all_selected = required_keys

    # Exclude already-installed files from size calculation
    install_dir.mkdir(parents=True, exist_ok=True)
    to_download = [k for k in all_selected if not _is_already_extracted(DOWNLOADS[k], install_dir)]
    size_info = calculate_total_size(DOWNLOADS, to_download)
    total_gb = size_info['total_gb']

    print()
    if to_download:
        print(f'Downloading required files ({total_gb:.1f} GB)...')
    else:
        print('All files already installed — skipping downloads.')

    # Initialise DataShare client
    client = DataShareClient(DATASHARE_API_BASE, DATASHARE_HANDLE)

    # Create directory structure
    dirs = create_directory_structure(str(install_dir))
    downloads_dir = dirs['downloads']

    # Download each selected file
    for key in all_selected:
        spec = DOWNLOADS[key]
        filename = spec['filename']
        size_mb = spec['size_mb']

        # Skip if already extracted
        if _is_already_extracted(spec, install_dir):
            extract_to = install_dir / spec['extract_to'].rstrip('/')
            print(f'  ✓ {filename:<45} already installed — skipping')
            continue

        # Get download URL from DataShare
        try:
            file_info = client.get_file_info(filename)
            url = file_info['download_url']
            expected_bytes = file_info['size_bytes']
        except Exception as e:
            print(f'  ✗ Could not resolve {filename}: {e}')
            continue

        dest = downloads_dir / filename
        size_str = (
            f'{size_mb / 1024:.1f} GB' if size_mb >= 1024
            else f'{size_mb:.0f} MB'
        )
        print(f'  {filename:<45} {size_str:>8}', end='  ', flush=True)

        try:
            download_file(
                url=url,
                destination=str(dest),
                expected_size=expected_bytes,
                progress_callback=_progress_bar,
            )
            print(' ✓')
        except Exception as e:
            print(f'\n  ✗ Download failed: {e}')
            continue

        # Extract
        extract_to = install_dir / spec['extract_to'].rstrip('/')
        if filename.endswith('.zip'):
            print(f'    Extracting...', end='  ', flush=True)
            try:
                extract_with_progress(dest, extract_to, verbose=False)
                print('✓')
                # Remove zip to save space
                dest.unlink(missing_ok=True)
            except Exception as e:
                print(f'\n  ✗ Extraction failed: {e}')
        else:
            # Plain file — just move to destination
            extract_to.mkdir(parents=True, exist_ok=True)
            import shutil as _shutil
            _shutil.move(str(dest), str(extract_to / filename))

    print()
    print('Installing dependencies...')
    venv_py = _install_dependencies()

    print()
    print('Downloading encoder model...')
    _download_encoder(install_dir, venv_py)

    print()
    print('Verifying installation...')
    validation = validate_installation_directory(str(install_dir))
    if validation['valid']:
        print('  ✓ Installation verified')
    else:
        if validation['missing']:
            print('  ⚠ Some files are missing:')
            for m in validation['missing']:
                print(f'    - {m}')
        else:
            print('  ✓ Core directories present')

    print()
    print('Cleaning installer download cache...')
    _cleanup_stale_archives(downloads_dir)

    # Write config and make launcher executable
    _write_install_config(install_dir, venv_py)
    _make_launcher_executable()

    print()
    _separator()
    on_mac = platform.system() == 'Darwin'
    on_win = platform.system() == 'Windows'
    if on_mac:
        print('  ✓ Installation complete. Double-click Launch.command to start.')
    elif on_win:
        print('  ✓ Installation complete. Double-click Launch.vbs to start.')
    else:
        print('  ✓ Installation complete. Run: python3 launch.py')
    _separator()
    print()


# ---------------------------------------------------------------------------
# Progress bar helper
# ---------------------------------------------------------------------------

_last_pct = -1


def _progress_bar(downloaded: int, total: int):
    global _last_pct
    if total <= 0:
        return
    pct = int(downloaded * 100 / total)
    if pct == _last_pct:
        return
    _last_pct = pct
    filled = pct // 5
    bar = '█' * filled + '░' * (20 - filled)
    print(f'\r    [{bar}] {pct:3d}%', end='', flush=True)


if __name__ == '__main__':
    _last_pct = -1
    main()
