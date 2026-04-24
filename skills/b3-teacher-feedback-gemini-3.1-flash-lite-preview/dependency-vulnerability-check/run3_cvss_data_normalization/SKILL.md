---
name: cvss_data_normalization
description: Logic to parse nested security database objects into a scalar CVSS score for the final CSV report.
---

When processing vulnerability metadata, extract the score using the following hierarchy to ensure data accuracy:
1. **NVD Source**: Look for `cve.cvss.cvssV3.baseScore` within the JSON metadata.
2. **GHSA Source**: Look for `github.cvss.score`.
3. **RedHat Source**: Look for `redhat.cvss.cvss3.score`.

**Transformation Rules:**
- The input is a nested JSON object (e.g., `{"cvssV3": {"baseScore": 8.8, "vectorString": "..."}}`).
- The output must be the scalar value of the `baseScore` or `score` field identified from the highest priority source.
- If no CVSS v3 score is present across all sources, check for `cvssV2` scores before finally returning "N/A".
- Ensure the extracted value is formatted as a decimal string in the final `/root/security_audit.csv` file.