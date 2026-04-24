---
name: 13f-fund-analysis
description: Analyze SEC 13F fund holdings data given an accession number. Use this skill when you have an accession_number and need to extract fund details including AUM, number of holdings, and detailed position data. Works with Q2 and Q3 2025 filings.
---

# 13F Fund Analysis Skill

## Overview

This skill enables deep analysis of 13F fund filings using accession numbers, extracting key metrics like AUM (Assets Under Management), number of holdings, and detailed stock positions.

## When to Use

Use this skill whenever you need to:
- Extract AUM from a specific fund filing
- Count the number of stocks held by a fund
- Get detailed holdings data (positions, shares, values)
- Analyze a fund's portfolio composition

## Prerequisites

You must have:
- The accession_number from a 13F filing (get this using the 13f-fund-search skill)
- The quarter folder path (/root/2025-q2/ or /root/2025-q3/)

## Analysis Process

### Step 1: Locate the Filing Files

Given an accession_number, find the corresponding filing folder:
```bash
# Accession numbers map to folder names, typically in format:
# /root/2025-q2/[cik]/[accession_folder]/
find /root/2025-q2/ -name "*accession*" -o -name "*.csv" -o -name "*.json"
```

### Step 2: Extract Fund Metadata

Look for files containing:
- **COVERPAGE** - Contains fund name, AUM, manager info
- **HOLDINGS** or **INFOTABLE** - Contains individual stock positions

```python
import pandas as pd
import json
import os

def analyze_fund(quarter_path, accession_number):
    """
    Analyze a fund's holdings and AUM given accession number.

    Args:
        quarter_path: Path to quarter (e.g., '/root/2025-q2/')
        accession_number: The accession number from search

    Returns:
        Dictionary with fund metrics
    """
    results = {
        'accession_number': accession_number,
        'aum': None,
        'number_of_holdings': 0,
        'holdings': [],
        'fund_name': None
    }

    # Search for accession folder
    for root, dirs, files in os.walk(quarter_path):
        # Check if this directory contains our accession number
        if accession_number in root:
            # Look for COVERPAGE
            for file in files:
                if 'COVERPAGE' in file.upper():
                    file_path = os.path.join(root, file)
                    try:
                        if file.endswith('.csv'):
                            df = pd.read_csv(file_path)
                        else:
                            with open(file_path, 'r') as f:
                                df = json.load(f)
                                if isinstance(df, list):
                                    df = pd.DataFrame(df)

                        # Extract AUM - look for columns containing 'aum' or 'assets'
                        for col in df.columns:
                            if 'aum' in col.lower() or 'assets' in col.lower():
                                if len(df) > 0:
                                    results['aum'] = df[col].iloc[0]
                                    break

                        # Extract fund name
                        for col in df.columns:
                            if 'name' in col.lower() or 'fund' in col.lower():
                                if len(df) > 0:
                                    results['fund_name'] = df[col].iloc[0]
                                    break
                    except Exception as e:
                        pass

            # Look for holdings/infotable
            for file in files:
                if 'INFOTABLE' in file.upper() or 'HOLDINGS' in file.upper() or 'POSITION' in file.upper():
                    file_path = os.path.join(root, file)
                    try:
                        if file.endswith('.csv'):
                            holdings_df = pd.read_csv(file_path)
                        else:
                            with open(file_path, 'r') as f:
                                holdings_df = json.load(f)
                                if isinstance(holdings_df, list):
                                    holdings_df = pd.DataFrame(holdings_df)

                        results['number_of_holdings'] = len(holdings_df)
                        results['holdings'] = holdings_df.to_dict('records')
                    except Exception as e:
                        pass

    return results

# Usage
fund_data = analyze_fund('/root/2025-q3/', '0001234567-25-000123')
print(f"AUM: ${fund_data['aum']}")
print(f"Number of holdings: {fund_data['number_of_holdings']}")
```

### Step 3: Parse Holdings Data

Holdings typically include:
- **CUSIP** - Stock identifier
- **Shares** - Number of shares held
- **Value** - Market value of position
- **Stock Name** - Company name

```python
def get_holdings_summary(fund_data):
    """Get top holdings by value."""
    holdings_df = pd.DataFrame(fund_data['holdings'])

    # Sort by value (look for value or market_value column)
    value_col = None
    for col in holdings_df.columns:
        if 'value' in col.lower():
            value_col = col
            break

    if value_col:
        holdings_df = holdings_df.sort_values(by=value_col, ascending=False)

    return holdings_df.head(10)  # Top 10
```

## Output Format

Returns fund analysis object:
```json
{
    "accession_number": "0001234567-25-000123",
    "fund_name": "Renaissance Technologies",
    "aum": 12345000000,
    "number_of_holdings": 245,
    "holdings": [
        {
            "cusip": "000000001",
            "name": "COMPANY NAME",
            "shares": 1000000,
            "value": 50000000
        }
    ]
}
```

## Key Fields to Extract

| Field | Description | Source |
|-------|-------------|--------|
| AUM | Assets Under Management | COVERPAGE |
| Number of Holdings | Count of stock positions | INFOTABLE/HOLDINGS |
| CUSIP | Stock identifier | INFOTABLE/HOLDINGS |
| Shares | Number of shares held | INFOTABLE/HOLDINGS |
| Value | Market value of position | INFOTABLE/HOLDINGS |

## Common Column Names

The 13F files may use varying column names:
- AUM: "AUM", "total_aum", "assets_under_management"
- Holdings: "infotable_entry", "position", "holding"
- Value: "value", "market_value", "value_of_shares"

## Tips

- Check file structure first—CSV vs JSON
- AUM may be in different units (thousands vs actual)
- Holdings count = number of rows in INFOTABLE
- Some funds may have partial holdings data in Q3
