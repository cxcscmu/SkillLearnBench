---
name: technical-exploded-view-poster
description: Use this skill when creating a technical exploded-view diagram poster of a hardware device. Covers layout, layer spacing, annotation style, and rendering approach using Python Pillow.
---

# Technical Exploded-View Poster Layout

## Overview

An exploded-view technical poster shows a device's internal layers separated vertically with annotation lines and labels. The style should be minimalist, clean, and engineering-handbook appropriate.

## Poster Dimensions

- **Width**: 1800px
- **Height**: 2400px
- **Orientation**: Portrait

## Layout Structure

```
┌──────────────────────────────────────┐
│ [NOVA title - top left, heading font]│
│                                      │
│         ┌─────────────┐              │
│         │  Layer 1:    │◄── label     │
│         │  Casing      │              │
│         └─────────────┘              │
│              ↕ gap                    │
│         ┌─────────────┐              │
│         │  Layer 2:    │◄── label     │
│         │  Thermal Unit│              │
│         └─────────────┘              │
│              ↕ gap                    │
│         ┌─────────────┐              │
│         │  Layer 3:    │◄── label     │
│         │  PCB         │              │
│         └─────────────┘              │
│              ↕ gap                    │
│         ┌─────────────┐              │
│         │  Layer 4:    │◄── label     │
│         │  Battery     │              │
│         └─────────────┘              │
│              ↕ gap                    │
│         ┌─────────────┐              │
│         │  Layer 5:    │◄── label     │
│         │  Interface   │              │
│         └─────────────┘              │
│                                      │
│  [Footer: "Internal Engineering      │
│   Handbook — Confidential"]          │
└──────────────────────────────────────┘
```

## Layer Definitions & Color Mapping

| Layer | Component | Shape | Fill Color | Outline |
|---|---|---|---|---|
| 1 | Outer Casing | Rounded rectangle (largest) | Corporate Dark (`#141413`) | None |
| 2 | Thermal Management Unit | Rounded rectangle with fin details | Secondary Accent (`#6a9bcc`) | Corporate Dark thin |
| 3 | PCB (Printed Circuit Board) | Rectangle with trace lines | Tertiary Accent (`#788c5d`) | Corporate Dark thin |
| 4 | Battery Pack | Rounded rectangle | Muted Mid Gray (`#b0aea5`) fill, darker outline | Corporate Dark thin |
| 5 | Interface / Connector Module | Rectangle with port cutouts | Primary Accent (`#d97757`) for connector highlights | Corporate Dark thin |

## Rendering Details

### Layer Shapes
- Each layer is a rounded rectangle, centered horizontally
- Layer width decreases slightly from top (casing) to bottom (interface) to suggest enclosure hierarchy
- Vertical gap between layers: 40–60px
- Each layer height: ~80–120px
- Add subtle details: thermal fins (parallel lines) on layer 2, trace patterns on PCB, connector ports on layer 5

### Annotation Lines
- Thin horizontal leader lines from each layer's right edge to a label column
- Line color: Muted Mid Gray (`#b0aea5`)
- Line width: 1.5px
- Label text: body font, Corporate Dark color
- Labels include component name and brief spec (e.g., "PCB — 6-layer FR4 substrate")

### Title Block
- Position: Top-left corner, with left margin ~80px, top margin ~60px
- Text: "NOVA" in heading font (Poppins Bold), large size (96–120px)
- Color: Corporate Dark (`#141413`)
- Subtitle below: "Technical Exploded View" in body font, smaller size
- Subtitle color: Muted Mid Gray (`#b0aea5`)

### Footer
- Bottom-center, small body font
- Text: "ANTHROPIC — Internal Engineering Handbook"
- Color: Muted Mid Gray

## Python Rendering Approach (Pillow)

```python
from PIL import Image, ImageDraw, ImageFont
import json
import os

# 1. Define all brand colors
COLORS = {
    "background": "#faf9f5",
    "corporate_dark": "#141413",
    "primary_accent": "#d97757",
    "secondary_accent": "#6a9bcc",
    "tertiary_accent": "#788c5d",
    "muted_mid_gray": "#b0aea5",
}

# 2. Load fonts (use font discovery from anthropic-brand-typography skill)
# heading_font, heading_font_name = find_font(["Poppins-Bold", "Poppins", "Arial"], size=96)
# body_font, body_font_name = find_font(["Lora-Regular", "Lora", "Georgia", "Arial"], size=28)

# 3. Create canvas
W, H = 1800, 2400
img = Image.new("RGB", (W, H), COLORS["background"])
draw = ImageDraw.Draw(img)

# 4. Draw title "NOVA" top-left
# draw.text((80, 60), "NOVA", font=heading_font, fill=COLORS["corporate_dark"])

# 5. Draw each layer as rounded rectangles with appropriate fills, centered
# 6. Draw annotation leader lines and labels
# 7. Draw footer
# 8. Save
img.save("/root/nova_technical_poster.png", dpi=(300, 300))

# 9. Write design_parameters.json
params = {
    "background_hex": COLORS["background"],
    "corporate_dark_hex": COLORS["corporate_dark"],
    "primary_accent_hex": COLORS["primary_accent"],
    "secondary_accent_hex": COLORS["secondary_accent"],
    "tertiary_accent_hex": COLORS["tertiary_accent"],
    "muted_mid_gray_hex": COLORS["muted_mid_gray"],
    "applied_heading_font": heading_font_name  # "Poppins" or actual fallback
}
with open("/root/design_parameters.json", "w") as f:
    json.dump(params, f, indent=2)
```

## Style Constraints

- **Minimalist**: No drop shadows, no 3D effects, no gradients
- **Low saturation**: All colors from the brand palette are naturally muted
- **No neon / AI gradient styling**: Strictly forbidden
- **Clean lines**: Uniform stroke widths, consistent spacing
- **Exploded-view alignment**: All layers share the same center X axis with vertical separation