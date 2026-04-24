---
name: analyze_fund_holdings_and_aum
description: Retrieve a fund's AUM, stock holding counts, or compare investment changes between two quarters.
---

Use this skill to answer questions about a single fund's financial status (AUM), the count of stocks held, or to find the top increased/decreased positions between a baseline quarter and a target quarter.

**Usage for Single Quarter (AUM & Counts):**
```bash
python3 scripts/one_fund_analysis.py --quarter <YYYY-qX> --accession_number <acc_num>
```

**Usage for Quarterly Comparison (Investment Changes):**
```bash
python3 scripts/one_fund_analysis.py --quarter <target_q> --accession_number <target_acc> --baseline_quarter <prev_q> --baseline_accession_number <prev_acc>
```

**Parameters:**
- `--quarter`: The primary reporting quarter.
- `--accession_number`: The unique ID for the fund in the primary quarter.
- `--baseline_quarter`: (Optional) The previous quarter for comparison.
- `--baseline_accession_number`: (Optional) The unique ID for the fund in the previous quarter.

**Notes:**
- To answer questions about the number of stocks, look specifically for the "stock holdings" count in the output rather than "total holdings" or "other holdings".
- For comparing investment increases, the script will output changes ranked by dollar value.