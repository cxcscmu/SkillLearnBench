---
name: technical-poster-generator
description: >
  Generate technical exploded-view posters of hardware devices using Python Pillow.
  Use this skill when creating engineering diagrams, exploded-view illustrations,
  hardware layer breakdowns, or technical documentation posters programmatically.
  Triggers on: exploded view, technical poster, hardware diagram, device layers.
---

# Technical Poster Generator

## Approach

Use Python with Pillow (PIL) to draw an exploded-view diagram. Each hardware layer is
rendered as a rounded rectangle or shaped polygon, vertically offset to create the
"exploded" separation effect.

## Exploded-View Construction

### Layer Stack (top to bottom, with vertical gaps)
1. **Outer Casing** — largest footprint, rounded corners, dark fill
2. **Thermal Management Unit** — slightly inset, distinct accent color
3. **PCB (Printed Circuit Board)** — inset further, with circuit-trace detail hints
4. **Battery Pack** — compact rectangle, neutral/dark fill
5. **Interface / Connector Board** — smallest, with highlighted connector points

### Drawing Strategy
- Canvas: 2400×3200px (portrait, print-quality at 300 DPI ≈ 8×10.7 inches)
- Each layer: rounded rectangle with 2-4px border
- Vertical gap between layers: 60-80px to show separation
- Slight horizontal offset or perspective shift (optional) for depth
- Annotation leader lines: thin horizontal lines from layer edge to text labels

### Annotation Pattern
- Draw a thin line (1.5px) from the layer's right edge to a text label
- Use small dots at the line origin on the layer
- Label text: component name + brief spec (e.g., "PCB — 6-Layer FR4")

### Title Block
- Position: top-left corner, with generous padding
- Large bold text for product name
- Smaller subtitle line below (e.g., "Technical Exploded View")

### Python Libraries
- `PIL` / `Pillow` for rendering
- `PIL.ImageDraw` for shapes and lines
- `PIL.ImageFont` for typography (use truetype fonts when available)

### Code Pattern
```python
from PIL import Image, ImageDraw, ImageFont

img = Image.new('RGB', (2400, 3200), background_color)
draw = ImageDraw.Draw(img)

# Draw layers bottom-up so upper layers visually overlap if needed
for layer in reversed(layers):
    draw.rounded_rectangle(layer.bbox, radius=12, fill=layer.color, outline=layer.border)

# Add annotation lines and labels
# Save
img.save('output.png', quality=95)
```
