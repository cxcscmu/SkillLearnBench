---
name: csv-security-report-generation
description: Formatting security audit findings into a standardized CSV format for reporting and compliance.
---

### CSV Structure Requirements
The output must strictly follow the specified column order:
`Package,Version,CVE_ID,Severity,CVSS_Score,Fixed_Version,Title,Url`

### Handling Edge Cases
*   **Missing CVEs**: If a vulnerability has no CVE assigned, use the internal identifier (e.g., GHSA-xxxx-xxxx-xxxx).
*   **Multiple CVEs**: If one dependency has multiple vulnerabilities, each should be a separate row in the CSV.
*   **Missing CVSS**: If the tool does not provide a numeric CVSS score, check the reference URL or mark it based on the severity level if a range is known.
*   **Fix Availability**: If `fixAvailable` is `false` or `null`, the `Fixed_Version` column must explicitly state `N/A`.
*   **Special Characters**: Ensure fields containing commas (like Titles) are properly quoted to maintain CSV integrity.

### Data Sanitization
Ensure that the `CVSS_Score` is a float or string representing the decimal score, and that the `Severity` is capitalized consistently (e.g., "HIGH", "CRITICAL") to meet reporting standards.