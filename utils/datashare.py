"""
Edinburgh DataShare REST API Client

Module for interacting with Edinburgh DataShare API to list and retrieve files.
"""

import requests
from typing import List, Dict, Optional
import json


class DataShareClient:
    """
    Client for Edinburgh DataShare REST API.

    Provides methods to:
    - List files in a dataset
    - Get file metadata (sizes, checksums, etc.)
    - Construct download URLs
    - Query dataset information
    """

    def __init__(self, api_base: str, handle: str):
        """
        Initialise DataShare client.

        Args:
            api_base: Base URL for DataShare API (e.g., https://datashare.ed.ac.uk/rest)
            handle: Dataset handle (e.g., 10283/XXXXX)
        """
        self.api_base = api_base.rstrip('/')
        self.handle = handle
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'NSDDD-v3-Installer/1.0',
            'Accept': 'application/json'
        })
        self._item_id = None

    def get_item_metadata(self) -> Dict:
        """
        Get item metadata from DataShare using handle lookup.

        Returns:
            Dictionary with item metadata including UUID, title, description

        Raises:
            requests.RequestException: If API request fails
            ValueError: If handle not found
        """
        url = f'{self.api_base}/handle/{self.handle}'
        response = self.session.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        if not data or 'uuid' not in data:
            raise ValueError(f'Handle {self.handle} not found or invalid')

        self._item_id = data['uuid']
        return data

    def _get_item_id(self) -> str:
        """
        Get item UUID from handle (with caching).

        Returns:
            Item UUID as string
        """
        if self._item_id is None:
            metadata = self.get_item_metadata()
            self._item_id = metadata['uuid']
        return self._item_id

    def list_bitstreams(self) -> List[Dict]:
        """
        List all files (bitstreams) in the dataset.

        Returns:
            List of dictionaries with file metadata including:
            - name: Filename
            - size: File size in bytes
            - id: Bitstream ID
            - checksum: SHA-256 checksum (if available)
            - mimeType: File MIME type

        Raises:
            requests.RequestException: If API request fails
        """
        item_id = self._get_item_id()
        url = f'{self.api_base}/items/{item_id}/bitstreams'
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_download_url(self, bitstream_uuid: str) -> str:
        """
        Construct download URL for a bitstream.

        Args:
            bitstream_uuid: UUID of the bitstream to download

        Returns:
            Full download URL
        """
        return f'{self.api_base}/bitstreams/{bitstream_uuid}/retrieve'

    def find_file_by_name(self, filename: str) -> Dict:
        """
        Find a specific file by name in the dataset.

        Args:
            filename: Name of file to find

        Returns:
            Dictionary with file metadata (name, size, id, checksum, etc.)

        Raises:
            FileNotFoundError: If file not found in dataset
        """
        bitstreams = self.list_bitstreams()
        for bitstream in bitstreams:
            if bitstream.get('name') == filename:
                return bitstream

        available = [b.get('name', 'unknown') for b in bitstreams]
        raise FileNotFoundError(
            f'File "{filename}" not found in dataset.\n'
            f'Available files: {", ".join(available)}'
        )

    def get_file_info(self, filename: str) -> Dict:
        """
        Get detailed information about a file.

        Args:
            filename: Name of file

        Returns:
            Dictionary with:
            - name: Filename
            - size_bytes: Size in bytes
            - size_mb: Size in MB
            - size_gb: Size in GB
            - uuid: Bitstream UUID
            - download_url: Full download URL
            - checksum: MD5 checksum if available
        """
        bitstream = self.find_file_by_name(filename)

        size_bytes = bitstream.get('sizeBytes', 0)
        size_mb = size_bytes / (1024 ** 2)
        size_gb = size_bytes / (1024 ** 3)

        return {
            'name': bitstream.get('name'),
            'size_bytes': size_bytes,
            'size_mb': round(size_mb, 2),
            'size_gb': round(size_gb, 2),
            'uuid': bitstream.get('uuid'),
            'download_url': self.get_download_url(bitstream.get('uuid')),
            'checksum': bitstream.get('checkSum', {}).get('value', 'N/A'),
            'mime_type': bitstream.get('mimeType')
        }

    def list_all_files(self) -> List[str]:
        """
        List all available filenames in the dataset.

        Returns:
            List of filenames
        """
        bitstreams = self.list_bitstreams()
        return [b.get('name', 'unknown') for b in bitstreams]

    def verify_handle(self) -> bool:
        """
        Verify that the handle is accessible.

        Returns:
            True if handle is accessible, False otherwise
        """
        try:
            self.get_item_metadata()
            return True
        except Exception:
            return False

    def get_dataset_summary(self) -> Dict:
        """
        Get summary information about the dataset.

        Returns:
            Dictionary with dataset info (files, total size, etc.)
        """
        bitstreams = self.list_bitstreams()

        total_size_bytes = sum(b.get('sizeBytes', 0) for b in bitstreams)
        total_size_gb = total_size_bytes / (1024 ** 3)

        return {
            'file_count': len(bitstreams),
            'total_size_bytes': total_size_bytes,
            'total_size_gb': round(total_size_gb, 2),
            'files': [b.get('name', 'unknown') for b in bitstreams]
        }
