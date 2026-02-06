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
git clone https://github.com/andrewneal78/NSDDD_v3_installer.git
cd NSDDD_v3_installer
```

**2. Install Jupyter (if not already installed):**

Minimal option (recommended):
```bash
pip install notebook
```

Or with JupyterLab (larger but better interface):
```bash
pip install jupyterlab
```

**3. Open the installer notebook:**

```bash
# If you installed notebook:
jupyter notebook INSTALL_NSDDD_v3.ipynb

# If you installed jupyterlab:
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

All examples use Python code. See `GETTING_STARTED.ipynb` for complete working examples.

**Semantic search for cyber threats**:
```python
from scipy.spatial.distance import cosine

query = 'cyber threats to critical infrastructure'
query_vector = encoder.encode([query])[0]

results = []
for i, segment_vector in enumerate(segment_encodings):
    similarity = 1 - cosine(query_vector, segment_vector)
    if similarity >= 0.7:  # Similarity threshold
        results.append((encoded_segments[i], similarity))

# Returns: 45 matching segments from 12 countries
```

**Filter by country and year**:
```python
import pandas as pd

metadata = pd.read_csv('metadata/document_metadata.csv')

# Find climate security discussions in European documents after 2020
eu_docs = metadata[(metadata['Region'] == 'Europe') &
                   (metadata['Year'] >= 2020)]

# Search only within these documents
filtered_results = [r for r in results
                   if get_document_id(r[0]) in eu_docs['ID'].values]
```

**Cluster similar segments**:
```python
import networkx as nx

# Build similarity graph
G = nx.Graph()
for i, (seg1, score1) in enumerate(results):
    for j, (seg2, score2) in enumerate(results[i+1:], i+1):
        if cosine_similarity(seg1, seg2) >= 0.78:
            G.add_edge(i, j)

# Find clusters
clusters = list(nx.connected_components(G))
# Returns: 12 distinct threat framings across documents
```

**Extract and analyse segments**:
```python
# Get full text for segments
for segment_id, similarity in results[:10]:
    doc_id, seg_num = segment_id.split('/')
    text = segments_dict[doc_id][int(seg_num)]['text']
    country = documents_dict[doc_id]['country']
    year = documents_dict[doc_id]['year']

    print(f'{country} ({year}): {text[:100]}...')
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
