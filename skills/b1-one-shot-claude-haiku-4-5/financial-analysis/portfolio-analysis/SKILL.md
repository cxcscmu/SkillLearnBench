---
name: portfolio-analysis
description: Analyzing fund portfolios including AUM extraction, holdings counts, and portfolio composition
---

# Portfolio Analysis for Hedge Funds

## Overview
Portfolio analysis involves extracting fund-level information (AUM, total holdings, composition) from 13-F filings and comparing across time periods.

## Key Metrics

### 1. Assets Under Management (AUM)

**Location**: SUMMARYPAGE.tsv

```python
import pandas as pd

def get_fund_aum(accession_number, summarypage_df):
    """
    Extract AUM for a specific fund
    """
    fund_summary = summarypage_df[
        summarypage_df['ACCESSION_NUMBER'] == accession_number
    ]

    # Look for AUM-related fields in the data
    # Common field names: AUM, ASSETS_UNDER_MANAGEMENT, TOTALASSETS, etc.
    # Check available columns first
    available_cols = fund_summary.columns.tolist()
    print(f"Available columns: {available_cols}")

    # If found, extract and convert to numeric
    for col in available_cols:
        if 'AUM' in col.upper() or 'ASSET' in col.upper() or 'TOTAL' in col.upper():
            try:
                aum_value = pd.to_numeric(
                    fund_summary[col].iloc[0],
                    errors='coerce'
                )
                return aum_value
            except:
                continue

    return None

# Usage
q3_summary = pd.read_csv('/root/2025-q3/SUMMARYPAGE.tsv', sep='\t')
aum = get_fund_aum('specific_accession_number', q3_summary)
```

### 2. Portfolio Holdings Count

```python
def get_holdings_count(accession_number, infotable_df):
    """
    Count the number of stocks held by a fund
    """
    fund_holdings = infotable_df[
        infotable_df['ACCESSION_NUMBER'] == accession_number
    ]
    return len(fund_holdings)

# Usage
q3_infotable = pd.read_csv('/root/2025-q3/INFOTABLE.tsv', sep='\t')
holdings_count = get_holdings_count('specific_accession_number', q3_infotable)
print(f"Renaissance Technologies holds {holdings_count} stocks")
```

### 3. Portfolio Composition

```python
def analyze_portfolio_composition(accession_number, infotable_df):
    """
    Analyze fund's portfolio composition
    """
    fund_holdings = infotable_df[
        infotable_df['ACCESSION_NUMBER'] == accession_number
    ].copy()

    # Ensure VALUE is numeric (in thousands)
    fund_holdings['VALUE'] = pd.to_numeric(fund_holdings['VALUE'], errors='coerce')

    # Calculate statistics
    total_portfolio_value = fund_holdings['VALUE'].sum() * 1000  # Convert to dollars
    num_holdings = len(fund_holdings)
    avg_position = total_portfolio_value / num_holdings if num_holdings > 0 else 0

    # Get top positions
    top_10 = fund_holdings.nlargest(10, 'VALUE')[
        ['NAMEOFISSUER', 'CUSIP', 'VALUE', 'SSHPRNAMT']
    ]
    top_10['VALUE_MILLIONS'] = top_10['VALUE'].astype(float) / 1000

    return {
        'total_value_dollars': total_portfolio_value,
        'num_holdings': num_holdings,
        'avg_position_dollars': avg_position,
        'top_10_positions': top_10,
        'concentration': (top_10['VALUE'].sum() / fund_holdings['VALUE'].sum() * 100)
    }

# Usage
composition = analyze_portfolio_composition('accession_number', q3_infotable)
print(f"Total Portfolio Value: ${composition['total_value_dollars']:,.0f}")
print(f"Number of Holdings: {composition['num_holdings']}")
print(f"Top 10 Positions Concentration: {composition['concentration']:.2f}%")
print("\nTop 10 Positions:")
print(composition['top_10_positions'])
```

### 4. Finding Funds with Specific Stocks

```python
def find_funds_holding_stock(cusip, infotable_df, coverpage_df=None):
    """
    Find all funds holding a specific stock (by CUSIP)
    """
    holdings = infotable_df[infotable_df['CUSIP'] == cusip].copy()

    if len(holdings) == 0:
        return pd.DataFrame()

    # Optional: Enrich with fund names from coverpage
    if coverpage_df is not None:
        holdings = holdings.merge(
            coverpage_df[['ACCESSION_NUMBER', 'FILINGMANAGER_NAME']],
            on='ACCESSION_NUMBER',
            how='left'
        )

    # Sort by value (descending)
    holdings['VALUE'] = pd.to_numeric(holdings['VALUE'], errors='coerce')
    return holdings.sort_values('VALUE', ascending=False)

# Usage
q3_infotable = pd.read_csv('/root/2025-q3/INFOTABLE.tsv', sep='\t')
q3_coverpage = pd.read_csv('/root/2025-q3/COVERPAGE.tsv', sep='\t')

# Find who's holding Palantir (CUSIP: 69608A702)
palantir_holders = find_funds_holding_stock('69608A702', q3_infotable, q3_coverpage)
print(palantir_holders[['FILINGMANAGER_NAME', 'VALUE', 'SSHPRNAMT']])
```

## Complete Fund Analysis Workflow

```python
import pandas as pd

def comprehensive_fund_analysis(accession_number, q_infotable, q_summarypage, q_coverpage):
    """
    Complete analysis of a fund for a quarter
    """
    # Get fund info
    fund_info = q_coverpage[
        q_coverpage['ACCESSION_NUMBER'] == accession_number
    ].iloc[0]

    # Get holdings
    holdings = q_infotable[
        q_infotable['ACCESSION_NUMBER'] == accession_number
    ].copy()

    holdings['VALUE'] = pd.to_numeric(holdings['VALUE'], errors='coerce')

    # Get AUM
    summary = q_summarypage[
        q_summarypage['ACCESSION_NUMBER'] == accession_number
    ]

    analysis = {
        'fund_name': fund_info['FILINGMANAGER_NAME'],
        'accession_number': accession_number,
        'quarter': fund_info['REPORTCALENDARORQUARTER'],
        'num_holdings': len(holdings),
        'total_portfolio_value_thousands': holdings['VALUE'].sum(),
        'top_5_positions': holdings.nlargest(5, 'VALUE')[
            ['NAMEOFISSUER', 'CUSIP', 'VALUE']
        ].to_dict('records')
    }

    return analysis

# Usage
q3_infotable = pd.read_csv('/root/2025-q3/INFOTABLE.tsv', sep='\t')
q3_summarypage = pd.read_csv('/root/2025-q3/SUMMARYPAGE.tsv', sep='\t')
q3_coverpage = pd.read_csv('/root/2025-q3/COVERPAGE.tsv', sep='\t')

analysis = comprehensive_fund_analysis('0000320193-25-000069', q3_infotable, q3_summarypage, q3_coverpage)
print(f"Fund: {analysis['fund_name']}")
print(f"Holdings: {analysis['num_holdings']}")
print(f"Portfolio Value: ${analysis['total_portfolio_value_thousands'] * 1000:,.0f}")
```

## Extracting AUM from SUMMARYPAGE

```python
def extract_aum_from_summarypage(accession_number, summarypage_df):
    """
    Extract AUM from summarypage with fallback methods
    """
    fund_row = summarypage_df[
        summarypage_df['ACCESSION_NUMBER'] == accession_number
    ]

    if fund_row.empty:
        return None

    fund_row = fund_row.iloc[0]

    # Try different possible column names for AUM
    possible_columns = [
        'TABLE_OF_CONTENTS',  # Sometimes contains AUM info
        'AUM',
        'TOTALASSETS',
        'VALUE'
    ]

    # Inspect all columns
    for col in summarypage_df.columns:
        if col in fund_row.index:
            value = fund_row[col]
            if pd.notna(value):
                try:
                    numeric_val = pd.to_numeric(value, errors='coerce')
                    if numeric_val and numeric_val > 1000000:  # Likely an AUM value (> 1M)
                        return numeric_val
                except:
                    pass

    return None
```

## Performance Metrics

```python
def calculate_performance_metrics(accession_q2, accession_q3, infotable_q2, infotable_q3):
    """
    Calculate portfolio changes between quarters
    """
    # Get holdings for both quarters
    holdings_q2 = infotable_q2[infotable_q2['ACCESSION_NUMBER'] == accession_q2].copy()
    holdings_q3 = infotable_q3[infotable_q3['ACCESSION_NUMBER'] == accession_q3].copy()

    # Standardize column names and numeric types
    for df in [holdings_q2, holdings_q3]:
        df['VALUE'] = pd.to_numeric(df['VALUE'], errors='coerce')
        df['SSHPRNAMT'] = pd.to_numeric(df['SSHPRNAMT'], errors='coerce')

    # Merge on CUSIP
    comparison = pd.merge(
        holdings_q2[['CUSIP', 'NAMEOFISSUER', 'VALUE', 'SSHPRNAMT']],
        holdings_q3[['CUSIP', 'VALUE', 'SSHPRNAMT']],
        on='CUSIP',
        how='outer',
        suffixes=('_q2', '_q3')
    ).fillna(0)

    # Calculate changes
    comparison['value_change'] = comparison['VALUE_q3'] - comparison['VALUE_q2']
    comparison['pct_change'] = (comparison['value_change'] / comparison['VALUE_q2'] * 100).replace([float('inf'), float('-inf')], 0)

    return comparison.sort_values('value_change', ascending=False)

# Usage
comparison = calculate_performance_metrics(
    accession_q2, accession_q3,
    q2_infotable, q3_infotable
)
top_increases = comparison[comparison['value_change'] > 0].head(5)
print(top_increases[['NAMEOFISSUER', 'CUSIP', 'value_change']])
```

## Best Practices

1. **Always convert VALUE to numeric**: `pd.to_numeric(df['VALUE'], errors='coerce')`
2. **Remember VALUE is in thousands**: Multiply by 1000 for actual dollar amounts
3. **Handle missing accession numbers**: Some funds may not file all quarters
4. **Validate cusip codes**: Check for null or malformed CUSIPs
5. **Compare matching quarters**: Q2 2025 vs Q3 2025, not Q2 2024 vs Q3 2025
