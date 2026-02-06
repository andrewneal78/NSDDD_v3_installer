# Setting Up NSDDD v3 Installer on GitHub

## Prerequisites

Before publishing to GitHub, you need:

1. ✓ Installer files ready (all present and verified)
2. ⏳ Dataset uploaded to Edinburgh DataShare
3. ⏳ DataShare handle/DOI obtained

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository settings:
   - **Name**: `NSDDD_v3_installer`
   - **Description**: 'Official installer for the National Security Documents Dataset (NSDDD) version 3 - 660 documents from 118 countries with semantic search'
   - **Visibility**: Public
   - **Initialize**: Do NOT add README, .gitignore, or license (we already have these)

3. Click 'Create repository'

## Step 2: Add Remote and Push

From the installer directory:

```bash
cd "/Users/aneal/Library/CloudStorage/OneDrive-UniversityofEdinburgh/national_security_analysis/NSDDD_v3/NSDDD_v3_installer"

# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/NSDDD_v3_installer.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Update config.py with DataShare Handle

After uploading your dataset to Edinburgh DataShare:

1. Obtain the DataShare handle (format: `10283/XXXXX`)
2. Update `config.py`:

```python
# Replace this line:
DATASHARE_HANDLE = '[HANDLE_TO_BE_ADDED]'

# With your actual handle:
DATASHARE_HANDLE = '10283/XXXXX'  # Your actual handle
```

3. Commit and push:

```bash
git add config.py
git commit -m "Add DataShare handle for dataset access"
git push
```

## Step 4: Test the Installer

Before announcing publicly:

1. Clone your repository to a fresh location:
   ```bash
   cd /tmp
   git clone https://github.com/YOUR_USERNAME/NSDDD_v3_installer.git
   cd NSDDD_v3_installer
   ```

2. Install Jupyter:
   ```bash
   pip install notebook
   ```

3. Open installer:
   ```bash
   jupyter notebook INSTALL_NSDDD_v3.ipynb
   ```

4. Run through all cells and verify:
   - Download works from DataShare
   - Checksums verify correctly
   - Model files load successfully
   - Search interface works

## Step 5: Add Repository Metadata

On GitHub repository page:

1. **Topics**: Add tags like `dataset`, `national-security`, `semantic-search`, `research-data`, `mpnet`, `python`, `jupyter-notebook`

2. **About section**: Add description and website (if you have a project page)

3. **Releases**: Create first release (v3.0.0) with release notes describing the dataset

## Step 6: Update Main Repository

In your main research repository (`ns_codebase_mpnet`):

1. Update `README.md` to add link to installer:

```markdown
## NSDDD v3 Dataset Access

The NSDDD v3 dataset is available through Edinburgh DataShare.

**Quick Start**: Use the [NSDDD v3 Installer](https://github.com/YOUR_USERNAME/NSDDD_v3_installer) to download and set up the dataset with semantic search capability.

- 📊 Dataset on DataShare: [DOI link]
- 🛠 Installation tool: [GitHub link]
- 📖 Documentation: [SEMANTIC_SEARCH_GUIDE.md](SEMANTIC_SEARCH_GUIDE.md)
```

## Optional: Create GitHub Pages Documentation

You can create a nice landing page:

1. In repository settings, enable GitHub Pages
2. Choose source: main branch, /docs folder (or root)
3. Create a simple landing page highlighting:
   - What NSDDD v3 is
   - Installation instructions
   - Citation information
   - Example searches

## Files Included in Repository

✓ Essential installer files:
- `INSTALL_NSDDD_v3.ipynb` - Main installer notebook
- `document_metadata_search.ipynb` - Search interface
- `README.md` - GitHub landing page
- `requirements.txt` - Python dependencies
- `config.py` - DataShare configuration
- `utils/` - Helper utilities
- `.gitignore` - Excludes downloads and generated files

✗ NOT included (gitignored):
- `.jupyter_ystore.db` - Jupyter state database
- `VERIFY.ipynb` - Test output
- `NSDDD_v3_workspace/` - User installation directory
- Downloaded zip files

## Maintenance

After publication:

1. **Monitor issues**: Respond to user questions/problems on GitHub Issues
2. **Update documentation**: Improve README based on user feedback
3. **Version releases**: Tag releases for any installer updates
4. **Citation tracking**: Update citation information if paper published

## Checklist Before Going Public

- [ ] Dataset uploaded to Edinburgh DataShare
- [ ] DataShare handle added to config.py
- [ ] Installer tested on fresh system
- [ ] All documentation reviewed for accuracy
- [ ] Citation information complete
- [ ] License file present and correct
- [ ] Contact information current
- [ ] Repository topics/tags added

## Support

Users should report issues at: `https://github.com/YOUR_USERNAME/NSDDD_v3_installer/issues`
