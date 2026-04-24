---
name: anthropic-brand-tokens
description: Anthropic official brand color palette, typography standards, and design tokens for consistent brand application.
---

# Anthropic Brand Tokens

## Color Palette

### Core Identity Colors
| Token | Name | HEX | Usage |
|-------|------|-----|-------|
| `--color-bg-light` | Identity Light | `#F5F0E8` | Primary background, light surfaces |
| `--color-corporate-dark` | Corporate Dark | `#1A1A1A` | Primary text, outer casing, headings |
| `--color-mid-gray` | Muted Mid Gray | `#8C8C8C` | Annotation lines, secondary text |

### Brand Accent Colors
| Token | Name | HEX | Usage |
|-------|------|-----|-------|
| `--color-accent-primary` | Primary Brand Accent | `#C96442` | CTAs, interaction highlights, connectors |
| `--color-accent-secondary` | Secondary Brand Accent | `#8B9E8E` | Thermal/secondary hardware, calm areas |
| `--color-accent-tertiary` | Tertiary Brand Accent | `#6B7FA3` | PCB substrate, informational elements |

### Supporting Tones
| Token | Name | HEX |
|-------|------|-----|
| Warm Off-White | Surface / Card | `#FAF8F3` |
| Soft Divider | Rule / Border | `#DDD8CE` |
| Deep Charcoal | Dark Variant | `#2D2D2D` |

## Design Principles
- **Low-saturation**: Desaturated, muted tones. No neon, no AI-gradient blues/purples.
- **Minimalist**: Generous whitespace, clean geometry.
- **Warm Neutral Base**: Cream/off-white background (Identity Light) as the canvas.
- **Monochromatic Accents**: Accents are desaturated earth/slate tones, not vivid.

## Typography

### Primary Font Stack
- **Heading / Display**: `Styrene A` (Anthropic proprietary) → fallback `"GT Walsheim"` → `"Inter"` → `"Liberation Sans"`
- **Body / Label**: Same stack at smaller sizes
- **Monospace / Technical**: `"IBM Plex Mono"` → `"Courier New"`

### Font Weights
- Display title: **Bold / 700**
- Section labels: **SemiBold / 600**
- Body / annotations: **Regular / 400**

### System Font Fallbacks (Linux)
When proprietary fonts are unavailable, use:
```python
HEADING_FONT_NAME = "DejaVu Sans"  # or "Liberation Sans"
font_paths = {
    "bold":    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "regular": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
}
```

## Brand Do / Don't
- Do: Use Identity Light (`#F5F0E8`) as the poster background.
- Do: Pair Corporate Dark (`#1A1A1A`) for primary typography.
- Do: Keep accents muted and earthy.
- Don't: Use neon, electric blue, or high-saturation gradients.
- Don't: Mix more than 3 accent colors in a single composition.
- Don't: Use white (`#FFFFFF`) as background — use Identity Light instead.
