---
name: get-fund-holdings
description: Load the INFOTABLE (holdings) parquet for a given quarter and filter by accession_number to get a specific fund's holdings. Handles column name variations. Use this after obtaining an accession_number from the coverpage.
---

## Load Fund Holdings from INFOTABLE

```python
import pandas as pd
from pathlib import Path

def load_infotable(quarter: str) -> pd.DataFrame:
    """Load INFOTABLE parquet for a given quarter ('q2' or 'q3')"""
    base = Path(f"/root/2025-{quarter}")
    for fname in ["INFOTABLE.parquet", "infotable.parquet", "INFOTABLE.csv", "infotable.csv"]:
        fpath = base / fname
        if fpath.exists():
            if fname.endswith(".parquet"):
                return pd.read_parquet(fpath)
            else:
                return pd.read_csv(fpath)
    files = list(base.iterdir())
    print(f"Files in {base}: {files}")
    raise FileNotFoundError(f"No INFOTABLE file found in {base}")

def get_fund_holdings(quarter: str, accession_number: str) -> pd.DataFrame:
    """
    Get holdings for a specific fund by accession_number.
    Returns filtered DataFrame with all holdings rows.
    """
    df = load_infotable(quarter)
    print(f"INFOTABLE columns: {df.columns.tolist()}")
    print(f"INFOTABLE shape: {df.shape}")
    
    # Find accession number column
    acc_col = None
    for col in df.columns:
        if "ACCESSION" in col.upper():
            acc_col = col
            break
    if acc_col is None:
        raise ValueError(f"No accession column found. Columns: {df.columns.tolist()}")
    
    holdings = df[df[acc_col] == accession_number].copy()
    print(f"Holdings rows for {accession_number}: {len(holdings)}")
    return holdings

# Usage:
# holdings = get_fund_holdings("q3", "0001037389-25-000001")
# print(holdings.head())
# print(holdings.columns.tolist())
```