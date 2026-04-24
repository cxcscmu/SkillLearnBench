---
name: run2_quarter_comparison
description: Compare holdings across quarters to identify increased/decreased investments
---

# Quarter-to-Quarter Holdings Comparison

## Overview
Compare a fund's holdings between two quarters (e.g., Q2 to Q3) to identify which stocks received increased or decreased investment.

## Core Workflow

### Step 1: Get Accession Numbers for Both Quarters
```python
import pandas as pd

# Q2 (June 30)
coverpage_q2 = pd.read_csv('/root/2025-q2/COVERPAGE.tsv', sep='\t')
fund_q2 = coverpage_q2[coverpage_q2['FILINGMANAGER_NAME'].str.contains('Berkshire', case=False)]
accession_q2 = fund_q2['ACCESSION_NUMBER'].values[0]

# Q3 (September 30)
coverpage_q3 = pd.read_csv('/root/2025-q3/COVERPAGE.tsv', sep='\t')
fund_q3 = coverpage_q3[coverpage_q3['FILINGMANAGER_NAME'].str.contains('Berkshire', case=False)]
accession_q3 = fund_q3['ACCESSION_NUMBER'].values[0]
```

### Step 2: Load Holdings for Both Quarters
```python
# Load INFOTABLE for both quarters
infotable_q2 = pd.read_csv('/root/2025-q2/INFOTABLE.tsv', sep='\t', low_memory=False)
infotable_q3 = pd.read_csv('/root/2025-q3/INFOTABLE.tsv', sep='\t', low_memory=False)

# Filter to specific fund
fund_q2_holdings = infotable_q2[infotable_q2['ACCESSION_NUMBER'] == accession_q2]
fund_q3_holdings = infotable_q3[infotable_q3['ACCESSION_NUMBER'] == accession_q3]
```

### Step 3: Aggregate by CUSIP
```python
# Group Q2 holdings by CUSIP
q2_summary = fund_q2_holdings.groupby('CUSIP').agg({
    'VALUE': 'sum',
    'NAMEOFISSUER': 'first',
    'SSHPRNAMT': 'sum'
}).reset_index()
q2_summary.columns = ['CUSIP', 'VALUE_Q2', 'NAMEOFISSUER_Q2', 'SHARES_Q2']

# Group Q3 holdings by CUSIP
q3_summary = fund_q3_holdings.groupby('CUSIP').agg({
    'VALUE': 'sum',
    'NAMEOFISSUER': 'first',
    'SSHPRNAMT': 'sum'
}).reset_index()
q3_summary.columns = ['CUSIP', 'VALUE_Q3', 'NAMEOFISSUER_Q3', 'SHARES_Q3']
```

### Step 4: Merge and Calculate Changes
```python
# Merge on CUSIP (outer join to capture new and exited positions)
comparison = pd.merge(q2_summary, q3_summary, on='CUSIP', how='outer')

# Fill NaN with 0 (positions not held in that quarter)
comparison['VALUE_Q2'] = comparison['VALUE_Q2'].fillna(0)
comparison['VALUE_Q3'] = comparison['VALUE_Q3'].fillna(0)

# Calculate value change
comparison['VALUE_CHANGE'] = comparison['VALUE_Q3'] - comparison['VALUE_Q2']
comparison['SHARE_CHANGE'] = comparison['SHARES_Q3'].fillna(0) - comparison['SHARES_Q2'].fillna(0)
```

### Step 5: Identify Top Changes
```python
# Top 5 stocks with INCREASED investment (positive value change)
top_5_increases = comparison[comparison['VALUE_CHANGE'] > 0].nlargest(5, 'VALUE_CHANGE')

# Top 5 stocks with DECREASED investment (negative value change)
top_5_decreases = comparison[comparison['VALUE_CHANGE'] < 0].nsmallest(5, 'VALUE_CHANGE')

# Get CUSIPs
increased_cusips = top_5_increases['CUSIP'].tolist()
decreased_cusips = top_5_decreases['CUSIP'].tolist()

print("Top 5 Increased Positions:")
print(top_5_increases[['CUSIP', 'NAMEOFISSUER_Q2', 'VALUE_Q2', 'VALUE_Q3', 'VALUE_CHANGE']])
```

## Important Considerations

### Handling Missing Companies
```python
# Use first non-null NAMEOFISSUER
comparison['NAMEOFISSUER'] = comparison['NAMEOFISSUER_Q2'].fillna(comparison['NAMEOFISSUER_Q3'])

# New positions (not in Q2): NAMEOFISSUER_Q2 is NaN
new_positions = comparison[comparison['VALUE_Q2'] == 0][comparison['VALUE_CHANGE'] > 0]

# Exited positions (not in Q3): NAMEOFISSUER_Q3 is NaN
exited_positions = comparison[comparison['VALUE_Q3'] == 0][comparison['VALUE_CHANGE'] < 0]
```

### Duplicate CUSIP Handling
Some fund filings may have the same CUSIP listed multiple times (different options, derivative types, etc.). The aggregation via `groupby().agg()` handles this automatically by summing.

### Data Type Warnings
```python
# Avoid DtypeWarning when loading INFOTABLE
infotable = pd.read_csv(
    'INFOTABLE.tsv',
    sep='\t',
    low_memory=False,  # Critical for INFOTABLE
    dtype={'ACCESSION_NUMBER': 'str', 'CUSIP': 'str', 'VALUE': 'int64'}
)
```

## Complete Example: Berkshire Q2 to Q3

```python
import pandas as pd

# Load files
infotable_q2 = pd.read_csv('/root/2025-q2/INFOTABLE.tsv', sep='\t', low_memory=False)
infotable_q3 = pd.read_csv('/root/2025-q3/INFOTABLE.tsv', sep='\t', low_memory=False)
coverpage_q2 = pd.read_csv('/root/2025-q2/COVERPAGE.tsv', sep='\t')
coverpage_q3 = pd.read_csv('/root/2025-q3/COVERPAGE.tsv', sep='\t')

# Get accession numbers
accession_q2 = coverpage_q2[coverpage_q2['FILINGMANAGER_NAME'] == 'Berkshire Hathaway Inc']['ACCESSION_NUMBER'].values[0]
accession_q3 = coverpage_q3[coverpage_q3['FILINGMANAGER_NAME'] == 'Berkshire Hathaway Inc']['ACCESSION_NUMBER'].values[0]

# Get holdings
q2_holdings = infotable_q2[infotable_q2['ACCESSION_NUMBER'] == accession_q2]
q3_holdings = infotable_q3[infotable_q3['ACCESSION_NUMBER'] == accession_q3]

# Aggregate by CUSIP
q2_agg = q2_holdings.groupby('CUSIP')['VALUE'].sum().reset_index()
q2_agg.columns = ['CUSIP', 'VALUE_Q2']

q3_agg = q3_holdings.groupby('CUSIP')['VALUE'].sum().reset_index()
q3_agg.columns = ['CUSIP', 'VALUE_Q3']

# Merge
comparison = pd.merge(q2_agg, q3_agg, on='CUSIP', how='outer')
comparison['VALUE_Q2'] = comparison['VALUE_Q2'].fillna(0)
comparison['VALUE_Q3'] = comparison['VALUE_Q3'].fillna(0)
comparison['VALUE_CHANGE'] = comparison['VALUE_Q3'] - comparison['VALUE_Q2']

# Top 5 increases
top_5 = comparison[comparison['VALUE_CHANGE'] > 0].nlargest(5, 'VALUE_CHANGE')
cusips = top_5['CUSIP'].tolist()

print(cusips)
# Output: ['02079K305', '037833100', '025816109', '166764100', '674599105']
```

## Output Format

Result should be a list of CUSIPs ordered by value change (descending):
```json
{
    "top_5_cusips": ["CUSIP1", "CUSIP2", "CUSIP3", "CUSIP4", "CUSIP5"],
    "changes": [
        {"cusip": "CUSIP1", "value_change": 4338397000000},
        {"cusip": "CUSIP2", "value_change": 3208516000000}
    ]
}
```

## Validation Checklist

- [ ] Confirm accession numbers exist for both Q2 and Q3
- [ ] Verify merging on CUSIP is case-sensitive and exact
- [ ] Check that outer join captures both new and exited positions
- [ ] Validate top 5 are sorted by VALUE_CHANGE (descending)
- [ ] Confirm VALUE_CHANGE = VALUE_Q3 - VALUE_Q2 (should be positive for increases)
- [ ] Handle NaN values correctly before calculation
