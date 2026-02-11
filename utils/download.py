"""
Download utilities for NSDDD v3 installation.

Provides file download with progress tracking, resume capability, and error handling.
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
from pathlib import Path
from typing import Callable, Optional
import time


def create_download_session(timeout: int = 300) -> requests.Session:
    """
    Create a requests session with proper timeout and retry configuration.

    Args:
        timeout: Timeout in seconds for connections and reads

    Returns:
        Configured requests.Session with retry strategy
    """
    session = requests.Session()

    # Create retry strategy for transient failures
    # Don't retry on the session level - we handle retries in download_file
    retry_strategy = Retry(
        total=0,  # We handle retries at function level
        backoff_factor=0,
        status_forcelist=[]
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    # Set reasonable defaults
    session.headers.update({
        'User-Agent': 'NSDDD-v3-Installer/1.0'
    })

    return session


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
    timeout: int = 300,
    progress_callback: Optional[Callable] = None,
    expected_size: Optional[int] = None,
    max_retries: int = 3
) -> Path:
    """
    Download file with progress bar and resume capability.

    Args:
        url: URL to download from
        destination: Local file path to save to
        resume: If True, resume partial downloads. If False, overwrite.
        chunk_size: Bytes per chunk (default 8KB)
        timeout: Request timeout in seconds (default 300s / 5 minutes)
        progress_callback: Optional callback function(bytes_downloaded, total_bytes)
        expected_size: Expected file size in bytes (used as fallback if Content-Length unavailable)
        max_retries: Maximum number of retries for transient failures

    Returns:
        Path object for downloaded file

    Raises:
        requests.RequestException: If download fails after retries
        IOError: If file writing fails
    """
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)

    # Create session with proper timeout configuration
    session = create_download_session(timeout)

    # Retry loop for transient failures
    last_error = None
    for attempt in range(max_retries):
        try:
            # Check for partial download
            downloaded_size = 0
            headers = {}

            if destination.exists() and resume:
                existing_size = destination.stat().st_size

                # Check if existing file is larger than expected (corrupted download)
                if expected_size is not None and existing_size > expected_size:
                    print(f'\n  ⚠ Existing file is larger than expected ({existing_size / (1024**2):.0f} MB > {expected_size / (1024**2):.0f} MB)')
                    print(f'  ⚠ File may be corrupted from previous attempt')
                    print(f'  ⊗ Deleting corrupted file and starting fresh...\n')
                    destination.unlink()
                    downloaded_size = 0
                    headers = {}
                    mode = 'wb'
                else:
                    downloaded_size = existing_size
                    headers['Range'] = f'bytes={downloaded_size}-'
                    mode = 'ab'
            else:
                mode = 'wb'

            # Make request with explicit timeout tuple (connection, read)
            # This ensures both connection and read operations respect the timeout
            response = session.get(
                url,
                headers=headers,
                stream=True,
                timeout=(timeout, timeout),  # (connection_timeout, read_timeout)
                allow_redirects=True
            )
            response.raise_for_status()
            break  # Success, exit retry loop

        except (requests.ConnectionError, requests.Timeout) as e:
            last_error = e
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 5  # 5s, 10s, 15s backoff
                print(f'  ⚠ Connection timeout, retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})...')
                time.sleep(wait_time)
                continue
            else:
                raise requests.RequestException(f'Failed to connect to {url} after {max_retries} attempts: {e}')
        except requests.RequestException as e:
            raise requests.RequestException(f'Failed to connect to {url}: {e}')
        finally:
            # Close session on each retry to ensure clean state
            if attempt < max_retries - 1:
                session.close()
                session = create_download_session(timeout)

    # Get total size from Content-Length header or use expected_size
    content_length = response.headers.get('content-length', '0')
    try:
        content_length = int(content_length)
    except ValueError:
        content_length = 0

    # Determine the actual total file size
    # When resuming, server may return full file size or remaining bytes in Content-Length
    if expected_size is not None:
        # Use expected_size as authoritative total
        total_size = expected_size
        if content_length == 0:
            # If no Content-Length, estimate remaining bytes
            remaining = max(0, expected_size - downloaded_size)
    else:
        # No expected_size, estimate from Content-Length
        if content_length > 0:
            # Server returned size; assume it's remaining (when resuming) or full (when starting)
            if downloaded_size > 0 and content_length < downloaded_size:
                # Clearly remaining bytes (resuming)
                total_size = content_length + downloaded_size
            else:
                # Could be full file or remaining; estimate as full
                total_size = max(content_length, content_length + downloaded_size)
        else:
            # No size information
            total_size = 0

    # If no size info and file exists, assume download is complete
    if total_size == 0 and destination.exists():
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

                    # Detect if we're receiving more data than expected
                    if total_size > 0 and bytes_downloaded > total_size:
                        print(f'\n  ✗ ERROR: Received more data than expected!')
                        print(f'  Downloaded: {bytes_downloaded / (1024**2):.0f} MB')
                        print(f'  Expected: {total_size / (1024**2):.0f} MB')
                        print(f'  This indicates a server issue or corrupted download.')
                        print(f'  Deleting corrupted file...\n')
                        f.close()
                        destination.unlink()
                        raise IOError(f'Download exceeded expected size: {bytes_downloaded} > {total_size}')

                    if progress_callback:
                        # Cap progress at 100% for display purposes
                        display_downloaded = min(bytes_downloaded, total_size) if total_size > 0 else bytes_downloaded
                        progress_callback(display_downloaded, total_size)

    except (requests.ConnectionError, requests.Timeout) as e:
        # Transient network error during download - file can be resumed
        print(f'\n  ⚠ Download interrupted: {type(e).__name__}')
        print(f'  Downloaded {bytes_downloaded / (1024**2):.0f} MB so far')
        print(f'  Restart this cell to resume from where it stopped.')
        raise requests.RequestException(f'Download interrupted after {bytes_downloaded / (1024**2):.0f} MB: {e}')
    except IOError as e:
        session.close()
        raise IOError(f'Failed to write to {destination}: {e}')
    finally:
        # Always close the session
        session.close()

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
