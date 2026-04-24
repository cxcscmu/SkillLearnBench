---
name: run2_fund_analysis
description: Analyze individual fund holdings, AUM, and portfolio composition from 13-F data
---

# Fund Analysis from 13-F Data

## Overview
Analyze specific hedge funds or asset managers using 13-F filings to answer questions about AUM, holdings count, and portfolio composition.

## Finding a Fund's Accession Number

### Method 1: Exact Name Search
When you know the exact manager name:
```python
import pandas as pd

coverpage = pd.read_csv('/root/2025-q3/COVERPAGE.tsv', sep='\t')
fund = coverpage[coverpage['FILINGMANAGER_NAME'] == 'Renaissance Technologies LLC']
accession = fund['ACCESSION_NUMBER'].values[0]
```

### Method 2: Fuzzy/Partial Name Search
When name might be slightly different:
```python
# Use case-insensitive contains search
fund = coverpage[coverpage['FILINGMANAGER_NAME'].str.contains('Renaissance', case=False, na=False)]
accession = fund['ACCESSION_NUMBER'].values[0]
```

### Method 3: Using fuzzy-name-search Skill
```bash
python3 scripts/search_fund.py --keywords "renaissance technologies" --quarter 2025-q3 --topk 10
```

**Best Practice**: Start with exact name search in raw data, then use fuzzy search if not found.

## Extracting Fund Metrics

### Q1: Get Fund AUM (Assets Under Management)

**Method**: Use INFOTABLE VALUE sum (more reliable than SUMMARYPAGE)
```python
accession = "0001037389-25-000064"  # Renaissance Technologies LLC

infotable = pd.read_csv('/root/2025-q3/INFOTABLE.tsv', sep='\t', low_memory=False)
fund_holdings = infotable[infotable['ACCESSION_NUMBER'] == accession]

# AUM = sum of all holdings values (VALUE is in dollars)
aum = fund_holdings['VALUE'].sum()
print(f"AUM: ${aum:,.0f}")
```

**Note**: The VALUE column is in actual dollars (not thousands). This can be verified by comparing with SUMMARYPAGE.TABLEVALUETOTAL which should match exactly.

### Q2: Count Total Holdings

**Method**: Count distinct CUSIPs
```python
fund_holdings = infotable[infotable['ACCESSION_NUMBER'] == accession]

# Count unique securities (CUSIPs)
num_holdings = fund_holdings['CUSIP'].nunique()
print(f"Number of holdings: {num_holdings}")

# Alternative: Count rows (if no duplicate CUSIPs per accession)
num_holdings = len(fund_holdings)
```

### Q3: Get Top Holdings by Value

**Method**: Group by CUSIP and sort by VALUE
```python
fund_holdings = infotable[infotable['ACCESSION_NUMBER'] == accession]

# Group by CUSIP and aggregate
top_holdings = fund_holdings.groupby('CUSIP').agg({
    'NAMEOFISSUER': 'first',
    'VALUE': 'sum',
    'SSHPRNAMT': 'sum'
}).reset_index()

# Sort by value descending
top_holdings = top_holdings.sort_values('VALUE', ascending=False)

print(top_holdings[['NAMEOFISSUER', 'VALUE']].head(10))
```

### Q4: Identify Fund Manager from Holdings

When you have an accession number and want the fund name:
```python
coverpage = pd.read_csv('/root/2025-q3/COVERPAGE.tsv', sep='\t')
fund_info = coverpage[coverpage['ACCESSION_NUMBER'] == accession]
fund_name = fund_info['FILINGMANAGER_NAME'].values[0]
```

## Common Fund Analysis Patterns

### Portfolio Concentration
```python
# What % of AUM is in top 10 holdings
fund_holdings = infotable[infotable['ACCESSION_NUMBER'] == accession]
top_10_value = fund_holdings.nlargest(10, 'VALUE')['VALUE'].sum()
total_value = fund_holdings['VALUE'].sum()
concentration = (top_10_value / total_value) * 100
print(f"Top 10 concentration: {concentration:.1f}%")
```

### Sector Analysis
```python
# Group holdings by sector (requires additional sector mapping)
# This requires matching CUSIP to sector data from another source
# Left as exercise based on available data
```

### Time-Based Analysis
```python
# Check when fund last reported
coverpage = pd.read_csv('/root/2025-q3/COVERPAGE.tsv', sep='\t')
fund_info = coverpage[coverpage['ACCESSION_NUMBER'] == accession]
report_date = fund_info['REPORTCALENDARORQUARTER'].values[0]
print(f"Last reported: {report_date}")
```

## Key Metrics Summary

For a given accession number:
1. **AUM**: `INFOTABLE[ACCESSION].VALUE.sum()`
2. **Holdings Count**: `INFOTABLE[ACCESSION].CUSIP.nunique()`
3. **Average Position Size**: AUM / Holdings Count
4. **Top 5 Holdings**: `nlargest(5, 'VALUE')`
5. **Fund Manager**: `COVERPAGE[ACCESSION].FILINGMANAGER_NAME`
6. **Report Date**: `COVERPAGE[ACCESSION].REPORTCALENDARORQUARTER`

## Important Considerations

1. **Handle Multiple Managers**: Some holdings may list multiple managers in OTHERMANAGER columns
2. **Amendment Status**: Check ISAMENDMENT in COVERPAGE (some filings are restated)
3. **Confidential Filings**: Some funds may have confidential positions omitted
4. **CUSIP Aggregation**: When grouping by CUSIP, sum VALUE as some holdings may be split across rows

## Validation Checklist

- [ ] Confirm ACCESSION_NUMBER exists in both COVERPAGE and INFOTABLE
- [ ] Verify sum of INFOTABLE.VALUE matches SUMMARYPAGE.TABLEVALUETOTAL
- [ ] Check report date matches expected quarter
- [ ] Confirm fund name in FILINGMANAGER_NAME is the intended fund
- [ ] Validate holdings count makes sense (typically 50-5000+ positions)
