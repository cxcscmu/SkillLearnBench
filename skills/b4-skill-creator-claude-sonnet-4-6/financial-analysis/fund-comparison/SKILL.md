---
name: fund-comparison
description: Compare hedge fund holdings between two quarters to identify changes in investment positions. Use this skill when analyzing Q-over-Q changes in fund portfolios, finding top increased/decreased positions, or tracking specific fund activity across reporting periods. Triggers on questions about "change from Q2 to Q3", "increased investment", "top buys/sells", or any cross-quarter 13F comparison.
---

# Fund Quarter-over-Quarter Comparison Skill

## Overview

Compare a fund's holdings between two quarters to find the biggest changes in investment positions by dollar value or share count.

## Step-by-Step Workflow

### Step 1: Get Accession Numbers for Both Quarters

```python
import pandas as pd

def find_fund_accession(quarter_dir, search_term):
    cover = pd.read_csv(f'{quarter_dir}/COVERPAGE.tsv', sep='\t', dtype=str)
    mask = cover['FILINGMANAGER_NAME'].str.contains(search_term, case=False, na=False)
    results = cover[mask][['ACCESSION_NUMBER', 'FILINGMANAGER_NAME', 'ISAMENDMENT']]
    # Prefer non-amended filing, or latest amendment
    return results

q2_acc = find_fund_accession('/root/2025-q2', 'berkshire')
q3_acc = find_fund_accession('/root/2025-q3', 'berkshire')
print("Q2:", q2_acc)
print("Q3:", q3_acc)
```

### Step 2: Load Holdings for Both Quarters

```python
q2_info = pd.read_csv('/root/2025-q2/INFOTABLE.tsv', sep='\t', dtype=str)
q3_info = pd.read_csv('/root/2025-q3/INFOTABLE.tsv', sep='\t', dtype=str)

q2_holdings = q2_info[q2_info['ACCESSION_NUMBER'] == q2_accession][['CUSIP', 'NAMEOFISSUER', 'VALUE', 'SSHPRNAMT']].copy()
q3_holdings = q3_info[q3_info['ACCESSION_NUMBER'] == q3_accession][['CUSIP', 'NAMEOFISSUER', 'VALUE', 'SSHPRNAMT']].copy()
```

### Step 3: Convert Numeric Columns

```python
q2_holdings['VALUE'] = pd.to_numeric(q2_holdings['VALUE'], errors='coerce').fillna(0)
q3_holdings['VALUE'] = pd.to_numeric(q3_holdings['VALUE'], errors='coerce').fillna(0)
q2_holdings['SSHPRNAMT'] = pd.to_numeric(q2_holdings['SSHPRNAMT'], errors='coerce').fillna(0)
q3_holdings['SSHPRNAMT'] = pd.to_numeric(q3_holdings['SSHPRNAMT'], errors='coerce').fillna(0)
```

### Step 4: Aggregate by CUSIP (handle duplicate rows per CUSIP)

```python
q2_agg = q2_holdings.groupby('CUSIP').agg({'VALUE': 'sum', 'SSHPRNAMT': 'sum', 'NAMEOFISSUER': 'first'}).reset_index()
q3_agg = q3_holdings.groupby('CUSIP').agg({'VALUE': 'sum', 'SSHPRNAMT': 'sum', 'NAMEOFISSUER': 'first'}).reset_index()
```

### Step 5: Merge and Calculate Changes

```python
merged = pd.merge(
    q3_agg.rename(columns={'VALUE': 'v_q3', 'SSHPRNAMT': 's_q3'}),
    q2_agg.rename(columns={'VALUE': 'v_q2', 'SSHPRNAMT': 's_q2', 'NAMEOFISSUER': 'name_q2'}),
    on='CUSIP', how='outer'
).fillna(0)

# Use Q3 name where available, else Q2
merged['NAME'] = merged['NAMEOFISSUER'].where(merged['NAMEOFISSUER'] != 0, merged['name_q2'])
merged['value_change'] = merged['v_q3'] - merged['v_q2']
merged['share_change'] = merged['s_q3'] - merged['s_q2']
```

### Step 6: Get Top 5 Increases

```python
# By dollar value increase
top5 = merged.nlargest(5, 'value_change')[['CUSIP', 'NAME', 'v_q2', 'v_q3', 'value_change']]
print(top5)

# Answer: list of CUSIPs
cusips = top5['CUSIP'].tolist()
print("Top 5 CUSIPs:", cusips)
```

## Notes

- VALUE is in thousands of USD in INFOTABLE
- Some holdings may appear in only one quarter (new buys or complete sells)
- `outer` join ensures stocks held in only one quarter are included (value=0 for missing quarter)
- When a fund has amendments, typically use the most recent (highest amendment number)
- Berkshire Hathaway files under "BERKSHIRE HATHAWAY INC" — search for "berkshire"
