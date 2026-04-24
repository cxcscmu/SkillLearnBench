---
name: cvss-extraction
description: Extract CVSS scores from Trivy JSON output.
---

# Extracting CVSS Scores from Trivy JSON

Trivy outputs vulnerabilities with multiple CVSS scores depending on the source (e.g., NVD, RedHat, GHSA). This skill helps you extract the most relevant score.

## JSON Structure

In the Trivy output, vulnerabilities are nested under `Results[] -> Vulnerabilities[]`. Inside a vulnerability, CVSS information is stored inside the `CVSS` dictionary.

```json
{
  "CVSS": {
    "nvd": {
      "V3Vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
      "V3Score": 9.8
    },
    "redhat": {
      "V3Vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
      "V3Score": 9.8
    },
    "ghsa": {
      "V3Score": 9.8
    }
  }
}
```

## Python Implementation

You can write a Python helper to extract a CVSS score from these sources, preferring NVD if available, followed by GHSA and RedHat, falling back to "N/A" if none are present.

```python
def extract_cvss(vuln):
    cvss_data = vuln.get("CVSS", {})
    # Sources in order of preference
    for source in ["nvd", "ghsa", "redhat", "ubuntu", "debian", "alpine"]:
        if source in cvss_data:
            score = cvss_data[source].get("V3Score")
            if score is not None:
                return score
            # Fallback to V2Score if V3 is not present
            score = cvss_data[source].get("V2Score")
            if score is not None:
                return score
    return "N/A"
```

This snippet ensures robust extraction of CVSS scores for reporting purposes.
