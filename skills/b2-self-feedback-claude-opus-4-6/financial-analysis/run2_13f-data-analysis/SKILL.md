---
name: run2_13f-data-analysis
description: Comprehensive guide for analyzing SEC 13-F quarterly filings data (TSV format) including fund lookup, AUM, holdings comparison, and stock investor analysis.
---

# SEC 13-F Data Analysis (Improved)

## Data Files

Each quarter folder contains TSV files:

| File | Purpose | Key Columns |
|------|---------|-------------|
| COVERPAGE.tsv | Fund manager metadata | `ACCESSION_NUMBER`, `FILINGMANAGER_NAME` |
| INFOTABLE.tsv | Individual stock holdings (~300MB) | `ACCESSION_NUMBER`, `NAMEOFISSUER`, `CUSIP`, `VALUE` (x1000), `SSHPRNAMT` (shares) |
| SUMMARYPAGE.tsv | Aggregate stats per filing | `ACCESSION_NUMBER`, `TABLEENTRYTOTAL`, `TABLEVALUETOTAL` (x1000) |

## Important Notes

- **VALUE is in thousands of dollars** — multiply by 1000 for actual dollar amounts
- **TABLEVALUETOTAL is also in thousands** in SUMMARYPAGE
- **CUSIP casing**: INFOTABLE may have mixed-case CUSIPs (e.g., `69608A108` vs `69608a108`). Always normalize: `df['CUSIP'] = df['CUSIP'].str.upper()`
- **Multiple accession numbers**: A single filer (e.g., Berkshire Hathaway) may have multiple filings. Use SUMMARYPAGE to identify the main one (largest TABLEVALUETOTAL).
- **Low memory**: INFOTABLE is large. Use `low_memory=False` or specify `dtype={'CUSIP': str}`.

## Workflow Patterns

### 1. Fuzzy Search for a Fund
```python
from difflib import SequenceMatcher
cover = pd.read_csv('COVERPAGE.tsv', sep='\t', dtype=str)
cover['score'] = cover['FILINGMANAGER_NAME'].apply(
    lambda x: SequenceMatcher(None, search.lower(), str(x).lower()).ratio()
)
best = cover.sort_values('score', ascending=False).iloc[0]
accession = best['ACCESSION_NUMBER']
```

### 2. Get AUM (from SUMMARYPAGE)
```python
summary = pd.read_csv('SUMMARYPAGE.tsv', sep='\t')
row = summary[summary['ACCESSION_NUMBER'] == accession]
aum_thousands = row['TABLEVALUETOTAL'].values[0]
```

### 3. Get Number of Holdings
Use `TABLEENTRYTOTAL` from SUMMARYPAGE or count unique CUSIPs from INFOTABLE (usually identical).

### 4. Compare Holdings Across Quarters
```python
q2_h = info_q2[info_q2['ACCESSION_NUMBER']==acc_q2].groupby('CUSIP')['VALUE'].sum()
q3_h = info_q3[info_q3['ACCESSION_NUMBER']==acc_q3].groupby('CUSIP')['VALUE'].sum()
diff = q3_h.subtract(q2_h, fill_value=0).sort_values(ascending=False)
top5_increased = diff.head(5).index.tolist()  # CUSIPs
```

### 5. Find Top Investors for a Stock
```python
# Find CUSIP by issuer name
matches = info[info['NAMEOFISSUER'].str.contains('NAME', case=False, na=False)]
cusip = matches['CUSIP'].str.upper().mode()[0]
# Aggregate by filing
holders = info[info['CUSIP'].str.upper()==cusip].groupby('ACCESSION_NUMBER')['VALUE'].sum()
top = holders.sort_values(ascending=False).head(3)
# Map to names via COVERPAGE
```

## Disambiguation Tips

- When multiple accession numbers match the same filer, the one with higher `TABLEVALUETOTAL` or more `TABLEENTRYTOTAL` is typically the main 13F-HR filing.
- Some funds file separate confidential treatment requests — filter by `ISCONFIDENTIALOMITTED='N'` if needed.
