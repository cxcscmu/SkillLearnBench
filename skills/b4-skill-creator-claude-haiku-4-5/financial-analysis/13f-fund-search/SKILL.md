---
name: 13f-fund-search
description: Search for hedge funds in SEC 13F filings by fuzzy name matching. Use this skill whenever you need to find a fund's accession number by name (e.g., "Renaissance Technologies", "Berkshire Hathaway"). Returns accession_number to use with fund analysis.
---

# 13F Fund Search Skill

## Overview

This skill enables searching the SEC 13F COVERPAGE data to locate specific hedge funds by name, returning their accession numbers needed for detailed analysis.

## When to Use

Use this skill whenever you need to:
- Find a fund's accession number by its name
- Locate multiple funds (e.g., Q2 and Q3 versions of the same fund)
- Verify fund names and get their correct identifiers

## Data Location

The 13F filings are stored in:
- `/root/2025-q2/` - Q2 2025 13F filings
- `/root/2025-q3/` - Q3 2025 13F filings

Each quarter folder contains subdirectories with COVERPAGE files containing fund metadata.

## Search Process

### Step 1: Explore Directory Structure
```bash
ls -la /root/2025-q2/
ls -la /root/2025-q3/
```

Look for CSV or JSON files containing COVERPAGE information. These typically contain:
- Fund name
- Accession number
- Filing date
- CIK (Central Index Key)

### Step 2: Fuzzy Search Implementation

For searching funds by name, use Python with fuzzy matching:

```python
import os
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def search_fund_in_quarter(quarter_path, search_term, threshold=80):
    """
    Search for fund by fuzzy name matching in a specific quarter.

    Args:
        quarter_path: Path to quarter data (e.g., '/root/2025-q2/')
        search_term: Fund name to search (e.g., 'Renaissance Technologies')
        threshold: Fuzzy match threshold (0-100)

    Returns:
        Dictionary with best matches containing fund name and accession_number
    """
    # Find COVERPAGE files
    results = []
    for root, dirs, files in os.walk(quarter_path):
        for file in files:
            if 'COVERPAGE' in file and (file.endswith('.csv') or file.endswith('.json')):
                file_path = os.path.join(root, file)
                try:
                    if file.endswith('.csv'):
                        df = pd.read_csv(file_path)
                    else:
                        df = pd.read_json(file_path)

                    # Look for name column (may be named differently)
                    name_col = None
                    for col in df.columns:
                        if 'name' in col.lower() or 'fund' in col.lower():
                            name_col = col
                            break

                    if name_col is None:
                        continue

                    # Fuzzy search
                    for idx, row in df.iterrows():
                        fund_name = str(row[name_col])
                        score = fuzz.token_sort_ratio(search_term.lower(), fund_name.lower())

                        if score >= threshold:
                            accession = row.get('accession_number') or row.get('ACCESSION') or row.get('accession')
                            results.append({
                                'fund_name': fund_name,
                                'accession_number': accession,
                                'match_score': score
                            })
                except Exception as e:
                    continue

    # Sort by match score
    results.sort(key=lambda x: x['match_score'], reverse=True)
    return results

# Usage
q2_results = search_fund_in_quarter('/root/2025-q2/', 'Renaissance Technologies')
q3_results = search_fund_in_quarter('/root/2025-q3/', 'Renaissance Technologies')

if q2_results:
    print(f"Q2 Match: {q2_results[0]}")
if q3_results:
    print(f"Q3 Match: {q3_results[0]}")
```

## Output Format

Returns a list of matches sorted by fuzzy match score:
```json
{
    "fund_name": "Renaissance Technologies",
    "accession_number": "0001234567-25-000123",
    "match_score": 95
}
```

Use the `accession_number` with the 13f-fund-analysis skill.

## Common Fund Names to Search

- "Renaissance Technologies" (Jim Simons)
- "Berkshire Hathaway" (Warren Buffett)
- Full names or abbreviated versions both work

## Tips

- Use token_sort_ratio from fuzzywuzzy for name variations
- Set threshold around 80-90 for good precision
- Multiple results indicate possible matches—use the highest score
- If searching for Q2 and Q3, run separately as accession numbers will differ
