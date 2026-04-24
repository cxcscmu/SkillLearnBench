---
name: count-renaissance-stocks
description: Count the number of distinct stocks (equity positions only) held by Renaissance Technologies. Filters to SH (share) type only and excludes options/derivatives by checking PUTCALL column. Use this specifically for Q2 answer about Renaissance stock count.
---

## Count Distinct Stocks for Renaissance Technologies

The key insight: "number of stocks" means distinct underlying companies with **direct equity positions only**.

```python
import pandas as pd
from pathlib import Path

def count_renaissance_stocks(holdings: pd.DataFrame) -> int:
    """
    Count distinct stocks held by Renaissance Technologies.
    
    Rules:
    1. Filter to equity shares only: SSHPRNAMTTYPE == 'SH' (exclude 'PRN' bonds/debt)
    2. Exclude options/derivatives: filter out rows where PUTCALL is not null/empty
    3. Count distinct CUSIPs (each CUSIP = one underlying company/stock)
    
    Parameters:
        holdings: DataFrame of fund holdings from INFOTABLE
    
    Returns:
        int: count of distinct stock positions
    """
    print(f"Total holdings rows: {len(holdings)}")
    print(f"Columns: {holdings.columns.tolist()}")
    
    # Step 1: Identify the share type column
    type_col = None
    for col in holdings.columns:
        if "PRNAMTTYPE" in col.upper() or "SSHPRNAMTTYPE" in col.upper():
            type_col = col
            break
    
    if type_col:
        print(f"Share type column: {type_col}")
        print(f"Unique values in {type_col}: {holdings[type_col].unique()}")
        # Filter to equity shares only (SH = shares, exclude PRN = principal/bonds)
        equity = holdings[holdings[type_col] == 'SH'].copy()
        print(f"After filtering SH only: {len(equity)} rows")
    else:
        print("WARNING: No share type column found, using all rows")
        equity = holdings.copy()
    
    # Step 2: Exclude options (PUTCALL column)
    putcall_col = None
    for col in equity.columns:
        if "PUTCALL" in col.upper():
            putcall_col = col
            break
    
    if putcall_col:
        print(f"PUTCALL column: {putcall_col}")
        print(f"Unique PUTCALL values: {equity[putcall_col].unique()}")
        # Keep only rows where PUTCALL is null/empty (direct stock positions, not options)
        before = len(equity)
        equity = equity[equity[putcall_col].isna() | (equity[putcall_col] == '') | (equity[putcall_col] == 'None')]
        print(f"After excluding options (PUTCALL not null): {before} -> {len(equity)} rows")
    else:
        print("No PUTCALL column found — skipping options filter")
    
    # Step 3: Count distinct CUSIPs
    cusip_col = None
    for col in equity.columns:
        if "CUSIP" in col.upper():
            cusip_col = col
            break
    
    if cusip_col is None:
        raise ValueError(f"No CUSIP column found. Columns: {equity.columns.tolist()}")
    
    distinct_stocks = equity[cusip_col].nunique()
    print(f"Distinct CUSIPs (equity, non-option): {distinct_stocks}")
    
    # Also show some diagnostics
    print(f"\nSample of equity holdings:")
    print(equity[[cusip_col, type_col if type_col else equity.columns[0]]].head(10))
    
    return distinct_stocks

# Full workflow:
# 1. Load coverpage and find Renaissance accession number
# 2. Load holdings
# 3. Count stocks

def run_renaissance_analysis(quarter: str = "q3"):
    from difflib import SequenceMatcher
    
    # Load coverpage
    base = Path(f"/root/2025-{quarter}")
    cp = None
    for fname in ["COVERPAGE.parquet", "coverpage.parquet"]:
        fpath = base / fname
        if fpath.exists():
            cp = pd.read_parquet(fpath)
            break
    
    if cp is None:
        raise FileNotFoundError("COVERPAGE not found")
    
    print("COVERPAGE columns:", cp.columns.tolist())
    
    # Find manager name column
    name_col = None
    for col in cp.columns:
        if "MANAGER" in col.upper() or "NAME" in col.upper():
            name_col = col
            break
    
    search_term = "renaissance technologies"
    
    def score(name):
        if pd.isna(name):
            return 0.0
        s = str(name).lower()
        if search_term in s:
            return 1.0
        return SequenceMatcher(None, search_term, s).ratio()
    
    cp["_score"] = cp[name_col].apply(score)
    best = cp.nlargest(5, "_score")
    print("\nTop matches:")
    print(best[[name_col, "ACCESSION_NUMBER" if "ACCESSION_NUMBER" in cp.columns else cp.columns[1], "_score"]])
    
    # Get best match accession number
    best_row = cp.nlargest(1, "_score").iloc[0]
    acc_col = "ACCESSION_NUMBER" if "ACCESSION_NUMBER" in cp.columns else [c for c in cp.columns if "ACCESSION" in c.upper()][0]
    accession = best_row[acc_col]
    print(f"\nBest match: {best_row[name_col]}, Accession: {accession}")
    
    # Get AUM
    aum_col = None
    for col in cp.columns:
        if "TABLEVALUETOTAL" in col.upper() or "AUM" in col.upper():
            aum_col = col
            break
    if aum_col:
        print(f"AUM ({aum_col}): {best_row[aum_col]}")
    
    # Load holdings
    it = None
    for fname in ["INFOTABLE.parquet", "infotable.parquet"]:
        fpath = base / fname
        if fpath.exists():
            it = pd.read_parquet(fpath)
            break
    
    it_acc_col = [c for c in it.columns if "ACCESSION" in c.upper()][0]
    holdings = it[it[it_acc_col] == accession].copy()
    
    stock_count = count_renaissance_stocks(holdings)
    
    return {
        "accession_number": accession,
        "aum": best_row[aum_col] if aum_col else None,
        "stock_count": stock_count
    }
```

### Key Rules for Counting Stocks:
1. **Filter `SSHPRNAMTTYPE == 'SH'`** — removes bond/debt positions (PRN type)
2. **Filter `PUTCALL` is null/empty** — removes options (calls and puts)
3. **Count `CUSIP.nunique()`** — distinct underlying companies
4. Do NOT count total rows — that inflates with duplicate entries for same stock under different position types