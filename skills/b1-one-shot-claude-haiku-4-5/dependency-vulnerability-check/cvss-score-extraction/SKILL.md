---
name: cvss-score-extraction
description: Extract and handle CVSS scores from multiple vulnerability data sources (NVD, GHSA, RedHat) with proper fallback priority.
---

# CVSS Score Extraction

## Overview
CVSS (Common Vulnerability Scoring System) scores quantify vulnerability severity from 0-10. Different sources may provide different scores, requiring intelligent fallback handling.

## Score Sources

### NVD (National Vulnerability Database)
- Official US government vulnerability database
- Provides CVSS v3.0 and v3.1 scores
- Most comprehensive coverage
- URL pattern: `https://nvd.nist.gov/vuln/detail/{CVE_ID}`

### GHSA (GitHub Security Advisory)
- GitHub's vulnerability advisory database
- Integrated with npm ecosystem
- URL pattern: `https://github.com/advisories/{GHSA_ID}`

### RedHat Security
- RedHat-specific vulnerability data
- Often has additional context
- URL pattern: `https://access.redhat.com/security/cve/{CVE_ID}`

## Source Priority

For optimal results, use this priority:
1. NVD CVSS v3.1 (most reliable, modern scoring)
2. NVD CVSS v3.0 (fallback, still reliable)
3. GHSA CVSS (GitHub advisory ecosystem)
4. RedHat CVSS (distribution-specific)
5. N/A (if no score available)

## Data Extraction Pattern

```python
def extract_cvss_score(vuln_data):
    """
    Extract CVSS score with source priority fallback.

    vuln_data: vulnerability object from Trivy or similar
    returns: (score, source) tuple
    """

    # Check NVD first (most authoritative)
    if 'nvd_cvss_v3_1' in vuln_data:
        return (vuln_data['nvd_cvss_v3_1'], 'NVD')

    if 'nvd_cvss_v3_0' in vuln_data:
        return (vuln_data['nvd_cvss_v3_0'], 'NVD')

    # Check GitHub Advisory
    if 'ghsa_cvss' in vuln_data:
        return (vuln_data['ghsa_cvss'], 'GHSA')

    # Check RedHat
    if 'redhat_cvss' in vuln_data:
        return (vuln_data['redhat_cvss'], 'RedHat')

    # No score available
    return ('N/A', 'Unknown')
```

## Handling Missing Scores

When CVSS scores are unavailable:

```python
def get_cvss_with_fallback(cve_id, vuln_sources):
    """
    Query multiple sources for CVSS score.

    cve_id: CVE identifier (e.g., CVE-2021-12345)
    vuln_sources: list of available data sources
    returns: (score_value, source_name)
    """

    for source in vuln_sources:
        score = source.get_cvss(cve_id)
        if score:
            return (score, source.name)

    # Fallback: use severity level as proxy
    return ('N/A', 'No Score Available')
```

## Common Patterns

### Trivy Integration
Trivy may not always include CVSS scores. For missing scores:

```python
def enrich_with_cvss(trivy_results):
    """Enrich Trivy results with CVSS scores from NVD"""
    enriched = []

    for vuln in trivy_results:
        cve_id = vuln['VulnerabilityID']
        score = vuln.get('CVSS', {}).get('nvd', {}).get('V3Score', 'N/A')

        vuln['cvss_score'] = score
        enriched.append(vuln)

    return enriched
```

## Usage

Use this skill when:
- Extracting CVSS scores from vulnerability data
- Need to prioritize scores from multiple sources
- Building vulnerability dashboards or reports
- Creating SLA-based remediation plans (based on CVSS severity)

## Related Skills

- `trivy-vulnerability-scanning`: Source of vulnerability data
- `security-audit-csv-reporting`: Include CVSS scores in reports
