---
name: run2_sec13f_data_loader
description: Load and parse SEC 13-F TSV files with proper data type handling and validation
---

# SEC 13-F Data Loader

## Overview
The SEC 13-F dataset consists of multiple tab-separated value (TSV) files that are linked together using ACCESSION_NUMBER. This skill provides guidance on loading, parsing, and validating these files for financial analysis.

## File Structure and Relationships

### Key Files and Their Purpose

| File | Primary Key | Contents | Key Columns |
|------|------------|----------|------------|
| COVERPAGE.tsv | ACCESSION_NUMBER | Fund filing metadata | ACCESSION_NUMBER, FILINGMANAGER_NAME, REPORTCALENDARORQUARTER, DATEREPORTED |
| INFOTABLE.tsv | ACCESSION_NUMBER, CUSIP | Stock holdings | ACCESSION_NUMBER, CUSIP, NAMEOFISSUER, VALUE, SSHPRNAMT, SSHPRNAMTTYPE |
| SUMMARYPAGE.tsv | ACCESSION_NUMBER | Filing summary | ACCESSION_NUMBER, TABLEVALUETOTAL, TABLEENTRYTOTAL, OTHERINCLUDEDMANAGERSCOUNT |
| OTHERMANAGER.tsv | ACCESSION_NUMBER | Co-managers | ACCESSION_NUMBER, MANAGERNAME |
| SUBMISSION.tsv | ACCESSION_NUMBER | Submission details | ACCESSION_NUMBER, FILER_ID, FILING_DATE |

## Important Data Characteristics

### VALUE Column
- **Location**: INFOTABLE.tsv
- **Units**: **Actual US Dollars (not thousands)**
- **Validation**: Sum of all VALUE entries should match SUMMARYPAGE.TABLEVALUETOTAL exactly
- **Note**: This is critical - do not assume thousands, verify against SUMMARYPAGE

### Date Handling
- Report quarters: "30-JUN-2025" (Q2), "30-SEP-2025" (Q3), "31-DEC-2024" (Q4), etc.
- Use these dates to identify quarters and years
- Format: "DD-MMM-YYYY"

### CUSIP Identifiers
- 9-character security identifiers
- Must be treated as strings (some start with zero)
- Used to link holdings across quarters and funds

## Loading Best Practices

### Efficient Loading
```python
import pandas as pd

# For large files, specify data types to reduce memory and prevent type coercion
dtypes = {
    'ACCESSION_NUMBER': 'str',
    'CUSIP': 'str',
    'VALUE': 'int64',
    'SSHPRNAMT': 'int64'
}

# Use low_memory=False to prevent mixed-type warnings
infotable = pd.read_csv(
    '/root/2025-q3/INFOTABLE.tsv',
    sep='\t',
    dtype=dtypes,
    low_memory=False
)
```

### Validation After Loading
```python
# Verify VALUE sum matches SUMMARYPAGE
summarypage = pd.read_csv('/root/2025-q3/SUMMARYPAGE.tsv', sep='\t')

for accession in infotable['ACCESSION_NUMBER'].unique():
    holdings_value = infotable[infotable['ACCESSION_NUMBER'] == accession]['VALUE'].sum()
    summary_value = summarypage[summarypage['ACCESSION_NUMBER'] == accession]['TABLEVALUETOTAL'].values

    if len(summary_value) > 0:
        assert holdings_value == summary_value[0], f"Value mismatch for {accession}"
```

## Quarter and Year Mapping

Each quarter has its own folder with all TSV files:
- **Q2 2025**: `/root/2025-q2/` (reports for 30-JUN-2025)
- **Q3 2025**: `/root/2025-q3/` (reports for 30-SEP-2025)

Each file in a folder contains data for all funds that reported in that quarter.

## Merging Data

### Linking COVERPAGE to INFOTABLE
```python
# Get fund manager name for each holding
holdings_with_managers = pd.merge(
    infotable,
    coverpage[['ACCESSION_NUMBER', 'FILINGMANAGER_NAME']],
    on='ACCESSION_NUMBER'
)
```

### Searching by Fund Name
```python
# Find accession number by fund manager name
coverpage = pd.read_csv('COVERPAGE.tsv', sep='\t')
fund_row = coverpage[coverpage['FILINGMANAGER_NAME'].str.contains('Renaissance', case=False)]
accession = fund_row['ACCESSION_NUMBER'].values[0]
```

## Performance Considerations

- INFOTABLE.tsv is the largest file (~300+ MB)
- Load with `low_memory=False` to avoid mixed type warnings
- Use indexing on ACCESSION_NUMBER for filtering operations
- Cache loaded dataframes when performing multiple queries

## Common Pitfalls to Avoid

1. **Assuming VALUE is in thousands** - It's not, validate with SUMMARYPAGE
2. **Not handling multiple entries per CUSIP** - Some holdings may appear multiple times (e.g., different PUTCALL or investment discretion)
3. **Ignoring REPORTCALENDARORQUARTER** - Always filter by the correct quarter/date
4. **Forgetting to load with low_memory=False** - INFOTABLE has mixed types
5. **Not validating ACCESSION_NUMBER matches** - When joining tables, verify the join is correct
