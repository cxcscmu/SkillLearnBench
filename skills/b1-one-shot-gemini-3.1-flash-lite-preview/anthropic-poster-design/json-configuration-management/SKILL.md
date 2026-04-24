---
name: json-configuration-management
description: Standardized structure for branding metadata in engineering documentation.
---

### Standard JSON Schema for Branding Metadata
When defining brand assets, use the following structure to ensure consistency across the engineering handbook.

```json
{
  "background_hex": "e6e6e6",
  "corporate_dark_hex": "1a1a1a",
  "primary_accent_hex": "007acc",
  "secondary_accent_hex": "555555",
  "tertiary_accent_hex": "aaaaaa",
  "muted_mid_gray_hex": "888888",
  "applied_heading_font": "Inter"
}
```

### Best Practices
- Always use 6-character hex strings.
- Validate property names against the project-specific schema requirements before writing the file.
- Keep the configuration flat to ensure easy parsing.
