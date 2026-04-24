---
name: technical-poster-generation
description: "Guide for generating technical exploded-view posters using Python (PIL/Pillow). Use this skill when creating engineering diagrams, hardware breakdowns, or product teardowns that require precise layer visualization, annotation leader lines, and technical accuracy. Includes methods for drawing components, layering, annotation, and exporting high-quality images."
---

# Technical Poster Generation

## Overview

This skill provides techniques for generating clean, professional technical exploded-view posters using Python's PIL/Pillow library. It covers:

- Setting up canvas and background
- Drawing hardware layers with precise positioning
- Creating annotation leader lines and callout labels
- Implementing component separation/explosion effect
- Exporting to PNG with proper resolution

## Prerequisites

```bash
pip install Pillow
```

Ensure Python 3.8+ is available.

---

## Architecture: Exploded View Layout

### Coordinate System

- **Origin (0, 0)**: Top-left corner
- **Canvas dimensions**: Typically 1200x1600px for A3-equivalent poster at 150 DPI
- **Safe margins**: 60px on all sides (avoid edge clipping)
- **Component spacing**: 80-120px vertical separation between layers for clarity

### Layer Order (Bottom to Top, as Drawn)

1. **Background**: Solid color fill (entire canvas)
2. **Title block**: Top-left positioning
3. **Main component assembly**: Center-aligned, with layers separated vertically
4. **Annotation elements**: Leader lines and labels (drawn last, on top)

---

## Drawing Techniques

### 1. Creating a Clean Canvas

```python
from PIL import Image, ImageDraw, ImageFont

# Create canvas with brand background color
WIDTH, HEIGHT = 1200, 1600
BACKGROUND_HEX = "#F8F8F8"

image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND_HEX)
draw = ImageDraw.Draw(image)
```

### 2. Drawing Hardware Layers

**Technique: Rectangle-based components**

Each layer should be drawn as a simple rectangle (or composite rectangles). Use filled rectangles for solid components, outlined rectangles for transparent/exposed views.

```python
# Example: Drawing a casing layer
casing_color = "#1A1A1A"  # Corporate Dark
x, y = 300, 200  # Top-left position
width, height = 600, 100  # Dimensions

draw.rectangle([x, y, x + width, y + height], fill=casing_color)

# Drawing with border (outline)
draw.rectangle([x, y, x + width, y + height], fill=None, outline=casing_color, width=2)
```

### 3. Annotation Leader Lines

**Technique: Thin lines connecting labels to components**

Leader lines should be:
- **Color**: Muted Mid Gray (#9E9E9E) at 40-60% opacity
- **Width**: 1-2 pixels
- **Style**: Straight lines (no curves unless absolutely necessary)

```python
def draw_leader_line(draw, start_x, start_y, end_x, end_y, gray_hex="#9E9E9E"):
    """Draw a thin annotation leader line."""
    # Note: PIL doesn't natively support opacity in RGB mode
    # Use ImageDraw with line width 1 and semi-transparent composite
    draw.line([(start_x, start_y), (end_x, end_y)], fill=gray_hex, width=1)
```

**For opacity support**, convert to RGBA:

```python
image = image.convert("RGBA")
draw = ImageDraw.Draw(image, "RGBA")
gray_with_opacity = (158, 158, 158, 128)  # #9E9E9E with 50% opacity
draw.line([(x1, y1), (x2, y2)], fill=gray_with_opacity, width=1)
image = image.convert("RGB")  # Convert back for PNG export
```

### 4. Text & Labels

```python
from PIL import ImageFont

# Load font (Inter preferred, fallback to system)
try:
    title_font = ImageFont.truetype("Inter-Bold.ttf", 56)
except IOError:
    title_font = ImageFont.load_default()

# Draw title
draw.text((80, 60), "NOVA", font=title_font, fill="#1A1A1A")

# Draw annotation label
label_font = ImageFont.truetype("Inter-Regular.ttf", 12)
draw.text((850, 250), "Thermal Management Unit", font=label_font, fill="#9E9E9E")
```

---

## Exploded View Structure Example

### Layout Pattern

```
┌──────────────────────────────────────────┐
│ NOVA                                     │  <- Title block (top-left)
│                                          │
├──────────────────────────────────────────┤
│                                          │
│                    Casing                │  <- Layer 1 (top)
│                  [Rectangle]             │
│                                          │
│                 Thermal Unit             │  <- Layer 2 (separated)
│                  [Rectangle]             │
│                                          │
│               PCB Substrate              │  <- Layer 3 (separated)
│                  [Rectangle]             │
│                                          │
│                  Battery                 │  <- Layer 4 (separated)
│                  [Rectangle]             │
│                                          │
│                Interface                 │  <- Layer 5 (bottom)
│                  [Rectangle]             │
│                                          │
└──────────────────────────────────────────┘

Annotations with leader lines point to specific components
```

---

## Step-by-Step Implementation Guide

### Step 1: Define Color Palette

```python
COLORS = {
    "background": "#F8F8F8",
    "corporate_dark": "#1A1A1A",
    "primary_accent": "#0D47A1",
    "secondary_accent": "#1565C0",
    "tertiary_accent": "#42A5F5",
    "muted_gray": "#9E9E9E"
}
```

### Step 2: Calculate Layer Positions

```python
# Define layers with their vertical positions
LAYER_SPACING = 100  # pixels between layers
LAYERS = [
    {"name": "Casing", "y": 250, "color": COLORS["corporate_dark"], "height": 80},
    {"name": "Thermal Unit", "y": 380, "color": COLORS["secondary_accent"], "height": 70},
    {"name": "PCB", "y": 500, "color": COLORS["tertiary_accent"], "height": 60},
    {"name": "Battery", "y": 610, "color": COLORS["primary_accent"], "height": 50},
    {"name": "Interface", "y": 710, "color": COLORS["corporate_dark"], "height": 40},
]
```

### Step 3: Draw Layers & Components

```python
for layer in LAYERS:
    x = 300
    y = layer["y"]
    width = 600
    height = layer["height"]

    draw.rectangle([x, y, x + width, y + height], fill=layer["color"])

    # Optional: subtle outline
    draw.rectangle([x, y, x + width, y + height], outline="#1A1A1A", width=1)
```

### Step 4: Add Annotations

```python
# Define annotations (component_name, x_offset, label_y)
ANNOTATIONS = [
    ("Titanium Casing", 950, 290),
    ("Active Cooling", 950, 415),
    ("Mainboard PCB", 950, 530),
    ("Li-Ion Battery Pack", 950, 645),
    ("USB-C Interface", 950, 750),
]

for label, label_x, label_y in ANNOTATIONS:
    # Draw leader line from annotation to component
    component_x = 900  # Right edge of component area
    component_y = label_y
    draw.line([(component_x, component_y), (label_x - 10, label_y)],
              fill=COLORS["muted_gray"], width=1)

    # Draw label text
    draw.text((label_x, label_y - 8), label, font=label_font, fill=COLORS["muted_gray"])
```

### Step 5: Export

```python
image.save("/root/nova_technical_poster.png", "PNG", quality=95, dpi=(150, 150))
```

---

## Design Checklist

- [ ] Canvas background is the correct brand color
- [ ] All layers are separated vertically for clarity
- [ ] Component colors match the approved brand palette
- [ ] Title is positioned top-left, uses correct font and size
- [ ] Leader lines are thin, subtle, and consistent
- [ ] Labels are legible and properly positioned
- [ ] No drop shadows, gradients, or excessive effects
- [ ] Image is exported at 150+ DPI for print
- [ ] Color values are in hex format and match the brand system

---

## Common Pitfalls

1. **Overcrowding**: Space layers too close together
   - **Fix**: Use 100-120px vertical spacing between components

2. **Low contrast on labels**: Text blends into background
   - **Fix**: Use Corporate Dark (#1A1A1A) for body labels, muted gray only for secondary callouts

3. **Thick leader lines**: Makes design look cluttered
   - **Fix**: Keep leader lines to 1px width

4. **Neon colors or high saturation**: Violates brand minimalism
   - **Fix**: Use only the approved hex palette; avoid brightness adjustments

5. **Missing margins**: Text/components clip at edges
   - **Fix**: Maintain 60px safe margin on all sides
