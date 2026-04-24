---
name: sec-13f-compare-holdings-q2-q3
description: How to compare fund holdings between Q2 and Q3 to find top stocks with increased investment by dollar value
---

## Comparing Holdings Between Quarters (Q2 vs Q3)

### Method 1: Use Built-in Scripts (Preferred)
```bash
# Check for holding comparison script
cat /root/2025-q3/scripts/holding_analysis.py 2>/dev/null
# It may accept two accession numbers for comparison
python /root/2025-q3/scripts/holding_analysis.py "<Q2_ACCESSION>" "<Q3_ACCESSION>" 2>/dev/null
```

### Method 2: Manual Comparison

#### Step 1: Get accession numbers for both quarters
```python
import pandas as pd

# Search in Q2
cover_q2 = pd.read_csv('/root/2025-q2/COVERPAGE.tsv', sep='\t', low_memory=False)
search = "berkshire hathaway"
# Find the name column first
print(cover_q2.columns.tolist())
name_col = 'FILINGMANAGER_NAME'  # adjust as needed
q2_matches = cover_q2[cover_q2[name_col].astype(str).str.lower().str.contains(search, na=False)]
print(q2_matches[['ACCESSION_NUMBER', name_col]])
accession_q2 = q2_matches['ACCESSION_NUMBER'].iloc[0]

# Search in Q3
cover_q3 = pd.read_csv('/root/2025-q3/COVERPAGE.tsv', sep='\t', low_memory=False)
q3_matches = cover_q3[cover_q3[name_col].astype(str).str.lower().str.contains(search, na=False)]
accession_q3 = q3_matches['ACCESSION_NUMBER'].iloc[0]
```

#### Step 2: Load holdings for both quarters
```python
info_q2 = pd.read_csv('/root/2025-q2/INFOTABLE.tsv', sep='\t', low_memory=False)
info_q3 = pd.read_csv('/root/2025-q3/INFOTABLE.tsv', sep='\t', low_memory=False)

holdings_q2 = info_q2[info_q2['ACCESSION_NUMBER'] == accession_q2].copy()
holdings_q3 = info_q3[info_q3['ACCESSION_NUMBER'] == accession_q3].copy()

# Filter to stocks only (exclude options)
for df in [holdings_q2, holdings_q3]:
    # Check PUTCALL values first
    print(df['PUTCALL'].value_counts(dropna=False))

# Keep only non-option rows
def filter_stocks(df):
    return df[df['PUTCALL'].isna() | (df['PUTCALL'].astype(str).str.strip().isin(['', 'nan', 'NaN', 'None']))]

holdings_q2 = filter_stocks(holdings_q2)
holdings_q3 = filter_stocks(holdings_q3)
```

#### Step 3: Aggregate by CUSIP and compare
```python
# Aggregate VALUE by CUSIP (VALUE is in thousands)
q2_agg = holdings_q2.groupby('CUSIP')['VALUE'].sum().reset_index()
q2_agg.columns = ['CUSIP', 'VALUE_Q2']

q3_agg = holdings_q3.groupby('CUSIP')['VALUE'].sum().reset_index()
q3_agg.columns = ['CUSIP', 'VALUE_Q3']

# Merge
merged = q3_agg.merge(q2_agg, on='CUSIP', how='outer').fillna(0)
merged['VALUE_CHANGE'] = merged['VALUE_Q3'] - merged['VALUE_Q2']

# Top 5 increased investments
top5_increased = merged.sort_values('VALUE_CHANGE', ascending=False).head(5)
print(top5_increased[['CUSIP', 'VALUE_Q2', 'VALUE_Q3', 'VALUE_CHANGE']])
top5_cusips = top5_increased['CUSIP'].tolist()
```