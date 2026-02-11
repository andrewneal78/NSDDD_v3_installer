"""
Download utilities for NSDDD v3 installation.

Provides file download with progress tracking, resume capability, and error handling.
"""

import requests
import os
from pathlib import Path
from typing import Callable, Optional
import time


def calculate_total_size(downloads_dict: dict, selected_keys: list) -> dict:
    """
    Calculate total disk space needed for selected downloads.

    Args:
        downloads_dict: Configuration dictionary with download specs
        selected_keys: List of selected download keys

    Returns:
        Dictionary with:
        - total_mb: Total size in MB
        - total_gb: Total size in GB
        - breakdown: List of (name, size_gb) tuples
    """
    total_mb = 0
    total_gb = 0
    breakdown = []

    for key in selected_keys:
        if key in downloads_dict:
            size_gb = downloads_dict[key]['size_gb']
            total_mb += downloads_dict[key]['size_mb']
            total_gb += size_gb
            breakdown.append((downloads_dict[key]['description'], size_gb))

    return {
        'total_mb': total_mb,
        'total_gb': round(total_gb, 2),
        'breakdown': breakdown
    }


def download_file(
    url: str,
    destination: str,
    resume: bool = True,
    chunk_size: int = 8192,
    timeout: int = 30,
    progress_callback: Optional[Callable] = None,
    expected_size: Optional[int] = None
) -> Path:
    """
    Download file with progress bar and resume capability.

    Args:
        url: URL to download from
        destination: Local file path to save to
        resume: If True, resume partial downloads. If False, overwrite.
        chunk_size: Bytes per chunk (default 8KB)
        timeout: Request timeout in seconds
        progress_callback: Optional callback function(bytes_downloaded, total_bytes)
        expected_size: Expected file size in bytes (used as fallback if Content-Length unavailable)

    Returns:
        Path object for downloaded file

    Raises:
        requests.RequestException: If download fails
        IOError: If file writing fails
    """
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)

    # Check for partial download
    downloaded_size = 0
    headers = {}

    if destination.exists() and resume:
        downloaded_size = destination.stat().st_size
        headers['Range'] = f'bytes={downloaded_size}-'
        mode = 'ab'
    else:
        mode = 'wb'

    # Make request
    try:
        response = requests.get(
            url,
            headers=headers,
            stream=True,
            timeout=timeout,
            allow_redirects=True
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise requests.RequestException(f'Failed to connect to {url}: {e}')

    # Get total size from Content-Length header or use expected_size
    content_length = response.headers.get('content-length', '0')
    try:
        content_length = int(content_length)
    except ValueError:
        content_length = 0

    # Use expected_size as fallback if Content-Length not available
    if content_length == 0 and expected_size is not None:
        content_length = expected_size - downloaded_size

    # If resuming, content-length is remaining bytes; total is remaining + downloaded
    total_size = content_length + downloaded_size

    # If no content-length and file exists, assume download is complete
    if content_length == 0 and destination.exists():
        return destination

    # Download with progress callback
    start_time = time.time()
    bytes_downloaded = downloaded_size

    try:
        with open(destination, mode) as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    bytes_downloaded += len(chunk)

                    if progress_callback:
                        progress_callback(bytes_downloaded, total_size)

    except IOError as e:
        raise IOError(f'Failed to write to {destination}: {e}')

    elapsed = time.time() - start_time
    speed_mbps = (bytes_downloaded / (1024 ** 2)) / elapsed if elapsed > 0 else 0

    return destination


def verify_download(filepath: Path, expected_size: Optional[int] = None) -> bool:
    """
    Verify downloaded file.

    Args:
        filepath: Path to file
        expected_size: Expected file size in bytes (optional)

    Returns:
        True if file exists and size is correct (if expected_size provided)
    """
    if not filepath.exists():
        return False

    if expected_size is not None:
        actual_size = filepath.stat().st_size
        return actual_size == expected_size

    return True


def get_free_disk_space(path: str) -> dict:
    """
    Get available disk space at given path.

    Args:
        path: Directory path

    Returns:
        Dictionary with:
        - free_mb: Free space in MB
        - free_gb: Free space in GB
        - total_mb: Total space in MB
        - total_gb: Total space in GB
    """
    try:
        stat = os.statvfs(path)
        free_bytes = stat.f_bavail * stat.f_frsize
        total_bytes = stat.f_blocks * stat.f_frsize

        return {
            'free_mb': round(free_bytes / (1024 ** 2), 2),
            'free_gb': round(free_bytes / (1024 ** 3), 2),
            'total_mb': round(total_bytes / (1024 ** 2), 2),
            'total_gb': round(total_bytes / (1024 ** 3), 2)
        }
    except Exception:
        return {
            'free_mb': 0,
            'free_gb': 0,
            'total_mb': 0,
            'total_gb': 0
        }


def check_disk_space(path: str, required_gb: float) -> tuple:
    """
    Check if sufficient disk space is available.

    Args:
        path: Directory path to check
        required_gb: Required space in GB

    Returns:
        Tuple (is_sufficient: bool, available_gb: float, required_gb: float)
    """
    space_info = get_free_disk_space(path)
    available_gb = space_info['free_gb']
    return available_gb >= required_gb, available_gb, required_gb
