---
name: run2_fund-analysis-pro
description: Advanced fund analysis with share change verification to distinguish between price movement and deliberate investment.
---

## Usage
### Handling Script Bugs
The provided `one_fund_analysis.py` may have bugs in its stock classification list (missing commas). For accurate results, use a custom Python script or manual aggregation:

```python
import pandas as pd
df = pd.read_csv("/root/2025-q3/INFOTABLE.tsv", sep="\t", dtype=str)
df["VALUE"] = df["VALUE"].astype(float)
df["SHARES"] = df["SSHPRNAMT"].astype(float)
# Filter by accession number and aggregate by CUSIP
fund_data = df[df["ACCESSION_NUMBER"] == "XXXXX-XX-XXXXXX"]
summary = fund_data.groupby("CUSIP").agg({"VALUE": "sum", "SHARES": "sum", "NAMEOFISSUER": "first"})
```

### Distinguishing Investment Decisions
"Increased investment" should be verified by checking `SHARE_CHANGE`.
1. Calculate `SHARE_CHANGE = SHARES_q3 - SHARES_q2`.
2. Filter for `SHARE_CHANGE > 0`.
3. Rank by `VALUE_CHANGE`.
