# NSDDD v3 Installer

Official installer for the **National Security Documents Dataset** (NSDDD) version 3.

NSDDD v3 is a comprehensive corpus of **660 national security strategy documents** from **118 countries** spanning **1987–2025**, with **726,307 pre-computed semantic embeddings** (MPNet 768-dimensional vectors) enabling local semantic search without API keys or internet connection.

## Quick Start

### Prerequisites

- Python 3.9 or newer
- pip (Python package installer)
- Jupyter Notebook
- 15 GB free disk space (minimum)
- 16 GB RAM (recommended)

**Note**: No conda required, no API keys needed, no Python coding required.

### Installation (3 steps)

**1. Clone this repository:**

```bash
git clone https://github.com/andrewneal78/NSDDD_v3_installer.git
cd NSDDD_v3_installer
```

**2. Install Jupyter Notebook (if not already installed):**

```bash
pip install notebook
```

**3. Open the installer notebook:**

```bash
jupyter notebook INSTALL_NSDDD_v3.ipynb
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

- **Interactive search notebook**: Widget-based interface—no coding required
- **660 national security documents** from 118 countries (1987–2025)
- **726,307 pre-computed MPNet embeddings** (768-dimensional vectors)
- **Complete metadata**: Country information, publication years, document types, organizational memberships
- **Semantic search capability**: Search for security concepts across all documents locally
- **Advanced filtering**: By country, region, organization, income group, democracy status, year
- **Documentation**: Complete methodology and usage guide

## System Requirements

| Requirement | Minimum      | Recommended       |
| ----------- | ------------ | ----------------- |
| Python      | 3.9          | 3.11+             |
| Disk space  | 15 GB        | 20 GB             |
| RAM         | 8 GB*        | 16 GB             |
| Internet    | For download | For download only |

*Note: The semantic search model file is 11 GB and requires sufficient RAM to load. A minimum of 16 GB is recommended to avoid memory pressure.

## What Can You Do With NSDDD v3?

All searches run **locally** on your computer using pre-computed embeddings. No external APIs, internet connection, or Python coding required after installation.

### How It Works

After installation, open the **Document Metadata Search Tool** notebook:

```bash
jupyter notebook document_metadata_search.ipynb
```

The notebook provides an **interactive widget interface**:

1. **Run all cells** to load the dataset and launch the search interface
2. **Enter search queries** in the text box (e.g., 'cyber threats to critical infrastructure')
3. **Select filters** using dropdown menus:
   - Countries (single or multiple)
   - UN Regions (Asia, Europe, Africa, Americas, Oceania)
   - Organizations (NATO, EU, ASEAN, BRICS, Commonwealth, G7, G20, etc.)
   - Income groups (High, Upper-middle, Lower-middle, Low)
   - Democracy status (Free, Partly Free, Not Free)
   - ODA recipient status
   - Years (1987–2025)
4. **Click 'Search'** to find matching document segments
5. **Review results** with similarity scores, document context, and clustering
6. **Export results** to CSV with configurable options:
   - Toggle CSV export on/off (useful for quick exploratory searches)
   - Enable iterative filenames (adds timestamps to prevent overwriting previous results)
   - Export includes metadata, similarity scores, document context, and cluster assignments

### Example Searches

**Cyber security threats**:
- Query: `cyber threats to critical infrastructure`
- Filters: NATO members, 2020–2025
- Result: ~45 segments showing how NATO countries frame cyber threats

**Climate change and security**:
- Query: `climate change as national security threat`
- Filters: Small Island Developing States (SIDS)
- Result: Segments showing climate threat framing in vulnerable nations

**Regional comparisons**:
- Query: `terrorism and non-state actors`
- Filters: Compare Asia vs Europe
- Result: Side-by-side comparison of terrorism threat construction

**Temporal analysis**:
- Query: `migration and border security`
- Filters: EU members, compare 2000–2010 vs 2011–2025
- Result: Evolution of migration security discourse

**No coding required**—just type queries and select filters in the interactive interface.

## Installation Time

- **Fast connection** (100 Mbps): 15–20 minutes
- **Standard connection** (25 Mbps): 30–45 minutes
- **Slow connection** (5 Mbps): 2–3 hours

The installer supports resume capability—if interrupted, simply re-run the notebook and downloads will continue from where they stopped.

## Disk Space Breakdown

| Component                           | Size  | Required? |
| ----------------------------------- | ----- | --------- |
| Model files (embeddings + segments) | 11.5 GB | Yes      |
| Metadata                            | 80 KB   | Yes      |
| Documentation files                 | 90 KB   | Yes      |
| Plain text documents                | 41 MB   | Optional |
| Sentence-segmented documents        | 44 MB   | Optional |
| PDF originals                       | 7 GB    | Optional |
| Original language documents         | 15 MB   | Optional |

**Minimum install**: 11.6 GB (semantic search only)
**With documents**: 11.7 GB
**Complete**: ~19 GB

## Dataset Information

**Coverage**: 660 documents from 118 countries, 1987–2025

**Document types**: National security strategies, defence white papers, strategic reviews

**Languages**: 80+ languages (primarily English + 20+ European languages)

**Segments**: 726,307 paragraph-level text segments with embeddings

**Encoding model**: sentence-transformers/all-mpnet-base-v2 (768-dimensional)

**DataShare repository**: https://datashare.ed.ac.uk (DOI assigned upon publication)

## Citation

If you use NSDDD v3 in research, please cite:

```bibtex
@dataset{neal_gardner_2026_nsddd_v3,
  author       = {Neal, Andrew W. and Gardner, Roy B.},
  title        = {National Security and Defence Documents Dataset (1987-2025) v3.0},
  year         = {2026},
  publisher    = {Edinburgh DataShare},
  institution  = {University of Edinburgh},
  note         = {660 national security strategy documents from 118 countries, 1987-2025, with MPNet embeddings. DOI available at https://datashare.ed.ac.uk}
}
```

Or in text form:

> Neal, A. W., & Gardner, R. B. (2026). National Security and Defence Documents Dataset (1987-2025) v3.0. University of Edinburgh. Edinburgh DataShare. https://datashare.ed.ac.uk

## Getting Started After Installation

After installation completes, open the **Document Metadata Search Tool**:

```bash
jupyter notebook document_metadata_search.ipynb
```

Run all cells in the notebook to:

1. Load the dataset (takes 90–120 seconds for 11 GB embedding file)
2. Launch the interactive search interface
3. Start searching with the widget-based interface—no coding required

The interface provides:

- **Text input** for search queries
- **Dropdown filters** for countries, regions, organizations, income groups, democracy status
- **Year range** selectors
- **Search and export buttons**
- **Results display** with similarity scores and document context

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
- See `WHATS_NEW_IN_NSDDD_V3.md` for comprehensive documentation
- Report issues on GitHub: https://github.com/andrewneal78/NSDDD_v3_installer/issues

## License

NSDDD v3 is licensed under Creative Commons Attribution 4.0 International (CC-BY 4.0).

The documents in NSDDD v3 are official government publications in the public domain.

See `LICENSE.txt` (included after installation) for full details.

## Support

For questions, issues, or feedback:

- **GitHub Issues**: https://github.com/andrewneal78/NSDDD_v3_installer/issues
- **Email**: andrew.neal@ed.ac.uk
- **Documentation**: See included documentation files
- **DataShare**: https://datashare.ed.ac.uk

## Dataset Versioning

- **NSDDD v3** (2026): Fresh MPNet-based encodings, complete reorganisation
- **NSDDD v2** (2023): Previous version with USE-4 embeddings
- **NSDDD v1** (2022): Initial release

See `WHATS_NEW_IN_NSDDD_V3.md` (included after installation) for complete version comparison and improvements.

## References

**Complete documentation**: See `WHATS_NEW_IN_NSDDD_V3.md` (included after installation)

**Dataset methodology**: See `dataset_inclusion_criteria.md` (included after installation)

**Citation formats**: See `CITATION.txt` (included after installation)

**License**: See `LICENSE.txt` (included after installation)

---

**Happy researching!** 🔍

For information about Edinburgh DataShare and the full dataset: [datashare.ed.ac.uk](https://datashare.ed.ac.uk)
