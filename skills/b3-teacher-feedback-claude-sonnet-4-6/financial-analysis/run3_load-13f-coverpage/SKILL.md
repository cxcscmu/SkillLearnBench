---
name: load-13f-coverpage
description: Load and search the COVERPAGE parquet file for a specific fund manager using fuzzy matching on the FILINGMANAGER_NAME field. Returns the best matching row including accession_number, AUM, and other fund details. Use this when you need to find a fund's accession number by name.
---

## Load 13F Cover Page and Fuzzy Search

```python
import pandas as pd
from pathlib import Path

def load_coverpage(quarter: str) -> pd.DataFrame:
    """Load COVERPAGE parquet for a given quarter ('q2' or 'q3')"""
    base = Path(f"/root/2025-{quarter}")
    # Try common file names
    for fname in ["COVERPAGE.parquet", "coverpage.parquet", "COVERPAGE.csv", "coverpage.csv"]:
        fpath = base / fname
        if fpath.exists():
            if fname.endswith(".parquet"):
                return pd.read_parquet(fpath)
            else:
                return pd.read_csv(fpath)
    # List directory to find actual file
    files = list(base.iterdir())
    print(f"Files in {base}: {files}")
    raise FileNotFoundError(f"No COVERPAGE file found in {base}")

def fuzzy_search_coverpage(df: pd.DataFrame, search_term: str, top_n: int = 5) -> pd.DataFrame:
    """
    Fuzzy search COVERPAGE for a fund manager name.
    Returns top_n matches sorted by similarity score.
    """
    from difflib import SequenceMatcher
    
    # Identify the manager name column
    name_col = None
    for col in df.columns:
        if "MANAGER" in col.upper() or "NAME" in col.upper() or "FILER" in col.upper():
            name_col = col
            break
    if name_col is None:
        print("Available columns:", df.columns.tolist())
        raise ValueError("Cannot find manager name column")
    
    print(f"Using column: {name_col}")
    
    search_lower = search_term.lower()
    
    def score(name):
        if pd.isna(name):
            return 0.0
        name_str = str(name).lower()
        # Direct substring match gets high score
        if search_lower in name_str:
            return 1.0
        return SequenceMatcher(None, search_lower, name_str).ratio()
    
    df = df.copy()
    df["_score"] = df[name_col].apply(score)
    results = df.nlargest(top_n, "_score")[[name_col, "ACCESSION_NUMBER" if "ACCESSION_NUMBER" in df.columns else df.columns[0], "_score"] + 
              [c for c in df.columns if "AUM" in c.upper() or "TABLEVALUETOTAL" in c.upper() or "VALUE" in c.upper()]]
    return results

# Usage example:
# cp_q3 = load_coverpage("q3")
# results = fuzzy_search_coverpage(cp_q3, "renaissance technologies")
# print(results)
```

### Steps:
1. Load COVERPAGE parquet from the quarter folder
2. Search for the fund by name (fuzzy matching)
3. Extract the `ACCESSION_NUMBER` from the best match
4. Use AUM field directly from COVERPAGE (often `TABLEVALUETOTAL` in thousands of dollars)