---
name: run2_cvss-score-extraction
description: Extract CVSS v3 scores from Trivy vulnerability JSON with source priority (NVD > GHSA > RedHat) and fallback to N/A.
---

# CVSS Score Extraction (Round 2)

## Priority Order
NVD V3Score → GHSA V3Score → RedHat V3Score → N/A

Do NOT fall back to V2Score — severity labels (HIGH/CRITICAL) come from Trivy's own assessment and are already correct; we only need the numeric score for reporting.

## Canonical Implementation

```python
def get_cvss_score(vuln):
    """
    Extract CVSS v3 score with source priority: NVD > GHSA > RedHat.
    Returns float score or string 'N/A'.
    """
    cvss = vuln.get('CVSS', {})
    if not isinstance(cvss, dict):
        return 'N/A'
    for source in ['nvd', 'ghsa', 'redhat']:
        entry = cvss.get(source, {})
        if isinstance(entry, dict):
            score = entry.get('V3Score')
            if score is not None and isinstance(score, (int, float)):
                return score
    return 'N/A'
```

## Real-World Examples from This Task

| CVE | NVD | GHSA | RedHat | Result |
|-----|-----|------|--------|--------|
| CVE-2024-29415 (ip) | - | 8.1 | 9.8 | **8.1** (GHSA wins, NVD absent) |
| CVE-2022-25883 (semver) | 7.5 | 7.5 | 7.5 | **7.5** (NVD wins) |
| CVE-2026-23745 (tar) | - | - | 8.2 | **8.2** (RedHat only) |

## Notes
- Source keys in Trivy JSON are lowercase: `nvd`, `ghsa`, `redhat`
- Only `V3Score` field is relevant (not `V3Vector`)
- When NVD is absent, GHSA is usually the next best source
