---
name: anthropic-brand-colors
description: Use this skill when you need to apply Anthropic's official brand color palette to any design artifact, poster, or visual. Contains the correct HEX values for all brand color tokens as of 2024.
---

# Anthropic Brand Color Palette

## Core Brand Colors (Official HEX Values)

| Token Name | Role | HEX Value | Description |
|---|---|---|---|
| Identity Light | Backgrounds, canvas | `#faf9f5` | Warm off-white, the default background for all brand materials |
| Corporate Dark | Primary dark / text / casing | `#141413` | Near-black with warm undertone, used for headings, dark UI, device casings |
| Primary Accent | Interaction highlights, connectors, CTAs | `#d97757` | Warm muted orange, the primary brand accent color |
| Secondary Accent | Secondary highlights, thermal units | `#6a9bcc` | Muted steel blue, used for secondary visual accents |
| Tertiary Accent | Tertiary highlights, PCB substrate | `#788c5d` | Muted sage green, used for tertiary visual elements |
| Muted Mid Gray | Annotation lines, secondary text, dividers | `#b0aea5` | Warm mid-gray, low contrast, for subtle UI elements |

## Usage Rules

- **Background**: Always use Identity Light (`#faf9f5`) as the poster/page background unless explicitly overridden.
- **Dark elements** (device casings, heavy borders, heading text): Use Corporate Dark (`#141413`).
- **Primary interactive elements** (connector highlights, key callouts): Use Primary Accent (`#d97757`).
- **Secondary visual accents** (thermal management unit fills): Use Secondary Accent (`#6a9bcc`).
- **Tertiary visual accents** (PCB substrate fills): Use Tertiary Accent (`#788c5d`).
- **Annotation leader lines**: Use Muted Mid Gray (`#b0aea5`) at thin stroke widths (1–1.5px).
- **Avoid**: Neon colors, saturated gradients, "AI gradient" styling. All colors are low-saturation and warm-toned.

## design_parameters.json Structure

When generating the `design_parameters.json` file, use exactly these values:

```json
{
  "background_hex": "#faf9f5",
  "corporate_dark_hex": "#141413",
  "primary_accent_hex": "#d97757",
  "secondary_accent_hex": "#6a9bcc",
  "tertiary_accent_hex": "#788c5d",
  "muted_mid_gray_hex": "#b0aea5",
  "applied_heading_font": "Poppins"
}
```

If Poppins is not available on the system and a fallback is used, update `applied_heading_font` to the actual fallback font name that was applied (e.g., "Arial").