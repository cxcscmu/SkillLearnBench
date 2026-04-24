---
name: analyze_13f_filings_and_holdings
description: Guidelines for analyzing 13F filings, finding fund accession numbers, calculating AUM, and counting exact stock holdings by utilizing existing scripts and correctly excluding options.
---
## 1. Utilize Existing Scripts
Before writing custom pandas code from scratch, explore your environment:
- Always check the `scripts/` directory first by running `ls scripts/`.
- There are likely pre-existing Python scripts built specifically for these tasks (e.g., fuzzy searching fund names, analyzing a single fund, and getting total stock holdings/AUM).
- Run these scripts with the `-h` or `--help` flag (e.g., `python scripts/analyze_fund.py --help`) to understand how to leverage them. This saves time and prevents reinventing the wheel.

## 2. Fuzzy Searching for Accession Numbers
To find a fund (e.g., "Renaissance Technologies" or "Berkshire Hathaway"):
- Search the `COVERPAGE` data in the appropriate quarter's directory (`/root/2025-q2/` or `/root/2025-q3/`).
- If a fuzzy search script exists in `scripts/`, use it to extract the correct `accession_number`. Note that accession numbers change between quarters, so you must find the specific accession number for each respective quarter.

## 3. Counting Stocks vs. Total Holdings
When a question specifically asks for the number of **stocks** held by a fund:
- **CRITICAL LOGIC:** Do not simply count all rows in the holding table.
- SEC 13F filings include options derivatives like PUT and CALL. These must be excluded to get the correct stock count.
- If using an existing script, check if it has a flag to filter stocks or exclude options.
- If writing custom Pandas code, load the holdings file (Information Table) and filter out the options using the `putCall` column (or equivalent):

```python
import pandas as pd

# Load the holdings/infotable
df = pd.read_csv("path_to_infotable.csv")

# Filter out Put/Call options to only count true stock holdings
# Options are usually labeled 'PUT' or 'CALL' in the 'putCall' column
if 'putCall' in df.columns:
    stocks_only = df[df['putCall'].isna() | (df['putCall'] == '')]
else:
    stocks_only = df

stock_count = len(stocks_only)
print(f"Number of stocks: {stock_count}")
```

## 4. Calculating AUM
AUM (Assets Under Management) is typically the sum of the `value` column across all holdings for a specific `accession_number`. Ensure you use the provided scripts in `scripts/` to calculate this accurately, or sum the `value` column in the Information Table.