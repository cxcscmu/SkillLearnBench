---
name: run2_cross_fund_analysis
description: Find which funds hold a specific stock and rank them by holding value
---

# Cross-Fund Holdings Analysis

## Overview
Analyze which funds hold a specific security (identified by CUSIP) and rank them by the size of their investment. This is useful for understanding which asset managers have the largest positions in a given stock.

## Finding a Stock's CUSIP

### Method 1: Exact Search (if you know CUSIP)
```python
import pandas as pd

# You already know the CUSIP
palantir_cusip = "69608A108"
```

### Method 2: Fuzzy Search for CUSIP
```python
# Use the fuzzy-name-search skill
# Command: python3 scripts/search_stock_cusip.py --keywords palantir --topk 10
# Returns: CUSIP: 69608A108
```

### Method 3: Search INFOTABLE
```python
# Search NAMEOFISSUER in INFOTABLE
infotable = pd.read_csv('/root/2025-q3/INFOTABLE.tsv', sep='\t', low_memory=False)
palantir_rows = infotable[infotable['NAMEOFISSUER'].str.contains('Palantir', case=False, na=False)]
cusip = palantir_rows['CUSIP'].unique()[0]
print(f"Palantir CUSIP: {cusip}")
```

## Finding All Funds Holding a Stock

### Step 1: Filter INFOTABLE by CUSIP
```python
import pandas as pd

palantir_cusip = "69608A108"

# Load INFOTABLE for the target quarter
infotable = pd.read_csv('/root/2025-q3/INFOTABLE.tsv', sep='\t', low_memory=False)

# Find all fund holdings of this stock
stock_holdings = infotable[infotable['CUSIP'] == palantir_cusip]

print(f"Number of funds holding this stock: {stock_holdings['ACCESSION_NUMBER'].nunique()}")
print(f"Total holdings records: {len(stock_holdings)}")
```

### Step 2: Link to Fund Manager Names
```python
# Load COVERPAGE to get fund names
coverpage = pd.read_csv('/root/2025-q3/COVERPAGE.tsv', sep='\t')

# Merge holdings with fund information
holdings_with_funds = pd.merge(
    stock_holdings,
    coverpage[['ACCESSION_NUMBER', 'FILINGMANAGER_NAME']],
    on='ACCESSION_NUMBER'
)

print(f"Unique funds: {holdings_with_funds['FILINGMANAGER_NAME'].nunique()}")
```

### Step 3: Aggregate and Rank by Value
```python
# Group by fund manager and sum the value
fund_holdings = holdings_with_funds.groupby('FILINGMANAGER_NAME').agg({
    'VALUE': 'sum',
    'SSHPRNAMT': 'sum',  # Share count
    'ACCESSION_NUMBER': 'first'
}).reset_index()

# Rename for clarity
fund_holdings.columns = ['FUND_NAME', 'TOTAL_VALUE', 'TOTAL_SHARES', 'ACCESSION_NUMBER']

# Sort by value (descending) to get largest holders
fund_holdings = fund_holdings.sort_values('TOTAL_VALUE', ascending=False)

print(fund_holdings.head(10))
```

### Step 4: Get Top N Funds
```python
# Extract top 3 fund names
top_3_funds = fund_holdings.nlargest(3, 'TOTAL_VALUE')
top_3_names = top_3_funds['FUND_NAME'].tolist()

print("Top 3 funds holding Palantir (by value):")
for i, (name, value) in enumerate(zip(top_3_names, top_3_funds['TOTAL_VALUE']), 1):
    print(f"{i}. {name}: ${value:,.0f}")
```

## Complete Example: Palantir Holdings

```python
import pandas as pd

# Stock CUSIP
palantir_cusip = "69608A108"

# Load files
infotable = pd.read_csv('/root/2025-q3/INFOTABLE.tsv', sep='\t', low_memory=False)
coverpage = pd.read_csv('/root/2025-q3/COVERPAGE.tsv', sep='\t')

# Find all holdings
palantir_holdings = infotable[infotable['CUSIP'] == palantir_cusip]

# Merge with fund names
holdings_with_names = pd.merge(
    palantir_holdings,
    coverpage[['ACCESSION_NUMBER', 'FILINGMANAGER_NAME']],
    on='ACCESSION_NUMBER'
)

# Aggregate by fund
fund_summary = holdings_with_names.groupby('FILINGMANAGER_NAME').agg({
    'VALUE': 'sum'
}).reset_index()

# Sort and get top 3
top_3 = fund_summary.nlargest(3, 'VALUE')
fund_names = top_3['FILINGMANAGER_NAME'].tolist()

print(fund_names)
# Output: ['VANGUARD GROUP INC', 'BlackRock, Inc.', 'STATE STREET CORP']
```

## Key Metrics for Cross-Fund Analysis

For a given CUSIP:
1. **Total Funds Holding**: `stock_holdings['ACCESSION_NUMBER'].nunique()`
2. **Total Shares Outstanding (across funds)**: `stock_holdings['SSHPRNAMT'].sum()`
3. **Aggregate Value**: `stock_holdings['VALUE'].sum()`
4. **Largest Holder**: First entry after sorting by VALUE descending
5. **Top 3 Holders**: `nlargest(3, 'VALUE')`
6. **Concentration**: (Top 3 value / Aggregate value) * 100

## Important Considerations

### Handling Multiple Records per Fund
```python
# Some funds may have Palantir in multiple rows (different options, derivatives, etc.)
# The groupby().sum() handles this correctly by aggregating all values

# Example: Fund A might have:
#   Row 1: 100M (common stock)
#   Row 2: 50M (call options)
# Total: 150M (correctly summed by groupby)
```

### Data Types
```python
# Ensure CUSIP is treated as string
infotable = pd.read_csv(
    'INFOTABLE.tsv',
    sep='\t',
    low_memory=False,
    dtype={'CUSIP': 'str', 'ACCESSION_NUMBER': 'str', 'VALUE': 'int64'}
)
```

### Filtering Options
```python
# Option 1: Exact CUSIP match
stock_holdings = infotable[infotable['CUSIP'] == cusip]

# Option 2: CUSIP contains (for potential variations)
stock_holdings = infotable[infotable['CUSIP'].str.contains(cusip_partial, na=False)]

# Option 3: NAMEOFISSUER contains (good for verification)
stock_holdings = infotable[infotable['NAMEOFISSUER'].str.contains('Palantir', case=False, na=False)]
```

## Validation Checklist

- [ ] Confirm CUSIP is correct (9 characters, case-sensitive)
- [ ] Verify CUSIP exists in INFOTABLE for the target quarter
- [ ] Confirm merge between INFOTABLE and COVERPAGE on ACCESSION_NUMBER is 1-to-many
- [ ] Check that VALUE is in dollars (not thousands)
- [ ] Validate top funds have reasonable holding sizes
- [ ] Confirm fund names are unique after groupby (no duplicates in top 3)
- [ ] Verify output order is descending by VALUE

## Output Format

```json
{
    "stock_cusip": "69608A108",
    "stock_name": "PALANTIR TECHNOLOGIES INC",
    "number_of_funds": 4531,
    "total_value": 123456789,
    "top_3_funds": [
        {
            "rank": 1,
            "name": "VANGUARD GROUP INC",
            "value": 39017133374,
            "shares": 213886270
        },
        {
            "rank": 2,
            "name": "BlackRock, Inc.",
            "value": 34409511965,
            "shares": 188627957
        },
        {
            "rank": 3,
            "name": "STATE STREET CORP",
            "value": 18471648356,
            "shares": 101258899
        }
    ]
}
```
