---
name: search_fund_accession_number
description: Fuzzy search the COVERPAGE data to find the specific accession_number for a hedge fund in a given quarter.
---

Use this skill when you need to identify the unique identifier (accession_number) for a fund manager like "Renaissance Technologies" or "Berkshire Hathaway" for a specific reporting period.

**Usage:**
```bash
python3 scripts/search_fund_accession.py --quarter <YYYY-qX> --keywords "<fund_name>"
```

**Parameters:**
- `--quarter`: The target quarter (e.g., `2025-q3`).
- `--keywords`: The name of the fund or keywords to search for.

**Output:**
Returns a list of potential matches. Identify the `accession_number` from the best match to use in subsequent analysis scripts.