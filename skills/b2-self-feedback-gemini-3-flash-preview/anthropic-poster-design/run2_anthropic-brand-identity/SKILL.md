---
name: run2_anthropic-brand-identity
description: A skill for managing and applying Anthropic's specific brand identity, including color tokens, typography fallbacks, and technical illustration standards.
---

# Anthropic Brand Identity Management

This skill provides a systematic way to implement Anthropic's brand guidelines in programmatic design.

## Official Brand Tokens (Hex)

- **Identity Light**: `#faf9f5` (Preferred background)
- **Corporate Dark**: `#141413` (Main casing, titles)
- **Primary Accent**: `#d97757` (Action/Connector highlights)
- **Secondary Accent**: `#6a9bcc` (Thermal/Cooling elements)
- **Tertiary Accent**: `#788c5d` (PCB/Internal substrate)
- **Muted Mid Gray**: `#b0aea5` (Leader lines, secondary text)

## Design Principles

- **Swiss Minimalism**: Prioritize whitespace, functional clarity, and grid-based alignment.
- **Low Saturation**: Avoid vibrant "neon" or "AI gradients". Use solid, muted colors or subtle tonal shifts.
- **Precision**: Annotation lines should be thin (1-2px) and use a "shelf" layout (diagonal line to a horizontal shelf for the text).

## Typography Strategy

Official Headings: **Poppins** or **Reckless Neue**.
Functional UI: **Inter** or **Arial**.

```python
# FALLBACK_STRATEGY
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/poppins/Poppins-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "Arial-Bold"
]
```
