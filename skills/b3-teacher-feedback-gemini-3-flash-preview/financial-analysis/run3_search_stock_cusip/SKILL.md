---
name: search_stock_cusip
description: Find the CUSIP (Committee on Uniform Securities Identification Procedures) identifier for a specific company or stock.
---

Use this skill when you have a company name (e.g., "Palantir") and need its unique CUSIP to perform ownership analysis or lookup holdings.

**Usage:**
```bash
python3 scripts/search_stock_cusip.py --keywords "<company_name>"
```

**Parameters:**
- `--keywords`: The name of the company or stock to search for.

**Output:**
Returns the CUSIP string associated with the stock.