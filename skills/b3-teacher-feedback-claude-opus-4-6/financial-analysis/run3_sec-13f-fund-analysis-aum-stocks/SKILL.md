---
name: sec-13f-fund-analysis-aum-stocks
description: How to analyze a fund's AUM and stock count using accession_number, with proper filtering of options and deduplication. Covers Q1 (AUM) and Q2 (stock count).
---

## Fund Analysis: AUM and Stock Count

### Method 1: Use Built-in Scripts (Preferred and More Reliable)
```bash
# Check if analysis script exists and read its source
cat /root/2025-q3/scripts/one_fund_analysis.py 2>/dev/null
# Run it with the accession number
python /root/2025-q3/scripts/one_fund_analysis.py "<ACCESSION_NUMBER>" 2>/dev/null
```

**Always prefer built-in scripts** as they handle edge cases (option filtering, deduplication) correctly.

### Method 2: Manual Analysis

#### Getting AUM
AUM might be in SUMMARYPAGE.tsv or can be computed from INFOTABLE:
```python
import pandas as pd

# Check SUMMARYPAGE first
summary = pd.read_csv('/root/2025-q3/SUMMARYPAGE.tsv', sep='\t')
fund_summary = summary[summary['ACCESSION_NUMBER'] == accession]
print(fund_summary)
# Look for columns like TABLEENTRYTOTAL, TABLEVALUETOTAL, etc.

# Or compute from INFOTABLE
info = pd.read_csv('/root/2025-q3/INFOTABLE.tsv', sep='\t', low_memory=False)
fund_holdings = info[info['ACCESSION_NUMBER'] == accession]
aum = fund_holdings['VALUE'].sum()  # VALUE is in thousands
print(f"AUM: ${aum * 1000:,.0f}")  # or just report in thousands
```

#### Counting Stocks Held - CRITICAL FILTERING
**The stock count must exclude options (PUT/CALL entries).** The PUTCALL column may contain unexpected values.

```python
# STEP 1: Inspect PUTCALL column thoroughly
fund_holdings = info[info['ACCESSION_NUMBER'] == accession]
print("PUTCALL unique values:", fund_holdings['PUTCALL'].unique())
print("PUTCALL value counts:")
print(fund_holdings['PUTCALL'].value_counts(dropna=False))

# STEP 2: Also inspect SSHPRNAMTTYPE
print("SSHPRNAMTTYPE unique values:", fund_holdings['SSHPRNAMTTYPE'].unique())
print(fund_holdings['SSHPRNAMTTYPE'].value_counts(dropna=False))

# STEP 3: Filter to only stock holdings (exclude PUT and CALL)
# Options have PUTCALL = "Put" or "Call" (check exact case/spelling)
# Stocks have PUTCALL as NaN or empty
stocks_only = fund_holdings[
    ~fund_holdings['PUTCALL'].isin(['Put', 'Call', 'PUT', 'CALL', 'put', 'call'])
    | fund_holdings['PUTCALL'].isna()
]

# Alternative more robust: only keep rows where PUTCALL is NaN or whitespace
stocks_only = fund_holdings[
    fund_holdings['PUTCALL'].isna() | 
    (fund_holdings['PUTCALL'].astype(str).str.strip().isin(['', 'nan', 'NaN', 'None']))
]

# STEP 4: Count unique stocks - may need to deduplicate by CUSIP
# Check if the scripts use unique CUSIPs or unique rows
num_stocks = stocks_only['CUSIP'].nunique()
print(f"Number of unique stocks (by CUSIP): {num_stocks}")

# Also check total rows vs unique CUSIPs
print(f"Total stock rows: {len(stocks_only)}")
print(f"Unique CUSIPs: {stocks_only['CUSIP'].nunique()}")
```

### Important: Understanding How Scripts Count Stocks
The built-in script likely:
1. Filters out PUT/CALL rows
2. May also filter by SSHPRNAMTTYPE == "SH" (shares only, excluding principal "PRN")
3. May deduplicate by CUSIP or CUSIP + other fields
4. Read the script source to understand the exact logic

```python
# If filtering to shares only:
stocks_sh = fund_holdings[
    (fund_holdings['PUTCALL'].isna() | (fund_holdings['PUTCALL'].astype(str).str.strip() == '')) &
    (fund_holdings['SSHPRNAMTTYPE'].astype(str).str.strip() == 'SH')
]
print(f"Shares-only count: {stocks_sh['CUSIP'].nunique()}")
```