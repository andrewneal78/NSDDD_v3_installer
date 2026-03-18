NSDDD v3 Installer
==================

Official installer for the National Security Documents Dataset (NSDDD) version 3.

NSDDD v3 is a corpus of 660 national security strategy documents from 118 countries
spanning 1987-2025, with 726,307 pre-computed semantic embeddings enabling local
semantic search without API keys or internet connection.


------------------------------------------------------------------------
BEFORE YOU START
------------------------------------------------------------------------

The installer runs inside Jupyter Notebook, which requires Python to be
installed on your computer. If you are not sure whether you have Python or
Jupyter, follow the steps below. If you already have Python 3.9+ and
Jupyter, skip to the INSTALLATION section.


Do you have Python?
-------------------

Open a terminal and type:

    python --version

or

    python3 --version

  - macOS: open the Terminal app (search for "Terminal" in Spotlight)
  - Windows: open Command Prompt or PowerShell (search in the Start menu)

If you see "Python 3.9" or higher, you have Python.
If you see an error or a version below 3.9, you need to install it.


Getting Python and Jupyter
--------------------------

Option A -- Anaconda (recommended for most researchers)

Anaconda installs Python, Jupyter, and all common scientific packages in
one step. No terminal expertise required after installation.

  1. Download Anaconda from:  https://www.anaconda.com/download
  2. Run the installer and follow the on-screen instructions
  3. Open Anaconda Navigator and launch Jupyter Notebook from there

This is the easiest option if you are new to Python.


Option B -- Python from python.org (minimal install)

  1. Download Python from:  https://www.python.org/downloads/
     Choose Python 3.11 or newer.
  2. Run the installer.
     On Windows: tick "Add Python to PATH" before clicking Install.
  3. Open a terminal and run:

         pip install notebook


Do you have git?
----------------

The installer files are on GitHub. The easiest way to get them is with git.
To check, open a terminal and type:

    git --version

If git is not installed, you have two options:

  - Install git from:  https://git-scm.com/downloads
    (Straightforward installer for all platforms.)

  - Download without git:
    Go to:  https://github.com/andrewneal78/NSDDD_v3_installer
    Click the green "Code" button, then "Download ZIP".
    Extract the ZIP file before proceeding.


------------------------------------------------------------------------
INSTALLATION
------------------------------------------------------------------------

Step 1 -- Get the installer files
----------------------------------

With git (open a terminal and run):

    git clone https://github.com/andrewneal78/NSDDD_v3_installer.git
    cd NSDDD_v3_installer

Without git: extract the downloaded ZIP and open the folder.


Step 2 -- Open the installer notebook
--------------------------------------

If you installed Anaconda:
  Open Anaconda Navigator, launch Jupyter Notebook, navigate to the
  NSDDD_v3_installer folder, and open INSTALL_NSDDD_v3.ipynb.

If you installed Python from python.org:
  Open a terminal in the NSDDD_v3_installer folder and run:

      jupyter notebook INSTALL_NSDDD_v3.ipynb


Step 3 -- Follow the notebook instructions
-------------------------------------------

The installer will guide you through each step. You do not need to write
any code -- just run cells and respond to prompts. The installer will:

  - Check your system requirements
  - Set up an isolated Python environment for NSDDD (recommended)
  - Download NSDDD v3 files from Edinburgh DataShare (4-15 GB)
  - Extract files to the correct directory structure
  - Verify file integrity
  - Test model loading
  - Show you how to open the Document Search notebook

Total time: 20-45 minutes depending on internet speed.


------------------------------------------------------------------------
SYSTEM REQUIREMENTS
------------------------------------------------------------------------

                  Minimum         Recommended
  Python          3.9             3.11+
  Disk space      15 GB           20 GB
  RAM             8 GB            16 GB
  Internet        For download    For download only

The semantic search model file is 11 GB. 16 GB RAM is recommended to avoid
memory pressure. All searches run locally -- no internet needed after install.


------------------------------------------------------------------------
WHAT GETS INSTALLED?
------------------------------------------------------------------------

After installation, you will have:

  - Interactive search notebook: widget-based interface, no coding required
  - 660 national security documents from 118 countries (1987-2025)
  - 726,307 pre-computed MPNet embeddings (768-dimensional vectors)
  - Complete metadata: countries, years, document types, organisations
  - Semantic search: search security concepts across all documents locally
  - Advanced filtering: by country, region, organisation, income group,
    democracy status, and year
  - Documentation: complete methodology and usage guide


------------------------------------------------------------------------
USING THE DOCUMENT SEARCH NOTEBOOK
------------------------------------------------------------------------

After installation, open document_metadata_search.ipynb. The installer
will show you exactly how to do this, but in brief:

  - If you set up a virtual environment during installation:
    Open the notebook in Jupyter and select:
    Kernel > Change kernel > NSDDD v3

  - If you used Anaconda or an existing environment:
    Open the notebook normally.

The notebook provides an interactive widget interface:

  1. Run all cells to load the dataset and launch the search interface
  2. Enter search queries in the text box
     (e.g. "cyber threats to critical infrastructure")
  3. Select filters using dropdown menus:
       - Countries (single or multiple)
       - UN Regions (Asia, Europe, Africa, Americas, Oceania)
       - Organisations (NATO, EU, ASEAN, BRICS, Commonwealth, G7, G20...)
       - Income groups (High, Upper-middle, Lower-middle, Low)
       - Democracy status (Free, Partly Free, Not Free)
       - Years (1987-2025)
  4. Click Search to find matching document segments
  5. Export results to CSV if needed


Example searches
----------------

Cyber security threats:
  Query:   "cyber threats to critical infrastructure"
  Filters: NATO members, 2020-2025

Climate change and security:
  Query:   "climate change as national security threat"
  Filters: Small Island Developing States (SIDS)

Regional comparisons:
  Query:   "terrorism and non-state actors"
  Filters: Compare Asia vs Europe

Temporal analysis:
  Query:   "migration and border security"
  Filters: EU members, compare 2000-2010 vs 2011-2025


------------------------------------------------------------------------
RUNNING THE SEARCH INTERFACE
------------------------------------------------------------------------

Once installed, you can launch the document search interface as a
standalone app — no Jupyter cells visible:

    python launch.py

This opens a browser window with the full search interface.
You can also open document_metadata_search.ipynb directly in Jupyter
as before.

To stop the server, press Ctrl+C in the terminal.


------------------------------------------------------------------------
DISK SPACE BREAKDOWN
------------------------------------------------------------------------

  Component                            Size      Required?
  -----------------------------------  --------  ----------
  Model files (embeddings + segments)  11.5 GB   Yes
  Metadata                             80 KB     Yes
  Documentation files                  90 KB     Yes
  Plain text documents                 41 MB     Optional
  Sentence-segmented documents         44 MB     Optional
  PDF originals                        7 GB      Optional
  Original language documents          15 MB     Optional

  Minimum install:   11.6 GB (semantic search only)
  With documents:    11.7 GB
  Complete:         ~19 GB


------------------------------------------------------------------------
TROUBLESHOOTING
------------------------------------------------------------------------

"python" or "pip" command not found
  - On macOS/Linux, try "python3" and "pip3" instead
  - If neither works, Python is not installed -- see "Getting Python and
    Jupyter" above

"jupyter" command not found
  - Run:  pip install notebook  (or  pip3 install notebook)
  - If using Anaconda, launch Jupyter from Anaconda Navigator instead

Permission error when installing packages
  - On macOS/Linux, try:  pip install --user notebook
  - Or use Anaconda, which avoids system permission issues entirely

"FileNotFoundError" during installation
  - Check your internet connection
  - Verify Edinburgh DataShare is accessible: https://datashare.ed.ac.uk
  - Re-run the installer cell -- it supports resuming interrupted downloads

Insufficient disk space
  - You need at least 15 GB free
  - Skip the optional PDF set during installation (saves 7 GB)

Memory error when loading the model
  - You need at least 8 GB RAM; 16 GB recommended
  - Close other applications and try again

Other issues
  - See WHATS_NEW_IN_NSDDD_V3.md (included after installation)
  - Report issues: https://github.com/andrewneal78/NSDDD_v3_installer/issues


------------------------------------------------------------------------
INSTALLATION TIME
------------------------------------------------------------------------

  Fast connection (100 Mbps):    15-20 minutes
  Standard connection (25 Mbps): 30-45 minutes
  Slow connection (5 Mbps):      2-3 hours

The installer supports resume -- if interrupted, re-run the notebook cell
and downloads will continue from where they stopped.


------------------------------------------------------------------------
DATASET INFORMATION
------------------------------------------------------------------------

  Coverage:         660 documents from 118 countries, 1987-2025
  Document types:   National security strategies, defence white papers,
                    strategic reviews
  Languages:        80+ languages (primarily English + 20+ European)
  Segments:         726,307 paragraph-level text segments with embeddings
  Encoding model:   sentence-transformers/all-mpnet-base-v2 (768-dim)
  DataShare:        https://datashare.ed.ac.uk/handle/10283/9156


------------------------------------------------------------------------
CITATION
------------------------------------------------------------------------

If you use NSDDD v3 in research, please cite:

  Neal, A. W., & Gardner, R. B. (2026). National Security and Defence
  Documents Dataset (1987-2025) v3.0. University of Edinburgh.
  Edinburgh DataShare. https://datashare.ed.ac.uk/handle/10283/9156

BibTeX:

  @dataset{neal_gardner_2026_nsddd_v3,
    author      = {Neal, Andrew W. and Gardner, Roy B.},
    title       = {National Security and Defence Documents Dataset
                   (1987-2025) v3.0},
    year        = {2026},
    publisher   = {Edinburgh DataShare},
    institution = {University of Edinburgh},
    url         = {https://datashare.ed.ac.uk/handle/10283/9156}
  }


------------------------------------------------------------------------
DATASET VERSIONING
------------------------------------------------------------------------

  NSDDD v3 (2026): Fresh MPNet-based encodings, complete reorganisation
  NSDDD v2 (2023): Previous version with USE-4 embeddings
  NSDDD v1 (2022): Initial release

See WHATS_NEW_IN_NSDDD_V3.md for complete version history and changes.


------------------------------------------------------------------------
LICENSE
------------------------------------------------------------------------

NSDDD v3 is licensed under Creative Commons Attribution 4.0 International
(CC-BY 4.0). The documents in NSDDD v3 are official government publications
in the public domain. See LICENSE.txt for full details.


------------------------------------------------------------------------
SUPPORT
------------------------------------------------------------------------

  GitHub Issues:  https://github.com/andrewneal78/NSDDD_v3_installer/issues
  Email:          andrew.neal@ed.ac.uk
  DataShare:      https://datashare.ed.ac.uk

------------------------------------------------------------------------
