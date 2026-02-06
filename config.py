"""
Configuration for NSDDD v3 Installation

This module contains all configuration settings for downloading and installing
the National Security Documents Dataset (NSDDD) version 3 from Edinburgh DataShare.
"""

# DataShare API endpoints
DATASHARE_API_BASE = 'https://datashare.ed.ac.uk/rest'

# DataShare handle (to be filled after dataset publication)
# Format: 10283/XXXXX
DATASHARE_HANDLE = '10283/[HANDLE_TO_BE_ADDED]'

# Construct base URL for files
DATASHARE_ITEM_URL = f'{DATASHARE_API_BASE}/handle/{DATASHARE_HANDLE}'

# Download specifications
DOWNLOADS = {
    # REQUIRED downloads (essential for semantic search)
    'model_files': {
        'filename': 'model_files.zip',
        'size_mb': 4700,
        'size_gb': 4.7,
        'extract_to': 'model/',
        'required': True,
        'description': 'Model files: MPNet embeddings and segment data (11.5GB uncompressed)'
    },
    'metadata': {
        'filename': 'metadata.zip',
        'size_mb': 1,
        'size_gb': 0.001,
        'extract_to': 'metadata/',
        'required': True,
        'description': 'Metadata: document and country information'
    },
    'documentation': {
        'filename': 'documentation.zip',
        'size_mb': 20,
        'size_gb': 0.02,
        'extract_to': 'documentation/',
        'required': True,
        'description': 'Documentation: guides and methodology'
    },

    # OPTIONAL downloads (user chooses which to download)
    'clean_text_documents': {
        'filename': 'clean_text_documents_English_and_translated.zip',
        'size_mb': 40,
        'size_gb': 0.04,
        'extract_to': 'documents/',
        'optional': True,
        'description': '660 plain text documents (English + translated)'
    },
    'spacy_documents': {
        'filename': 'spacy_documents.zip',
        'size_mb': 50,
        'size_gb': 0.05,
        'extract_to': 'documents/',
        'optional': True,
        'description': '660 sentence-segmented documents'
    },
    'pdf_originals': {
        'filename': 'pdf_originals.zip',
        'size_mb': 6000,
        'size_gb': 6.0,
        'extract_to': 'documents/',
        'optional': True,
        'description': '635 original PDFs organized by country (7.7GB uncompressed)'
    },
    'original_language_documents': {
        'filename': 'original_language_documents.zip',
        'size_mb': 10,
        'size_gb': 0.01,
        'extract_to': 'documents/',
        'optional': True,
        'description': '128 original language plain text files'
    },
    'original_language_spacy': {
        'filename': 'original_language_spacy.zip',
        'size_mb': 10,
        'size_gb': 0.01,
        'extract_to': 'documents/',
        'optional': True,
        'description': '129 original language sentence-segmented files'
    }
}

# System requirements
PYTHON_VERSION_MIN = (3, 9)
DISK_SPACE_REQUIRED_MIN_GB = 15  # Minimum for model files only
RAM_REQUIRED_GB = 16  # Recommended for loading 11GB embedding file

# Installation directory naming
DEFAULT_INSTALL_DIR = 'NSDDD_v3_workspace'

# Dependencies (from requirements.txt)
CORE_DEPENDENCIES = [
    'sentence-transformers>=2.2.0',
    'numpy>=1.24.0',
    'scipy>=1.10.0',
    'networkx>=3.0',
    'ipywidgets>=8.0.0',
    'tqdm>=4.65.0',
    'requests>=2.31.0',
    'psutil>=5.9.0'
]

# Optional dependencies for visualisation
OPTIONAL_DEPENDENCIES = [
    'matplotlib>=3.7.0',
    'seaborn>=0.12.0',
    'pandas>=1.5.0'
]

# Download and verification settings
CHUNK_SIZE = 8192  # Bytes per chunk for downloads
RETRY_ATTEMPTS = 3
TIMEOUT_SECONDS = 30

# Dataset information
DATASET_NAME = 'National Security Documents Dataset (NSDDD) Version 3'
DATASET_DOCUMENTS = 660
DATASET_COUNTRIES = 119
DATASET_YEARS = '1987–2025'
DATASET_SEGMENTS = 726307
DATASET_ENCODING_DIM = 768
