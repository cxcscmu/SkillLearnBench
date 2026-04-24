---
name: run2_advanced-technical-pillow
description: A skill for advanced technical illustration with Pillow, including complex hardware shapes, cooling fins, and annotation shelf-lines.
---

# Advanced Technical Illustration with Pillow

Technical illustrations require precise geometry and functional visual markers to communicate internal architecture.

## Hardware Detail Primitives

- **Cooling Fins**: Series of thin, parallel rectangles on a base layer.
- **PCB Components**: Grid of varying small rectangles (darker/lighter tones) representing chips.
- **Connectors**: High-contrast, small-scale shapes using the Primary Accent color.

```python
def draw_chips(draw, base_points, count=10):
    # base_points is a list of [top, right, bottom, left] of the PCB
    # Logic to fill with small rectangles
    pass

def draw_cooling_fins(draw, base_y, width, height, color):
    # Logic to draw parallel lines/slats
    pass
```

## Precision Annotation "Shelves"

A "shelf" annotation consists of a diagonal leader line from the object to a specific (x, y), and then a horizontal line ("shelf") where the text sits.

```python
def draw_shelf_annotation(draw, anchor, label, font, line_color="#b0aea5"):
    # anchor: (x, y) on the object
    # shelf_x: predetermined side (e.g., 900 for right side)
    # Logic to draw diagonal then horizontal line
    pass
```

## Layer Spacing

Maintain equal vertical spacing between layers to emphasize the "exploded" nature. Recommended: 150-250 pixels.
Include a "shadow" or "footprint" on the layer below if more depth is needed.
