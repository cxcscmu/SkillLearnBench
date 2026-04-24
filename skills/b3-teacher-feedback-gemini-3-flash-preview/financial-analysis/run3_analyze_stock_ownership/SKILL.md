---
name: analyze_stock_ownership
description: Identify and rank the top fund managers holding a specific stock CUSIP in a given quarter.
---

Use this skill to find which hedge funds are the largest investors in a specific security. This is used for answering questions about top fund managers for a given stock like Palantir.

**Usage:**
```bash
python3 scripts/holding_analysis.py --quarter <YYYY-qX> --cusip <target_cusip>
```

**Parameters:**
- `--quarter`: The quarter to analyze (e.g., `2025-q3`).
- `--cusip`: The unique identifier of the stock obtained from a CUSIP search.

**Output:**
Returns a list of fund managers and their respective share values for that specific stock, ranked from highest to lowest.