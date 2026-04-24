---
name: Extract CVSS Score with Correct Priority
description: Extract CVSS score from vulnerability data using the correct priority order (NVD → GHSA → RedHat) and handle nested JSON structure properly. Use case-insensitive field access and correct JSON path navigation.
---

## Process

1. **Access CVSS nested structure correctly**
   - Check for `vuln['CVSS']` existence
   - Use the exact key names: `'NVD'`, `'GHSA'`, `'RedHat'` (case-sensitive)
   - Access score with `vuln['CVSS'][source]['V3Score']` (not `v3Score` or `score`)

2. **Implement priority-based fallback**
   ```
   For each vulnerability:
   - Try NVD first
   - If NVD missing/null → try GHSA
   - If GHSA missing/null → try RedHat
   - If all missing → return "N/A"
   ```

3. **Handle edge cases**
   - Null or missing CVSS sections
   - Missing score keys within a source
   - Empty string values (treat as missing)

4. **Validate output**
   - CVSS score should be numeric or "N/A"
   - Never use empty strings as fallback