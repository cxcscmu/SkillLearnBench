---
name: run2_cvss-extraction
description: Advanced robust CVSS extraction logic that correctly falls back across priority sources and handles missing values.
---

# Robust CVSS Score Extraction

Extracting a valid and reliable CVSS (Common Vulnerability Scoring System) score is critical when processing security audits. Scanners often compile scoring metrics from various providers. To guarantee data consistency, it is crucial to establish a fallback strategy across providers, preferring comprehensive databases like NVD over vendor-specific sources like RedHat.

## Priority Strategy
The established priority order for pulling CVSS data from Trivy's JSON reports is:
1. `nvd` (National Vulnerability Database, highly authoritative)
2. `ghsa` (GitHub Security Advisory, reliable for open-source)
3. `redhat` (Vendor specific, but valid for many OS-level vulnerabilities)

## Implementation
You should primarily seek the CVSS v3 score (`V3Score`), falling back to `V2Score` if no `V3Score` exists. If neither score is present or the `CVSS` field is entirely missing, a safe string like `'N/A'` must be returned to avoid crashing the downstream CSV generation.

### Enhanced Code Example

```python
def extract_cvss_score_with_fallback(vuln_dict):
    """
    Safely extract the CVSS score using a fallback strategy.
    Priority: nvd > ghsa > redhat.
    Within each priority, V3Score is preferred, followed by V2Score.
    
    Args:
        vuln_dict (dict): The vulnerability dictionary object parsed from Trivy JSON.
        
    Returns:
        float or str: The CVSS score as a float, or 'N/A' if missing.
    """
    cvss = vuln_dict.get('CVSS', {})
    
    # Priority order for sources
    sources = ['nvd', 'ghsa', 'redhat']
    
    for source in sources:
        if source in cvss:
            # First try CVSS v3 score
            v3_score = cvss[source].get('V3Score')
            if v3_score is not None:
                return float(v3_score)
                
            # Fall back to CVSS v2 score
            v2_score = cvss[source].get('V2Score')
            if v2_score is not None:
                return float(v2_score)
                
    # If no score was found at all, return N/A
    return 'N/A'

# Example usage
sample_vuln = {
    "VulnerabilityID": "CVE-1234",
    "CVSS": {
        "ghsa": {
            "V3Score": 8.5
        }
    }
}
score = extract_cvss_score_with_fallback(sample_vuln)
# score will be 8.5
```

### Type Safety
Explicitly casting the score to `float()` (or checking its type before casting) is a good practice if your CSV parser expects a consistent datatype to apply mathematical thresholds (e.g., `score >= 7.0`), though simply returning the numeric type provided by the JSON parser is usually acceptable.
