# INSTALL_NSDDD_v3.ipynb — Notebook Structure

This document outlines the structure of the main installer Jupyter notebook.

## Section 1: Welcome and Prerequisites (Cells 1–5)

### Cell 1: Title and Introduction
- Display welcome message with NSDDD v3 information
- Citation and licensing
- What users will get
- Installation time estimate (20–30 minutes)

### Cell 2: System Requirements Check
- Python version check (≥3.9)
- Operating system detection (macOS/Linux/Windows)
- Free disk space check
- RAM check (if psutil available)
- Summary of requirements

### Cell 3: Installation Directory Setup
- Text input widget for installation directory name (default: `NSDDD_v3_workspace`)
- Display target directory path
- Display expected structure
- Create directory

### Cell 4: Download Selection
- Checkboxes for optional components:
  - ☑ Model files + metadata + docs (required, 8 GB) — always selected
  - ☐ Clean text documents (optional, 40 MB)
  - ☐ SpaCy sentence-segmented documents (optional, 50 MB)
  - ☐ PDF originals (optional, 6 GB)
  - ☐ Original language documents (optional, 20 MB)
  - ☐ Original language SpaCy documents (optional, 20 MB)
- Calculate total size based on selections
- Check available disk space
- Warn if insufficient space

### Cell 5: Summary Before Starting
- Display all configuration choices
- Required files and optional selections
- Total download size and time estimate
- Disk space verification
- Confirmation button: "Start Installation"

## Section 2: Environment Setup (Cells 6–10)

### Cell 6: Virtual Environment Check
- Detect if already in a venv
- If not, offer to create one (optional)
- Explain benefits of venv (isolation, version management)
- Install venv if user chooses

### Cell 7: Install Dependencies
- Install packages from requirements.txt
- Show progress as packages install
- Verify installations succeeded

### Cell 8: Verify Installation
- Import core packages (sentence-transformers, numpy, scipy)
- Display versions
- Verify sentence-transformers model downloads (this may take 1–2 minutes)

### Cell 9: Environment Summary
- Display environment information
- Python version and location
- Installed packages and versions

## Section 3: Download Required Files (Cells 11–15)

### Cell 10: Connect to DataShare
- Initialise DataShare API client with handle
- Fetch dataset file list from DataShare API
- Display available files and sizes
- Verify handle is accessible

### Cell 11: Download Model Files
- Display: "Downloading model_files.zip (4.7 GB)"
- Progress bar for download
- Estimated time based on connection speed
- Resume capability if interrupted

### Cell 12: Extract Model Files
- Extract model_files.zip to model/
- Display extracted files
- Progress bar

### Cell 13: Verify Model File Integrity
- Load checksums.txt from extracted model_files.zip
- Verify each JSON file against SHA-256 checksum
- Display verification results (✓ or ✗)
- Abort if verification fails

### Cell 14: Download Metadata and Documentation
- Download metadata.zip
- Extract to metadata/
- Download documentation.zip
- Extract to documentation/
- Verify extracted files present

## Section 4: Download Optional Document Sets (Cells 15–20)

### Cell 15: Download Selected Optional Files
- For each selected optional component:
  - Download (e.g., clean_text_documents_English_and_translated.zip)
  - Extract to documents/ directory
  - Display progress
- Skip components user didn't select
- Handle download failures gracefully

### Cell 16: Organise Downloaded Documents
- Document files in documents/ are already organised by country
- Display directory tree of documents/
- Count documents per type

## Section 5: Directory Structure Verification (Cells 21–23)

### Cell 17: Create Final Directory Structure
- Verify all expected directories exist
- Display final directory tree:
  ```
  NSDDD_v3_workspace/
  ├── model/                    # 11.5 GB
  │   ├── segment_encodings.json
  │   ├── segments_dict.json
  │   ├── encoded_segments.json
  │   ├── documents_dict.json
  │   ├── countries_dict.json
  │   └── checksums.txt
  ├── metadata/                 # < 1 MB
  │   ├── document_metadata.csv
  │   ├── Country_metadata.csv
  │   ├── Freedom_house.csv
  │   └── ... [other metadata CSVs]
  ├── documentation/            # 20 KB
  │   ├── SEMANTIC_SEARCH_GUIDE.md
  │   ├── NSDDD_v3_LAUNCH_REPORT.md
  │   └── ... [other docs]
  ├── documents/                # [optional, 0–13 GB]
  │   ├── clean_text_documents_English_and_translated/
  │   ├── spacy_documents/
  │   ├── pdf_originals/
  │   ├── original_language_documents/
  │   └── original_language_spacy/
  └── downloads/                # [temporary, can be deleted]
  ```

### Cell 18: Installation Summary
- Total disk space used: calculated from actual files
- File counts by component
- Installation directory location

## Section 6: Verification Tests (Cells 24–30)

### Cell 19: Load and Test Model Files
- Load segment_encodings.json (11 GB, takes ~60–120 seconds)
- Load all other JSON files
- Verify data structures
- Display: "✓ Model files loaded successfully"

### Cell 20: Load Sentence Transformer Model
- Load sentence-transformers/all-mpnet-base-v2
- Display model information
- Test encoding a sample sentence (this verifies encoder works)

### Cell 21: Run Sample Semantic Search
- Define test query: "Cyber threats to critical infrastructure"
- Encode query using loaded encoder
- Search segment_encodings for similar vectors (top 10 results)
- Display results:
  ```
  Query: "Cyber threats to critical infrastructure"
  Results (Top 10):
  ┌─────┬──────────┬────────────┬─────────────────────────────────────┐
  │ Rank│ Segment  │ Similarity │ Text Preview                        │
  ├─────┼──────────┼────────────┼─────────────────────────────────────┤
  │  1  │ 42/15    │ 0.891      │ "Critical infrastructure cyber...  │
  │  2  │ 127/8    │ 0.876      │ "Protecting digital systems and...  │
  │  ... │  ...     │  ...       │ ...                                 │
  └─────┴──────────┴────────────┴─────────────────────────────────────┘
  ```

### Cell 22: Test Result Clustering
- Cluster top 20 results using inter-segment similarity
- Display cluster summary
- Verify clustering works

### Cell 23: Performance Benchmark
- Benchmark encoding speed (queries per second)
- Benchmark search speed (segments searched per second)
- Display performance metrics

### Cell 24: Verification Summary
- Display: "✓ All verification tests passed"
- System is ready for use

## Section 7: Next Steps and Cleanup (Cells 31–33)

### Cell 25: Cleanup Temporary Downloads
- Option to delete downloaded zip files (frees 8–15 GB space)
- Show what will be deleted
- Confirm before deleting
- Display space freed

### Cell 26: Documentation and Next Steps
- Display file paths to documentation
- Link to GETTING_STARTED.ipynb
- Suggest reading SEMANTIC_SEARCH_GUIDE.md
- List example research questions

### Cell 27: Citation Information
- Display recommended citation format
- Explain CC-BY 4.0 license
- Link to dataset on DataShare

### Cell 28: Completion Summary
- Display: "✓✓✓ Installation Complete!"
- Installation directory location
- Next steps (open GETTING_STARTED.ipynb)
- Support information (GitHub issues, email, etc.)

## Key Features of Notebook

1. **Progress tracking**: Each major step has clear ✓/✗ indicators
2. **Error recovery**: If download fails, can resume from where it stopped
3. **Flexibility**: User can choose which optional documents to download
4. **Verification**: SHA-256 checksums verify file integrity
5. **Testing**: Comprehensive tests ensure everything works before completion
6. **Documentation**: Links to complete documentation and guides
7. **Interactivity**: Uses ipywidgets for user input and choices

## Dependencies Within Notebook

The notebook will import and use:

```python
import sys
import platform
import shutil
from pathlib import Path
import json
import numpy as np
from tqdm import tqdm
import ipywidgets as widgets
from IPython.display import display, Markdown, HTML
import requests
import zipfile
import os
import time

# Local modules
from config import DATASHARE_HANDLE, DATASHARE_API_BASE, DOWNLOADS
from utils.datashare import DataShareClient
from utils.download import download_file, calculate_total_size, check_disk_space
from utils.verify import verify_file, calculate_sha256, load_checksums_file, verify_directory
from utils.setup import create_directory_structure, display_directory_structure, get_directory_size

# Third-party for actual search
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
```

## Estimated Notebook Size

- Total notebook: ~150–200 code cells + ~50 markdown cells
- Execution time: 20–30 minutes (depending on internet speed)
- File size: ~500 KB as .ipynb
