---
name: anthropic-brand-tokens
description: >
  Authoritative reference for Anthropic's official brand color palette, typography,
  and design tokens. Use this skill whenever creating any Anthropic-branded artifact,
  poster, UI, or document that must apply official HEX values for background, casing,
  accents, and annotation colors. Triggers on: "Anthropic brand", "brand colors",
  "corporate dark", "identity light", "primary accent", "secondary accent",
  "tertiary accent", "brand tokens", "muted mid gray", "Anthropic typography".
---

# Anthropic Brand Tokens

## Color Palette

| Token Name              | HEX Value   | Usage                                        |
|-------------------------|-------------|----------------------------------------------|
| Identity Light          | `#F5F0EB`   | Primary background for all branded artifacts |
| Corporate Dark          | `#1A1A1A`   | Outer casings, headers, dark surfaces        |
| Primary Brand Accent    | `#D4621A`   | Key interactions, connector highlights, CTAs |
| Secondary Brand Accent  | `#8B7355`   | Thermal / mid-tone hardware elements         |
| Tertiary Brand Accent   | `#6B8E7F`   | PCB substrate, circuit board surfaces        |
| Muted Mid Gray          | `#9E9E9E`   | Annotation lines, dividers, subtle borders   |

## Typography

| Role            | Font Family         | Notes                                      |
|-----------------|--------------------|--------------------------------------------|
| Heading / Title | `DejaVu Sans`      | Bold weight for product titles like "NOVA" |
| Body / Labels   | `DejaVu Sans`      | Regular weight for annotation text        |

> DejaVu Sans is the reliable cross-platform fallback used in Anthropic engineering
> artifacts when custom font files are not embedded. It provides clean, geometric
> letterforms consistent with Anthropic's minimalist aesthetic.

## Design Principles

- **Low saturation**: All colors are muted; avoid neon, fluorescent, or AI-gradient palettes.
- **Minimalist**: Use whitespace generously; no decorative gradients.
- **Monochromatic accent discipline**: Use only one accent color per layer; do not blend accents.
- **Dark-on-light hierarchy**: Corporate Dark on Identity Light is the primary contrast pairing.
- **Annotation restraint**: Leader lines in Muted Mid Gray only; never colored annotation lines.

## Quick Reference — Python HEX Constants

```python
IDENTITY_LIGHT      = "#F5F0EB"   # poster background
CORPORATE_DARK      = "#1A1A1A"   # outer casing
PRIMARY_ACCENT      = "#D4621A"   # connector / interaction highlights
SECONDARY_ACCENT    = "#8B7355"   # thermal management unit
TERTIARY_ACCENT     = "#6B8E7F"   # PCB substrate
MUTED_MID_GRAY      = "#9E9E9E"   # annotation leader lines
HEADING_FONT        = "DejaVu Sans"
```
