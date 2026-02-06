# NSDDD v3 Installer

Official installer for the **National Security Documents Dataset** (NSDDD) version 3.

NSDDD v3 is a comprehensive corpus of **660 national security strategy documents** from **119 countries** spanning **1987–2025**, with **726,307 pre-computed semantic embeddings** (MPNet 768-dimensional vectors) enabling local semantic search without API keys or internet connection.

## Quick Start

### Prerequisites

- Python 3.9 or newer
- pip (Python package installer)
- Jupyter Lab or Jupyter Notebook
- 15 GB free disk space (minimum)
- 16 GB RAM (recommended)

**Note**: No conda required, no API keys needed.

### Installation (3 steps)

**1. Clone this repository:**

```bash
git clone https://github.com/[username]/NSDDD_v3_installer.git
cd NSDDD_v3_installer
```

**2. Install Jupyter (if not already installed):**

```bash
pip install jupyter jupyterlab
```

**3. Open the installer notebook:**

```bash
jupyter lab INSTALL_NSDDD_v3.ipynb
```

Follow the installation steps in the notebook. The installer will:

- Check your system requirements
- Download NSDDD v3 files from Edinburgh DataShare (~8–15 GB depending on options selected)
- Extract files to the correct directory structure
- Verify file integrity with SHA-256 checksums
- Test model loading
- Set up your working environment

## What Gets Installed?

After installation, you'll have:

- **660 national security documents** from 119 countries (1987–2025)
- **726,307 pre-computed MPNet embeddings** (768-dimensional vectors)
- **Complete metadata**: Country information, publication years, document types
- **Semantic search capability**: Search for security concepts across all documents locally
- **Python code examples**: Tutorial notebook with working code
- **Documentation**: Complete methodology and usage guide

## System Requirements

| Requirement | Minimum | Recommended |
|---|---|---|
| Python | 3.9 | 3.11+ |
| Disk space | 15 GB | 20 GB |
| RAM | 8 GB* | 16 GB |
| Internet | For download | For download only |

*Note: The semantic search model file is 11 GB and requires sufficient RAM to load. A minimum of 16 GB is recommended to avoid memory pressure.

## What Can You Do With NSDDD v3?

All searches run **locally** on your computer using pre-computed embeddings. No external APIs or internet connection required after installation.

### Example Uses

**Semantic search**:
```python
"Find all mentions of cyber threats to critical infrastructure"
→ Returns 45 matching segments from 12 countries
```

**Topic analysis**:
```python
"Which countries identify climate change as a security threat?"
→ Shows temporal patterns and cross-national trends
```

**Document exploration**:
```python
"Extract all references to supply chain security"
→ Provides segments, countries, years, and similarity scores
```

**Comparative analysis**:
```python
"How has terrorism been framed in European vs. Asian security documents?"
→ Semantic clustering of threat constructions across regions
```

## Installation Time

- **Fast connection** (100 Mbps): 15–20 minutes
- **Standard connection** (25 Mbps): 30–45 minutes
- **Slow connection** (5 Mbps): 2–3 hours

The installer supports resume capability—if interrupted, simply re-run the notebook and downloads will continue from where they stopped.

## Disk Space Breakdown

| Component | Size | Required? |
|---|---|---|
| Model files (embeddings + segments) | 8 GB | Yes |
| Metadata | <1 MB | Yes |
| Documentation | 20 KB | Yes |
| Plain text documents | 40 MB | Optional |
| Sentence-segmented documents | 50 MB | Optional |
| PDF originals | 6 GB | Optional |
| Original language documents | 20 MB | Optional |

**Minimum install**: 8.02 GB (semantic search only)
**With documents**: 8.04–8.05 GB
**Complete**: ~15 GB

## Dataset Information

**Coverage**: 660 documents from 119 countries, 1987–2025

**Document types**: National security strategies, defence white papers, strategic reviews

**Languages**: 80+ languages (primarily English + 20+ European languages)

**Segments**: 726,307 paragraph-level text segments with embeddings

**Encoding model**: sentence-transformers/all-mpnet-base-v2 (768-dimensional)

**DataShare repository**: [Link to be added after publication]

## Citation

If you use NSDDD v3 in research, please cite:

```bibtex
@dataset{gardner_2025_nsddd_v3,
  author       = {Gardner, Andrew Neal},
  title        = {National Security Documents Dataset (NSDDD) Version 3},
  year         = {2025},
  publisher    = {Edinburgh DataShare},
  url          = {https://doi.org/10.7488/ds/[DOI_TO_BE_ADDED]},
  institution  = {University of Edinburgh},
  note         = {660 national security strategy documents from 119 countries, 1987–2025, with MPNet embeddings}
}
```

Or in text form:

> Gardner, A. N. (2025). National Security Documents Dataset (NSDDD) Version 3. University of Edinburgh. https://doi.org/10.7488/ds/[DOI_TO_BE_ADDED]

## Getting Started After Installation

After installation completes, open `GETTING_STARTED.ipynb` for a tutorial covering:

- Loading the data model
- Running semantic searches
- Filtering by country, year, and document type
- Clustering and analysing results
- Extracting segments for further analysis
- Example research queries

## Troubleshooting

### 'FileNotFoundError' during installation?

- Check your internet connection
- Verify Edinburgh DataShare is accessible (https://datashare.ed.ac.uk)
- Try re-running the installer—it supports resuming interrupted downloads

### 'Insufficient disk space' error?

- You need at least 15 GB free
- Try not downloading optional PDF set (saves 6 GB)
- Clear other temporary files

### 'Memory error' when loading models?

- You need 16 GB RAM minimum
- Close other applications
- Consider running on a machine with more memory

### Downloads running slowly?

- Check your internet connection speed
- The installer will resume if interrupted—safe to pause and restart

### Other issues?

- Check the documentation included in the installation
- See `SEMANTIC_SEARCH_GUIDE.md` for comprehensive help
- Report issues on GitHub: [link to issues]

## License

NSDDD v3 is licensed under Creative Commons Attribution 4.0 International (CC-BY 4.0).

The documents in NSDDD v3 are official government publications in the public domain.

See `LICENSE.txt` (included after installation) for full details.

## Support

For questions, issues, or feedback:

- **GitHub Issues**: [Report bugs or request features]
- **Email**: [Contact information]
- **Documentation**: See included documentation files
- **DataShare**: [Link to dataset page]

## Dataset Versioning

- **NSDDD v3** (2025): Fresh MPNet-based encodings, complete reorganisation
- **NSDDD v2** (2023): Previous version with USE-4 embeddings
- **NSDDD v1** (2022): Initial release

See `NSDDD_v3_LAUNCH_REPORT.md` (included after installation) for version comparison.

## References

**Semantic search methodology**: See `SEMANTIC_SEARCH_GUIDE.md` (included)

**Dataset inclusion criteria**: See `INCLUSION_CRITERIA.md` (included)

**Language audit**: See `LANGUAGE_AUDIT_REPORT.md` (included)

---

**Happy researching!** 🔍

For information about Edinburgh DataShare and the full dataset: [datashare.ed.ac.uk](https://datashare.ed.ac.uk)
