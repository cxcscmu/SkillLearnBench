---
name: design-params-json
description: >
  How to generate a design_parameters.json file containing the applied HEX color
  values and heading font name used in a branded poster or artifact. Use this skill
  whenever a task requires outputting a machine-readable record of design tokens
  alongside a visual output. Triggers on: "design_parameters.json", "design parameters",
  "applied hex values", "color parameters json", "brand token json output".
---

# Design Parameters JSON Output

## Purpose

After generating a branded visual artifact, output a companion JSON file that records
every applied design token so engineers can reproduce or audit the styling.

## Required JSON Structure

The file must use exactly these keys (no additions, no renames):

```json
{
  "background_hex": "",
  "corporate_dark_hex": "",
  "primary_accent_hex": "",
  "secondary_accent_hex": "",
  "tertiary_accent_hex": "",
  "muted_mid_gray_hex": "",
  "applied_heading_font": ""
}
```

## Population Rules

| Key                   | Value source                                      |
|-----------------------|---------------------------------------------------|
| `background_hex`      | Color used for the poster/page background         |
| `corporate_dark_hex`  | Color used for the outer casing / dark surfaces   |
| `primary_accent_hex`  | Color used for interaction details / highlights   |
| `secondary_accent_hex`| Color used for the Thermal Management Unit        |
| `tertiary_accent_hex` | Color used for the PCB substrate                  |
| `muted_mid_gray_hex`  | Color used for annotation leader lines            |
| `applied_heading_font`| Exact font family string used in the title block  |

## Python Output Snippet

```python
import json

design_params = {
    "background_hex":      IDENTITY_LIGHT,
    "corporate_dark_hex":  CORPORATE_DARK,
    "primary_accent_hex":  PRIMARY_ACCENT,
    "secondary_accent_hex": SECONDARY_ACCENT,
    "tertiary_accent_hex": TERTIARY_ACCENT,
    "muted_mid_gray_hex":  MUTED_MID_GRAY,
    "applied_heading_font": HEADING_FONT,
}

with open("/root/design_parameters.json", "w") as f:
    json.dump(design_params, f, indent=2)
```

## Validation

- All HEX values must start with `#` and be 7 characters (e.g. `#F5F0EB`).
- Font name must be the exact string passed to `fontfamily=` in matplotlib.
- File must be valid JSON parseable by `json.load()`.
