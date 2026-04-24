---
name: Handle NULL and Missing Values in Vulnerability Data
description: Properly handle null, missing, and empty values in vulnerability records with appropriate fallback values.
---

## Fallback Rules

| Field | Missing/Null Handling |
|---|---|
| FixedVersion | Use `"N/A"` (never empty string) |
| CVSS_Score | Use `"N/A"` if no source available |
| Url | Use `"N/A"` if no PrimaryURL or References |
| Title | Use `""` (empty string) or `"N/A"` — verify ground truth |
| Other fields | Include raw value or `"N/A"` per requirement |

## Process

1. Check field existence with `.get()` method
2. Check for `None` or `null` values explicitly
3. Check for empty strings: `if value == ""`
4. Apply appropriate fallback immediately
5. Never allow empty strings where `"N/A"` is required