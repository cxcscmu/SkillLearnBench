---
name: sec13f-data-format
description: Understanding SEC 13-F filing data structure, TSV format, and key tables for hedge fund analysis
---

# SEC 13-F Data Format and Structure

## Overview
SEC 13-F filings provide quarterly snapshots of large institutional investment holdings. The data is distributed as tab-separated value (TSV) files organized by reporting quarters.

## Key Data Files

### COVERPAGE.tsv
**Purpose**: Fund/Manager information and filing metadata
**Key Columns**:
- `ACCESSION_NUMBER`: Unique identifier for the filing (use to link with holdings)
- `FILINGMANAGER_NAME`: Name of the fund or investment manager
- `REPORTCALENDARORQUARTER`: Reporting date (e.g., "30-JUN-2025")
- `DATEREPORTED`: When the filing was reported
- `REPORTTYPE`: Type of 13-F report

**Usage Example**:
```python
import pandas as pd

# Load fund information
coverpage = pd.read_csv('/root/2025-q3/COVERPAGE.tsv', sep='\t')

# Find a specific fund by name
fund_info = coverpage[coverpage['FILINGMANAGER_NAME'].str.contains('Renaissance', case=False, na=False)]
accession_number = fund_info['ACCESSION_NUMBER'].values[0]
```

### INFOTABLE.tsv
**Purpose**: Detailed holdings data for all funds
**Key Columns**:
- `ACCESSION_NUMBER`: Links to the fund (from COVERPAGE)
- `NAMEOFISSUER`: Company name of the stock
- `CUSIP`: Committee on Uniform Security Identification Procedures code (unique stock identifier)
- `VALUE`: Market value of holdings in thousands (USD)
- `SSHPRNAMT`: Number of shares held (integer)
- `SSHPRNAMTTYPE`: Share amount type (usually "SH" for shares)

**Usage Example**:
```python
# Load all holdings
holdings = pd.read_csv('/root/2025-q3/INFOTABLE.tsv', sep='\t')

# Get holdings for a specific fund
fund_holdings = holdings[holdings['ACCESSION_NUMBER'] == 'specific_accession_number']

# Get count of stocks held
stock_count = len(fund_holdings)

# Find a specific stock
palantir = holdings[holdings['NAMEOFISSUER'].str.contains('PALANTIR', case=False, na=False)]
```

### SUMMARYPAGE.tsv
**Purpose**: Summary-level information per fund
**Key Columns**:
- `ACCESSION_NUMBER`: Fund identifier
- `TABLE_OF_CONTENTS`: Summary metadata
- Other aggregate information

## Data Characteristics

### Value Representation
- All monetary values in INFOTABLE are in **thousands of USD**
- To get actual dollar value: `actual_value = VALUE_FROM_TSV * 1000`
- Share counts are exact integers

### Date Formats
- Dates typically in format "DD-MMM-YYYY" (e.g., "30-JUN-2025")
- Convert using: `pd.to_datetime(df['date_column'], format='%d-%b-%Y')`

### Data Types
```python
# Common data type conversions
df['VALUE'] = pd.to_numeric(df['VALUE'], errors='coerce')
df['SSHPRNAMT'] = pd.to_numeric(df['SSHPRNAMT'], errors='coerce')
df['CUSIP'] = df['CUSIP'].astype(str)
```

## Loading and Initial Data Exploration

```python
import pandas as pd

def load_13f_data(quarter_path):
    """Load all 13-F data for a quarter"""
    return {
        'coverpage': pd.read_csv(f'{quarter_path}/COVERPAGE.tsv', sep='\t'),
        'infotable': pd.read_csv(f'{quarter_path}/INFOTABLE.tsv', sep='\t'),
        'summarypage': pd.read_csv(f'{quarter_path}/SUMMARYPAGE.tsv', sep='\t')
    }

# Usage
q2_data = load_13f_data('/root/2025-q2')
q3_data = load_13f_data('/root/2025-q3')

# Find number of unique funds
num_funds = q3_data['coverpage']['ACCESSION_NUMBER'].nunique()
print(f"Number of unique funds in Q3: {num_funds}")
```

## Common Analysis Patterns

### Get Fund AUM (Assets Under Management)
AUM is typically found in SUMMARYPAGE.tsv:
```python
summarypage = q3_data['summarypage']
# Look for AUM-related fields (may vary by filing)
```

### Get Fund Holdings Count
```python
fund_accession = 'specific_accession_number'
fund_holdings = q3_data['infotable'][q3_data['infotable']['ACCESSION_NUMBER'] == fund_accession]
num_holdings = len(fund_holdings)
```

### Cross-Quarter Comparison
```python
# Get same fund's holdings from two quarters
q2_holdings = q2_data['infotable'][q2_data['infotable']['ACCESSION_NUMBER'] == accession]
q3_holdings = q3_data['infotable'][q3_data['infotable']['ACCESSION_NUMBER'] == accession]

# Merge and compare
comparison = pd.merge(
    q2_holdings[['CUSIP', 'VALUE', 'SSHPRNAMT', 'NAMEOFISSUER']],
    q3_holdings[['CUSIP', 'VALUE', 'SSHPRNAMT']],
    on='CUSIP',
    suffixes=('_q2', '_q3'),
    how='outer'
).fillna(0)

# Calculate changes
comparison['value_change'] = comparison['VALUE_q3'] - comparison['VALUE_q2']
comparison = comparison.sort_values('value_change', ascending=False)
```

## Notes
- ACCESSION_NUMBER is the critical linking key between all tables
- CUSIP is the universal stock identifier
- Multiple funds can have the same stock in their portfolios
- Data is case-sensitive in some fields, use `.str.lower()` or `str.contains(..., case=False)` for case-insensitive matching
