---
name: csv-reporting
description: Creating structured CSV reports for security findings.
---

### Purpose
Format security vulnerability data into a CSV file with defined headers.

### Required Fields
- Package name
- Installed version
- CVE ID
- Severity level
- CVSS score
- Fixed version
- Vulnerability title
- Reference URL

### Python Example for CSV generation
```python
import csv

data = [...] # List of dictionaries containing the required fields
headers = ['Package', 'Version', 'CVE_ID', 'Severity', 'CVSS_Score', 'Fixed_Version', 'Title', 'Url']

with open('/root/security_audit.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)
```
