# NSDDD v3 — National Security Documents Search

Local semantic search across the National Security and Defence Documents Dataset (NSDDD) v3: **660 national security strategy documents from 118 countries, 1987–2025**, with 726,307 pre-computed text segment embeddings.

Search by concept, filter by country, region, organisation, year, and more — entirely offline after installation.

---

## Requirements

| | Minimum | Recommended |
|---|---|---|
| Python | 3.9 | 3.11+ |
| Disk space | 15 GB | 20 GB |
| RAM | 8 GB | 16 GB |

---

## Installation

### Before you start

**Opening a terminal:**
- **Mac:** press `Cmd + Space`, type `Terminal`, press Enter
- **Windows:** press `Win + R`, type `cmd`, press Enter

**Do you have Python 3.9+?**
Most Macs do. Windows usually does not. To check, open a terminal and type:

```
python3 --version
```

If you see `Python 3.9` or higher, you're ready. If not (or if the command isn't found), install Python from https://www.python.org/downloads/ — on Windows, tick **Add Python to PATH** during install.

---

### Step 1 — Download the installer

Click the green **Code** button on this page, then **Download ZIP**. Extract the ZIP — you'll get a folder called `NSDDD_v3_installer`.

---

### Step 2 — Open a terminal in that folder

- **Mac:** press `Cmd + Space`, type `Terminal`, press Enter — then type `cd ` (with a space), drag the `NSDDD_v3_installer` folder into the Terminal window, and press Enter
- **Windows:** open the `NSDDD_v3_installer` folder in File Explorer, click the address bar at the top, type `cmd`, press Enter

---

### Step 3 — Run the installer

```bash
python3 install.py
```

The installer will walk you through:

- Setting up an isolated Python environment (nothing changed system-wide)
- Downloading dataset files from Edinburgh DataShare (~5 GB) and the sentence encoder from HuggingFace (~420 MB)
- Installing Python dependencies

**Estimated time: 20–45 minutes** depending on internet speed. Downloads can be interrupted and resumed.

---

### Step 4 — Launch

| Platform | How |
|---|---|
| **Mac** | Double-click `Launch.command` in the installer folder |
| **Windows** | Double-click `Launch.vbs` in the installer folder |
| **Terminal** | `python3 launch.py` |

Your browser opens at `http://localhost:8867`. The search interface loads automatically.

> On startup, the launcher checks for installer updates before opening the interface.

> The browser may briefly show “server not found” for a few seconds while Voilà starts.

---

## Automatic updates

The launcher checks for updates each time you start:

- **Git installs (cloned repo):** `git fetch` + fast-forward pull from `origin/main` when newer.
- **Download/ZIP installs:** compares local `VERSION` with GitHub `VERSION`; if newer, downloads and overlays latest installer files while preserving local data folders (`NSDDD_v3_workspace`, `outputs`, `.venv`, etc.).

After applying an update, the launcher restarts automatically.

Disable auto-update for a single run:

```bash
python3 launch.py --no-update
```

Disable auto-update via environment variable:

```bash
NSDDD_AUTO_UPDATE=0 python3 launch.py
```

---

## Search Interface

The browser-based interface provides:

**Two search modes:**
- **Semantic search** — AI-powered conceptual matching (finds documents about an idea, not just exact words)
- **Keyword search** — regex-based, with optional Boolean operators (AND, OR, NOT) and fuzzy matching

**Filters:**
- Country (all 118, individually selectable)
- UN region and subregion
- International organisations (NATO, EU, ASEAN, AU, G7, G20, BRICS, Commonwealth, and more)
- Income group (World Bank classification)
- Democracy status (Freedom House)
- Document type (national security strategy, defence white paper, strategic review)
- Year range (1987–2025)
- Most recent document per country only

**Output:**
- Results grouped into semantic clusters with auto-generated labels
- Export to CSV
- Visualisations: results by year, top countries, cluster overview

---

## Dataset

| | |
|---|---|
| Documents | 660 |
| Countries | 118 |
| Coverage | 1987–2025 |
| Segments | 726,307 sentence-level |
| Embedding model | `all-mpnet-base-v2` (768-dimensional) |
| Languages | English + translations for 80+ countries |
| DataShare | https://datashare.ed.ac.uk/handle/10283/9156 |

Document types included: national security strategies (NSS), defence white papers (WP), defence and security reviews (DD), and treaty/alignment documents (TA).

---

## Advanced Use

For scripting, custom analysis, or direct access to the notebook:

```bash
jupyter notebook document_metadata_search.ipynb
```

This is the same interface without the browser launcher. Use it if you want to modify the search logic, access results programmatically, or integrate with other notebooks.

To verify your installation or diagnose issues, run:

```bash
jupyter notebook VERIFY.ipynb
```

---

## Citation

If you use NSDDD v3 in research, please cite:

> Neal, A. W., & Gardner, R. B. (2026). *National Security and Defence Documents Dataset (1987–2025) v3.0*. University of Edinburgh. Edinburgh DataShare. https://datashare.ed.ac.uk/handle/10283/9156

```bibtex
@dataset{neal_gardner_2026_nsddd_v3,
  author      = {Neal, Andrew W. and Gardner, Roy B.},
  title       = {National Security and Defence Documents Dataset (1987--2025) v3.0},
  year        = {2026},
  publisher   = {Edinburgh DataShare},
  institution = {University of Edinburgh},
  url         = {https://datashare.ed.ac.uk/handle/10283/9156}
}
```

---

## Troubleshooting

**`python3` not found**
Install Python 3.9+ from https://www.python.org/downloads/ (tick "Add to PATH" on Windows).

**Loading message doesn't clear / interface doesn't appear**
Wait briefly after launch. The server can take a few seconds to start. If needed, close the tab, wait 10 seconds, and reopen `http://localhost:8867`.

**Multiple browser tabs open / interface freezes**
Each launch starts a fresh server; old sessions are stopped automatically. If you experience freezing, close all browser tabs, wait 10 seconds, and reopen `http://localhost:8867`.

**FileNotFoundError during installation**
Check your internet connection. Re-run `python3 install.py` — downloads resume automatically.

**Memory error when loading**
Close other applications. 16 GB RAM recommended for comfortable use.

**Other issues**
Open an issue at https://github.com/andrewneal78/NSDDD_v3_installer/issues or email andrew.neal@ed.ac.uk

---

## License

The installer code (this repository) is released under the **MIT License**.
The NSDDD v3 dataset is released under **CC-BY 4.0**.
The documents in NSDDD v3 are official government publications in the public domain.
