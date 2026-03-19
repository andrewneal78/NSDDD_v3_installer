"""
Country lookup utilities for NSDDD v3.

Provides access to country data from the installed dataset.
"""

import json
from pathlib import Path
from typing import List, Optional, Tuple


class CountryLookup:
    """
    Lookup country information from countries_dict.json.

    Resolves the data file from:
    1. Explicit data_path argument
    2. NSDDD_v3_workspace/model/countries_dict.json (relative to cwd)
    Falls back gracefully with empty data if not found.
    """

    def __init__(self, data_path: Optional[str] = None):
        self._data = {}

        if data_path is not None:
            candidate = Path(data_path)
        else:
            candidate = Path('NSDDD_v3_workspace/model/countries_dict.json')

        if candidate.exists():
            try:
                with open(candidate, 'r', encoding='utf-8') as f:
                    self._data = json.load(f)
            except Exception:
                self._data = {}

    def list_all_countries(self, show_region: bool = False) -> List[Tuple]:
        """
        Return a list of (num, iso_alpha3, country_name, region) tuples,
        sorted alphabetically by country name, numbered from 1.
        The show_region parameter is accepted for compatibility but region
        is always included as the fourth element.
        """
        entries = []
        for iso_alpha3, info in self._data.items():
            country_name = info.get('country', iso_alpha3)
            region = info.get('unsd_region', '')
            entries.append((iso_alpha3, country_name, region))

        entries.sort(key=lambda x: x[1])

        return [(i + 1, iso, name, region) for i, (iso, name, region) in enumerate(entries)]
