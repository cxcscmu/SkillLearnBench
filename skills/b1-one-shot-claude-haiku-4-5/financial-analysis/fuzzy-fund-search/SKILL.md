---
name: fuzzy-fund-search
description: Fuzzy matching techniques for finding hedge funds by name when exact names are unknown
---

# Fuzzy Name Search for Hedge Funds

## Overview
Fund names in the COVERPAGE.tsv may not match exactly what you're searching for. Fuzzy matching helps find the best match when you have approximate or partial names.

## Libraries

### Using fuzzywuzzy
```bash
pip install fuzzywuzzy python-Levenshtein
```

### Using difflib (built-in)
No installation needed - Python standard library

## Search Methods

### Method 1: Using fuzzywuzzy (Recommended)

```python
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd

def fuzzy_search_fund(search_term, coverpage_df, threshold=70):
    """
    Find funds matching a search term using fuzzy matching

    Args:
        search_term: Partial or approximate fund name (e.g., "renaissance technologies")
        coverpage_df: DataFrame from COVERPAGE.tsv
        threshold: Minimum match score (0-100)

    Returns:
        DataFrame of matches sorted by score (highest first)
    """

    fund_names = coverpage_df['FILINGMANAGER_NAME'].tolist()

    # Use extractBests to get multiple matches
    matches = process.extractBests(
        search_term,
        fund_names,
        scorer=fuzz.token_sort_ratio,  # Good for finding partial matches
        score_cutoff=threshold
    )

    # Build result dataframe
    results = []
    for matched_name, score in matches:
        fund_row = coverpage_df[coverpage_df['FILINGMANAGER_NAME'] == matched_name].iloc[0]
        results.append({
            'FILINGMANAGER_NAME': matched_name,
            'ACCESSION_NUMBER': fund_row['ACCESSION_NUMBER'],
            'match_score': score,
            'REPORTCALENDARORQUARTER': fund_row['REPORTCALENDARORQUARTER']
        })

    return pd.DataFrame(results).sort_values('match_score', ascending=False)

# Usage Example
q3_coverpage = pd.read_csv('/root/2025-q3/COVERPAGE.tsv', sep='\t')
matches = fuzzy_search_fund("renaissance technologies", q3_coverpage, threshold=70)
print(matches.head())

# Get best match
best_match = matches.iloc[0]
accession_number = best_match['ACCESSION_NUMBER']
fund_name = best_match['FILINGMANAGER_NAME']
```

### Method 2: Using difflib (Built-in)

```python
from difflib import SequenceMatcher
import pandas as pd

def simple_fuzzy_search(search_term, coverpage_df, threshold=0.6):
    """
    Simple fuzzy search using difflib (no external dependencies)
    """
    search_term_lower = search_term.lower()
    fund_names = coverpage_df['FILINGMANAGER_NAME'].tolist()

    matches = []
    for name in fund_names:
        similarity = SequenceMatcher(None, search_term_lower, name.lower()).ratio()
        if similarity >= threshold:
            fund_row = coverpage_df[coverpage_df['FILINGMANAGER_NAME'] == name].iloc[0]
            matches.append({
                'FILINGMANAGER_NAME': name,
                'ACCESSION_NUMBER': fund_row['ACCESSION_NUMBER'],
                'similarity': similarity
            })

    return pd.DataFrame(matches).sort_values('similarity', ascending=False)
```

### Method 3: Partial String Matching (Simple)

```python
def substring_search(search_term, coverpage_df, case_sensitive=False):
    """
    Simple substring matching (works for known partial names)
    """
    if case_sensitive:
        matches = coverpage_df[coverpage_df['FILINGMANAGER_NAME'].str.contains(search_term, na=False)]
    else:
        matches = coverpage_df[coverpage_df['FILINGMANAGER_NAME'].str.contains(
            search_term, case=False, na=False
        )]

    return matches[['FILINGMANAGER_NAME', 'ACCESSION_NUMBER']]
```

## Matching Algorithms Comparison

| Algorithm | Use Case | Pros | Cons |
|-----------|----------|------|------|
| `token_sort_ratio` | Handles reordered words | "technologies renaissance" ≈ "renaissance technologies" | Slower |
| `token_set_ratio` | Handles subset words | "Renaissance Tech" ≈ "Renaissance Technologies" | Slower |
| `fuzz.ratio` | Exact character match | Fast, simple | Sensitive to word order |
| `SequenceMatcher` | Quick approximate match | Built-in, no deps | Less sophisticated |
| Substring match | Known partial names | Fastest | Only works with exact substrings |

## Best Practices

### 1. Start with a Reasonable Threshold
```python
# For very fuzzy matches
matches = fuzzy_search_fund("berkshire", coverpage_df, threshold=50)

# For tighter matches
matches = fuzzy_search_fund("berkshire hathaway", coverpage_df, threshold=80)
```

### 2. Clean Search Terms
```python
def clean_search_term(term):
    """Remove extra whitespace and punctuation"""
    return ' '.join(term.lower().strip().split())

search = clean_search_term("  RENAISSANCE TECHNOLOGIES  ")
# Result: "renaissance technologies"
```

### 3. Validate Top Match
```python
matches = fuzzy_search_fund("warren buffett", coverpage_df)

if len(matches) > 0:
    best = matches.iloc[0]
    print(f"Found: {best['FILINGMANAGER_NAME']}")
    print(f"Match Score: {best['match_score']}")
    print(f"Accession: {best['ACCESSION_NUMBER']}")

    # Manual verification
    assert 'berkshire' in best['FILINGMANAGER_NAME'].lower(), "Match doesn't contain expected keyword"
else:
    print("No matches found")
```

## Common Search Patterns

```python
# Search for famous fund managers
q3_data = pd.read_csv('/root/2025-q3/COVERPAGE.tsv', sep='\t')

# Renaissance Technologies (Jim Simons)
renaissance = fuzzy_search_fund("renaissance technologies", q3_data)

# Berkshire Hathaway (Warren Buffett)
berkshire = fuzzy_search_fund("berkshire hathaway", q3_data)

# Citadel
citadel = fuzzy_search_fund("citadel", q3_data)

# Tiger Global
tiger = fuzzy_search_fund("tiger global", q3_data)
```

## Example: Complete Fund Lookup Workflow

```python
import pandas as pd
from fuzzywuzzy import process, fuzz

def find_and_verify_fund(search_term, coverpage_df, expected_keywords=None):
    """
    Find a fund and verify the match
    """
    # Fuzzy search
    fund_names = coverpage_df['FILINGMANAGER_NAME'].tolist()
    matches = process.extractBests(
        search_term,
        fund_names,
        scorer=fuzz.token_sort_ratio,
        score_cutoff=70,
        limit=3
    )

    # Verify with expected keywords
    for matched_name, score in matches:
        if expected_keywords is None or all(
            keyword.lower() in matched_name.lower()
            for keyword in expected_keywords
        ):
            fund_row = coverpage_df[
                coverpage_df['FILINGMANAGER_NAME'] == matched_name
            ].iloc[0]
            return {
                'fund_name': matched_name,
                'accession_number': fund_row['ACCESSION_NUMBER'],
                'quarter': fund_row['REPORTCALENDARORQUARTER'],
                'match_score': score
            }

    return None

# Usage
result = find_and_verify_fund(
    "renaissance",
    q3_data,
    expected_keywords=['renaissance', 'tech']
)
```

## Troubleshooting

### No Matches Found
- Lower the threshold: `threshold=50` instead of `80`
- Try simpler search terms: "Renaissance" instead of "Renaissance Technologies"
- Check if fund exists in data: `coverpage_df['FILINGMANAGER_NAME'].str.contains(partial_name, case=False).any()`

### Too Many Matches
- Increase threshold: `threshold=85` instead of `70`
- Add more specific keywords: "berkshire hathaway" instead of "berkshire"

### Wrong Match Selected
- Manually inspect top matches before using
- Add validation keywords to filter results
- Use `limit=5` to get multiple options and review manually
