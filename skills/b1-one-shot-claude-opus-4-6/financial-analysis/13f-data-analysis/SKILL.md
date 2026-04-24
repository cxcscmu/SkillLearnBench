---
name: 13f-data-analysis
description: Analyze SEC 13-F filings data including AUM, holdings count, and cross-quarter comparisons using TSV files.
---

# SEC 13-F Data Analysis

## Data Structure

13-F data is distributed as TSV files:

- **COVERPAGE.tsv**: Filing metadata. Key columns: `ACCESSION_NUMBER`, `FILINGMANAGER_NAME`, `REPORTCALENDARORQUARTER`
- **INFOTABLE.tsv**: Individual holdings. Key columns: `ACCESSION_NUMBER`, `NAMEOFISSUER`, `TITLEOFCLASS`, `CUSIP`, `VALUE` (in thousands $), `SSHPRNAMT` (shares), `SSHPRNAMTTYPE`
- **SUMMARYPAGE.tsv**: Aggregated data. Key columns: `ACCESSION_NUMBER`, `TABLEENTRYTOTAL` (number of holdings), `TABLEVALUETOTAL` (AUM in thousands $)

## Common Operations with Python/Pandas

### Load data
```python
import pandas as pd
cover = pd.read_csv('COVERPAGE.tsv', sep='\t')
info = pd.read_csv('INFOTABLE.tsv', sep='\t')
summary = pd.read_csv('SUMMARYPAGE.tsv', sep='\t')
```

### Find fund by name (fuzzy)
```python
from thefuzz import fuzz
cover['score'] = cover['FILINGMANAGER_NAME'].apply(lambda x: fuzz.token_sort_ratio(search_term.lower(), str(x).lower()))
best = cover.loc[cover['score'].idxmax()]
accession = best['ACCESSION_NUMBER']
```

### Get AUM and holdings count
```python
row = summary[summary['ACCESSION_NUMBER'] == accession]
aum = row['TABLEVALUETOTAL'].values[0]  # in thousands
count = row['TABLEENTRYTOTAL'].values[0]
```

### Compare holdings across quarters
```python
q2_holdings = info_q2[info_q2['ACCESSION_NUMBER'] == acc_q2][['CUSIP','VALUE','SSHPRNAMT']]
q3_holdings = info_q3[info_q3['ACCESSION_NUMBER'] == acc_q3][['CUSIP','VALUE','SSHPRNAMT']]
# Group by CUSIP (a fund may hold multiple lots of same stock)
q2_agg = q2_holdings.groupby('CUSIP')['VALUE'].sum().reset_index()
q3_agg = q3_holdings.groupby('CUSIP')['VALUE'].sum().reset_index()
merged = q3_agg.merge(q2_agg, on='CUSIP', how='outer', suffixes=('_q3','_q2')).fillna(0)
merged['change'] = merged['VALUE_q3'] - merged['VALUE_q2']
top_increases = merged.nlargest(5, 'change')
```

### Find all holders of a specific stock (by CUSIP)
```python
holders = info[info['CUSIP'] == target_cusip]
holders_agg = holders.groupby('ACCESSION_NUMBER')['VALUE'].sum().reset_index()
holders_agg = holders_agg.merge(cover[['ACCESSION_NUMBER','FILINGMANAGER_NAME']], on='ACCESSION_NUMBER')
top_holders = holders_agg.nlargest(3, 'VALUE')
```

## Notes
- VALUE column is in **thousands of dollars**
- Multiple INFOTABLE rows can exist for same CUSIP within one filing (different share classes, put/call)
- SUMMARYPAGE may have fewer rows than COVERPAGE (not all filings have summary)
