---
name: Map Trivy JSON Fields to CSV Columns Accurately
description: Correctly identify and extract Trivy vulnerability JSON field names and map them to the required CSV output columns in exact order.
---

## Field Mapping Reference

Map Trivy JSON fields to CSV columns in this exact order:

| CSV Column | Trivy JSON Field | Notes |
|---|---|---|
| Package | `Target` (from metadata) or parse from context | The package name identifier |
| Version | `InstalledVersion` | Not `Version` — use the exact field name |
| CVE_ID | `VulnerabilityID` | Not `CVE_ID` — use Trivy's field name |
| Severity | `Severity` | Case-sensitive: filter for `HIGH` and `CRITICAL` only |
| CVSS_Score | `CVSS[source]['V3Score']` | Use priority: NVD → GHSA → RedHat |
| Fixed_Version | `FixedVersion` | Use `"N/A"` if null/missing, never empty string |
| Title | `Title` or `Description` | Vulnerability title/description text |
| Url | `PrimaryURL` or `References[0]` | Use `PrimaryURL` first, fallback to `References[0]`, then `"N/A"` |

## Process

1. Inspect the actual Trivy JSON output to confirm exact field names
2. Extract each field using correct path (e.g., `vuln.get('VulnerabilityID')`)
3. Verify field names are case-sensitive
4. Apply fallbacks in specified order for URL and CVSS