---
name: Filter Vulnerabilities by Severity Level
description: Filter vulnerability records to include only HIGH and CRITICAL severity levels with case-sensitive exact matching.
---

## Filtering Logic

1. **Severity comparison must be case-sensitive**
   - Match exactly: `"HIGH"` or `"CRITICAL"`
   - Do NOT match: `"high"`, `"High"`, `"critical"`, etc.

2. **Implementation**
   ```
   Include vulnerability if:
   severity == "HIGH" OR severity == "CRITICAL"
   ```

3. **Verify before filtering**
   - Extract actual severity values from JSON
   - Check for uppercase/lowercase inconsistency in source data
   - Convert to uppercase if needed: `severity.upper() == "HIGH"`

4. **Validation**
   - Count filtered records
   - Confirm no excluded HIGH/CRITICAL records
   - Confirm no included lower-severity records