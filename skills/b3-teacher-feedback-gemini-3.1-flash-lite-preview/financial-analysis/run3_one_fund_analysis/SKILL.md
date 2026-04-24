---
name: one_fund_analysis
description: Extracts AUM and total holdings count for a specific fund using its accession number and the quarter folder path.
---
To retrieve fund metrics, use the `scripts/one_fund_analysis.py` tool.

1. **Parameters**:
   - `--accession_number`: The ID found via fuzzy search.
   - `--quarter_path`: The directory path (e.g., `/root/2025-q3`).
2. **Unit Handling**: Ensure the final AUM calculation accounts for the 1,000x scaling factor typically used in SEC filings (if the raw data is in thousands, multiply by 1,000 to reach the base unit).
3. **Execution**:
   ```bash
   python3 scripts/one_fund_analysis.py --accession_number <acc_num> --quarter_path /root/2025-q3
   ```