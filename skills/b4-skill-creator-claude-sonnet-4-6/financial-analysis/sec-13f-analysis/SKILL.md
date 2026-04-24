---
name: sec-13f-analysis
description: Analyze SEC 13F filings data from TSV files. Use this skill whenever the user asks about hedge fund holdings, AUM (Assets Under Management), stock positions, fund managers, or any analysis of 13F filings data. Triggers on questions about fund portfolios, investment positions, quarterly comparisons, or SEC filing data stored in COVERPAGE.tsv, INFOTABLE.tsv, SUMMARYPAGE.tsv files.
---

# SEC 13F Analysis Skill

## Overview

SEC Form 13F is a quarterly report filed by institutional investment managers with over $100M AUM. The data is stored in TSV files organized by quarter.

## Data Structure

Each quarter folder (e.g., `/root/2025-q3/`) contains:

- **COVERPAGE.tsv** — Fund manager identification. Key columns:
  - `ACCESSION_NUMBER`: Unique filing identifier
  - `FILINGMANAGER_NAME`: Name of the fund/manager
  - `REPORTCALENDARORQUARTER`: Quarter end date (e.g., `30-SEP-2025`)

- **INFOTABLE.tsv** — Individual stock holdings. Key columns:
  - `ACCESSION_NUMBER`: Links to COVERPAGE
  - `NAMEOFISSUER`: Company name
  - `CUSIP`: 9-character stock identifier
  - `VALUE`: Position value in thousands of USD
  - `SSHPRNAMT`: Number of shares

- **SUMMARYPAGE.tsv** — Fund-level summary. Key columns:
  - `ACCESSION_NUMBER`: Links to COVERPAGE
  - `TABLEVALUETOTAL`: Total portfolio value in thousands of USD (= AUM)
  - `TABLEENTRYTOTAL`: Number of holdings

- **SUBMISSION.tsv** — Filing metadata (dates, CIK, etc.)

## Common Analysis Patterns

### 1. Find a Fund by Name (Fuzzy Search)

```python
import pandas as pd

cover = pd.read_csv('/root/2025-q3/COVERPAGE.tsv', sep='\t', dtype=str)
# Case-insensitive search
mask = cover['FILINGMANAGER_NAME'].str.contains('renaissance', case=False, na=False)
results = cover[mask][['ACCESSION_NUMBER', 'FILINGMANAGER_NAME']]
print(results)
```

### 2. Get AUM for a Fund

```python
import pandas as pd

accession = '0001037389-25-000007'  # from COVERPAGE lookup
summary = pd.read_csv('/root/2025-q3/SUMMARYPAGE.tsv', sep='\t', dtype=str)
row = summary[summary['ACCESSION_NUMBER'] == accession]
# TABLEVALUETOTAL is in thousands of USD
aum_thousands = int(row['TABLEVALUETOTAL'].values[0])
aum_dollars = aum_thousands * 1000
print(f"AUM: ${aum_dollars:,}")
```

### 3. Count Holdings for a Fund

```python
import pandas as pd

accession = '0001037389-25-000007'
info = pd.read_csv('/root/2025-q3/INFOTABLE.tsv', sep='\t', dtype=str)
holdings = info[info['ACCESSION_NUMBER'] == accession]
print(f"Number of holdings: {len(holdings)}")
```

### 4. Find a Stock by CUSIP or Name

```python
import pandas as pd

info = pd.read_csv('/root/2025-q3/INFOTABLE.tsv', sep='\t', dtype=str)
# Search by company name
mask = info['NAMEOFISSUER'].str.contains('palantir', case=False, na=False)
stocks = info[mask][['CUSIP', 'NAMEOFISSUER']].drop_duplicates()
print(stocks)
```

### 5. Compare Holdings Between Quarters

```python
import pandas as pd

q2_info = pd.read_csv('/root/2025-q2/INFOTABLE.tsv', sep='\t', dtype=str)
q3_info = pd.read_csv('/root/2025-q3/INFOTABLE.tsv', sep='\t', dtype=str)

# Filter by accession number for each quarter
q2_holdings = q2_info[q2_info['ACCESSION_NUMBER'] == q2_accession].copy()
q3_holdings = q3_info[q3_info['ACCESSION_NUMBER'] == q3_accession].copy()

# Convert VALUE to numeric
q2_holdings['VALUE'] = pd.to_numeric(q2_holdings['VALUE'], errors='coerce')
q3_holdings['VALUE'] = pd.to_numeric(q3_holdings['VALUE'], errors='coerce')

# Merge on CUSIP
merged = pd.merge(
    q3_holdings[['CUSIP', 'NAMEOFISSUER', 'VALUE']],
    q2_holdings[['CUSIP', 'VALUE']],
    on='CUSIP', how='outer', suffixes=('_q3', '_q2')
).fillna(0)

merged['value_change'] = merged['VALUE_q3'] - merged['VALUE_q2']
top_increases = merged.nlargest(5, 'value_change')
print(top_increases[['CUSIP', 'NAMEOFISSUER', 'value_change']])
```

### 6. Find Top Investors in a Stock

```python
import pandas as pd

cusip = '69608A108'  # Palantir CUSIP
info = pd.read_csv('/root/2025-q3/INFOTABLE.tsv', sep='\t', dtype=str)
cover = pd.read_csv('/root/2025-q3/COVERPAGE.tsv', sep='\t', dtype=str)

holders = info[info['CUSIP'] == cusip].copy()
holders['VALUE'] = pd.to_numeric(holders['VALUE'], errors='coerce')

# Sum by fund (in case of multiple entries per fund)
by_fund = holders.groupby('ACCESSION_NUMBER')['VALUE'].sum().reset_index()
by_fund = by_fund.nlargest(10, 'VALUE')

# Join with fund names
result = pd.merge(by_fund, cover[['ACCESSION_NUMBER', 'FILINGMANAGER_NAME']], on='ACCESSION_NUMBER')
print(result[['FILINGMANAGER_NAME', 'VALUE']])
```

## Notes

- VALUE in INFOTABLE and TABLEVALUETOTAL in SUMMARYPAGE are in **thousands of USD**
- CUSIP is a 9-character identifier unique to each security
- One fund may have multiple rows in INFOTABLE (one per stock held)
- Accession numbers change each quarter — always look them up fresh
- Some funds file amendments (`ISAMENDMENT = Y`); prefer non-amendment or latest amendment
