---
name: cvss-report-generation
description: How to generate security audit reports in CSV format. Use this skill whenever you need to produce a `/root/security_audit.csv` report.
---

# CVSS Report Generation

This skill provides instructions for generating standardized security audit reports in CSV format from scan data.

## CSV Structure

The generated CSV must follow this structure:
`Package,Version,CVE_ID,Severity,CVSS_Score,Fixed_Version,Title,Url`

## Implementation Steps

1. **Prepare Data**: Map the findings from your scan tool output into a consistent object structure.
2. **Handle Missing Values**: For fields like `Fixed_Version`, if not available, record as "N/A".
3. **Format**: Use Python's `csv` library for reliable CSV generation to handle escaping special characters.
4. **Writing**: Output the final content to `/root/security_audit.csv`.

```python
import csv

data = [...] # List of dictionaries

with open('/root/security_audit.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['Package', 'Version', 'CVE_ID', 'Severity', 'CVSS_Score', 'Fixed_Version', 'Title', 'Url'])
    writer.writeheader()
    writer.writerows(data)
```
