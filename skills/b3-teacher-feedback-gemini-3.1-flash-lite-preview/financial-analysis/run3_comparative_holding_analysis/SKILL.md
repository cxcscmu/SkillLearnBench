---
name: comparative_holding_analysis
description: Compares holding changes between two quarters for a specific fund to determine investment increases.
---
To determine the top 5 stocks with increased investment, utilize the comparison utility specifically designed for multi-quarter delta analysis.

1. **Tool Selection**: Use `scripts/portfolio_delta.py` instead of the general `holding_analysis.py` to calculate the difference in `(shares * price)` between Q2 and Q3.
2. **Execution**:
   ```bash
   python3 scripts/portfolio_delta.py --q2_path /root/2025-q2 --q3_path /root/2025-q3 --fund_acc_q2 <q2_num> --fund_acc_q3 <q3_num> --metric value
   ```
3. **Logic**: Sort the resulting output by dollar value increase in descending order and extract the top 5 CUSIPs.