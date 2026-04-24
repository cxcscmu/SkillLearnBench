---
name: run2_cvss-score
description: Extract CVSS v3 scores from Trivy vulnerability data with source priority fallback (NVD > GHSA > RedHat) and handle missing data gracefully.
---

# CVSS Score Extraction from Trivy Data

## CVSS Sources in Trivy Output
Trivy provides CVSS scores from multiple sources in the `CVSS` field:
- **nvd**: National Vulnerability Database (most authoritative)
- **ghsa**: GitHub Security Advisory
- **redhat**: Red Hat security team

Not all sources are present for every vulnerability.

## Recommended Priority: NVD > GHSA > RedHat
NVD is the standard reference. GHSA is widely used for npm/GitHub ecosystems. RedHat is useful as a fallback.

## Python Implementation
```python
def get_cvss_score(vuln):
    """Extract best available CVSS v3 score with source priority fallback."""
    cvss = vuln.get("CVSS") or {}
    for source in ["nvd", "ghsa", "redhat"]:
        entry = cvss.get(source)
        if entry:
            score = entry.get("V3Score")
            if score is not None:
                return score
    return "N/A"
```

## Real-world examples from npm scanning
- CVE-2024-29415 (ip): Only ghsa (8.1) and redhat (9.8) — no NVD score → returns 8.1
- CVE-2022-25883 (semver): All three sources at 7.5 → returns 7.5
- CVE-2026-23745 (tar): Only redhat (8.2) → returns 8.2
