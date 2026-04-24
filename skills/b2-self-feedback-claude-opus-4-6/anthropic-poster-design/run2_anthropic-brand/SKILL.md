---
name: run2_anthropic-brand
description: Anthropic official brand colors, typography tokens, and design guidelines extracted from anthropic.com CSS.
---

# Anthropic Brand Design Tokens (Verified)

## Brand Colors — Extracted from anthropic.com CSS Variables

| Role | CSS Variable | HEX | Usage Context |
|------|-------------|-----|---------------|
| Corporate Dark | `--_theme---foreground-primary` | `#141413` | Text, dark surfaces, outer hardware |
| Identity Light | `--_theme---background` | `#E8E6DC` | Warm cream page/poster background |
| Primary Accent | `--_theme---heroes-accent` | `#D97757` | Primary CTA, interaction highlights |
| Secondary Accent | selection highlight | `#CC785C` | Secondary warm accents, thermal tones |
| Tertiary Accent | highlight/badge | `#EDA100` | Gold/amber for tertiary elements |
| Muted Mid Gray | neutral mid | `#87867F` | Subtle lines, annotations, secondary text |
| Secondary Dark | `--_theme---foreground-secondary` | `#30302E` | Secondary text, dark variants |

### Additional Neutrals
- Shadow/depth on cream: `#D5D3C9` (slightly darker cream for subtle shadows)
- Light foreground variants: `rgba(250, 249, 240, 0.3-0.5)`

## Typography

### Heading Font: Copernicus (Darden Studio)
- Editorial serif with humanist proportions
- Used for display headings and titles
- CSS variable: `--serif`
- Fallback rendering: DejaVu Serif Bold (closest available system serif)

### Body Font: Clean sans-serif
- CSS variable: `--sans`
- System rendering: DejaVu Sans

### Size Scale (from CSS clamp values)
- Display XL: ~140px at poster scale (clamp 2.5rem–4rem)
- Display M: ~60px (clamp 1.75rem–2rem)
- Label: ~30px
- Detail: ~24px
- Spec/fine: ~20px

## Design Philosophy
- Warm, low-saturation earth-tone palette
- NO neon, NO high-intensity "AI gradient" effects
- Generous whitespace with clear hierarchy
- Muted annotation systems (thin gray lines)
- Professional, editorial aesthetic
