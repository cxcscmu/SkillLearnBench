---
name: run2_cvss-scoring-strategy
description: Strategic CVSS score extraction with multi-source lookup, fallback handling, and NVD/GHSA integration
---

# CVSS Scoring Strategy and Extraction

## Purpose
Implement robust CVSS score extraction with fallback strategies, multi-source validation, and proper handling of missing scores.

## CVSS Score Sources in Priority Order

### 1. Trivy JSON CVSS Data
First check Trivy's embedded CVSS information:

```json
"CVSS": {
  "nvd": {
    "V3Score": 7.5,
    "V3Vector": "CVSS:3.1/AV:N/AC:L/AT:N/PR:N/UI:N/S:U/C:N/I:H/A:N"
  },
  "ghsa": {
    "V3Score": 7.5
  }
}
```

**Extraction Logic:**
```python
def get_cvss_from_trivy(vuln_data):
    """Extract CVSS from Trivy CVSS field"""
    cvss = vuln_data.get("CVSS", {})

    # Priority: NVD v3 > GHSA v3 > Other sources
    if "nvd" in cvss and "V3Score" in cvss["nvd"]:
        return cvss["nvd"]["V3Score"]

    if "ghsa" in cvss and "V3Score" in cvss["ghsa"]:
        return cvss["ghsa"]["V3Score"]

    for source in ["redhat", "ubuntu", "oracle"]:
        if source in cvss and "V3Score" in cvss[source]:
            return cvss[source]["V3Score"]

    return None
```

### 2. NVD (NIST) Database Lookup
When Trivy doesn't have CVSS, construct NVD URL and note for manual lookup:

**NVD URL Format:**
```
https://nvd.nist.gov/vuln/detail/{CVE-ID}
```

**When to Use:**
- Trivy has no CVSS data
- Need v3.1 (most current) CVSS scores
- Severity from GHSA but need NVD CVSS validation

**Extraction Pattern:**
- Look for "Base Score" on NVD page
- CVSS v3.1 preferred over v3.0
- Accept CVSS v2.0 as last resort

### 3. GHSA (GitHub Security Advisory) Lookup
For npm packages, GHSA often has detailed scoring:

**GHSA URL Format (if available):**
```
https://github.com/advisories/{GHSA-ID}
```

**When to Use:**
- Trivy lists VendorIDs with GHSA-* prefix
- Need GitHub-specific assessments
- npm-specific vulnerability context

**Mapping:**
```python
# From Trivy's VendorSeverity codes
vendor_severity_map = {
    0: "LOW",
    1: "MODERATE",
    2: "MEDIUM",
    3: "HIGH",
    4: "CRITICAL"
}
```

### 4. RedHat Advisory Database
For packages affecting Red Hat distributions:

**RedHat URL Format:**
```
https://access.redhat.com/security/cve/{CVE-ID}
```

**When to Use:**
- RedHat vulnerability data available
- Enterprise Linux security context needed
- Legacy vulnerability tracking

## Multi-Source Validation

### Consistency Checking
```python
def validate_cvss_consistency(cvss_score, severity_level):
    """Check CVSS score matches reported severity"""
    try:
        score = float(cvss_score)
    except (ValueError, TypeError):
        return True  # Can't validate if not numeric

    # CVSS thresholds per NIST
    if severity_level == "CRITICAL" and score < 9.0:
        return False  # CRITICAL should be 9.0+
    if severity_level == "HIGH" and score < 7.0:
        return False  # HIGH should be 7.0-8.9

    return True
```

### Fallback Strategy

When CVSS score is completely unavailable:

```python
def get_cvss_with_fallback(vuln_data, cve_id):
    """
    Get CVSS score with multi-level fallback
    Returns: (score, source, confidence)
    """

    # Level 1: Trivy embedded CVSS
    trivy_score = get_cvss_from_trivy(vuln_data)
    if trivy_score:
        return (trivy_score, "trivy_embedded", "high")

    # Level 2: CVSS in references (parsed from URLs)
    refs_score = extract_from_references(vuln_data.get("References", []))
    if refs_score:
        return (refs_score, "references", "medium")

    # Level 3: Infer from severity and vendor codes
    inferred = infer_from_vendor_severity(vuln_data.get("VendorSeverity", {}))
    if inferred:
        return (inferred, "inferred", "low")

    # Level 4: Use severity level as signal
    severity = vuln_data.get("Severity", "")
    if severity == "CRITICAL":
        return ("9.0", "severity_mapping", "minimal")
    elif severity == "HIGH":
        return ("7.5", "severity_mapping", "minimal")

    # No score available
    return ("N/A", "not_available", "none")
```

## Handling Special Cases

### Missing CVSS with Available Severity
- CVSS is informational enhancement, not required
- Severity level (HIGH/CRITICAL) is the hard requirement
- Report "N/A" for CVSS when unavailable
- Do NOT fabricate CVSS scores

### Discrepancies Between Severity and CVSS
- Document the discrepancy
- Use the more conservative assessment
- Example: If CVSS says 6.5 but severity is HIGH, use "N/A" and note discrepancy

### Version-Specific CVSS
Some CVEs have version-specific scoring:
- Report the relevant version's score
- If package version is 7.3.7 and CVSS is for 7.3.x, use it
- Otherwise use the general CVSS v3 score

## CVSS Score Format Standardization

```python
def standardize_cvss_score(score):
    """Format CVSS score for CSV output"""
    if score is None or score == "" or score == "N/A":
        return "N/A"

    try:
        # Convert to float and back to string for consistent formatting
        f_score = float(score)
        if 0 <= f_score <= 10:
            return str(round(f_score, 1))  # One decimal place
        else:
            return "N/A"  # Invalid CVSS range
    except (ValueError, TypeError):
        return "N/A"
```

## Audit Trail for Score Extraction

Track scoring source for audit purposes:
```python
{
    "package": "semver",
    "cve_id": "CVE-2022-25883",
    "cvss_score": "7.5",
    "cvss_source": "trivy_embedded",
    "severity_source": "ghsa",
    "confidence": "high"
}
```

This enables verification and understanding of score derivation.

## Examples

### Example 1: Complete CVSS Available
```json
{
  "VulnerabilityID": "CVE-2022-25883",
  "Severity": "HIGH",
  "CVSS": {
    "nvd": {"V3Score": 7.5},
    "ghsa": {"V3Score": 7.5}
  }
}
```
**Result:** CVSS = 7.5 ✓

### Example 2: No CVSS, Severity Available
```json
{
  "VulnerabilityID": "CVE-2024-29415",
  "Severity": "HIGH",
  "CVSS": {}
}
```
**Result:** CVSS = "N/A" ✓ (Severity is sufficient)

### Example 3: Multiple CVSS Sources
```json
{
  "VulnerabilityID": "CVE-2023-XXXXX",
  "Severity": "CRITICAL",
  "CVSS": {
    "nvd": {"V3Score": 9.8},
    "ghsa": {"V3Score": 9.5}
  }
}
```
**Result:** CVSS = 9.8 (NVD preferred) ✓
