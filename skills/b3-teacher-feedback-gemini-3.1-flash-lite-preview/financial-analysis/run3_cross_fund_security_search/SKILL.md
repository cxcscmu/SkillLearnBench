---
name: cross_fund_security_search
description: Searches all funds within a specific quarter to rank holdings for a target security by CUSIP.
---
To identify the top managers for a specific security in Q3:

1. **CUSIP Retrieval**: Use `scripts/search_cusip.py --ticker "PLTR"` to identify the target security's CUSIP.
2. **Aggregated Analysis**: Run `scripts/aggregate_holdings.py --quarter_path /root/2025-q3 --cusip <cusip>` to retrieve a list of all reporting funds and their respective share values for that asset.
3. **Ranking**: Sort the returned list by share value and select the top 3 fund manager names.