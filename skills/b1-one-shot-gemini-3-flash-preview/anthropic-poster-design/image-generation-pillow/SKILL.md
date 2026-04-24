---
name: image-generation-pillow
description: Technical image generation using Python's Pillow library. Use this when you need to programmatically create diagrams, posters, or technical drawings.
---

## Overview
Pillow (PIL) is a robust library for image processing and creation in Python. It's ideal for generating technical diagrams, exploded views, and annotated posters.

## Installation
Ensure `Pillow` is installed in your environment:
```bash
pip install Pillow
```

## Usage Patterns

### Basic Canvas Setup
```python
from PIL import Image, ImageDraw, ImageFont

# Create a blank canvas
width, height = 1200, 1600
background_color = (250, 249, 245)  # Anthropic Identity Light
image = Image.new('RGB', (width, height), background_color)
draw = ImageDraw.Draw(image)
```

### Drawing Technical Shapes
Use `draw.polygon`, `draw.rectangle`, and `draw.line` to create exploded views. Parallelograms can represent layered hardware components.

```python
def draw_hardware_layer(draw, top_left, size, color, offset=20):
    # top_left: (x, y)
    # size: (w, h)
    # color: (r, g, b)
    # Draw a 3D-like box
    x, y = top_left
    w, h = size
    # Base rectangle
    draw.rectangle([x, y, x + w, y + h], fill=color, outline=(20, 20, 19), width=2)
```

### Exploded View Strategy
To create an exploded view, stack layers vertically with a consistent Y-offset and use leader lines for annotations.

```python
layers = [
    {"name": "Casing", "color": (20, 20, 19)},
    {"name": "Thermal Unit", "color": (106, 155, 204)},
    {"name": "PCB", "color": (120, 140, 93)},
    {"name": "Battery", "color": (176, 174, 165)},
    {"name": "Interface", "color": (217, 119, 87)}
]

for i, layer in enumerate(layers):
    draw_hardware_layer(draw, (300, 200 + i * 200), (600, 100), layer['color'])
```

### Annotations and Typography
```python
# Load a font (ensure the font file exists or use a default)
try:
    font_heading = ImageFont.truetype("Poppins-Bold.ttf", 48)
except:
    font_heading = ImageFont.load_default()

draw.text((50, 50), "NOVA", fill=(20, 20, 19), font=font_heading)
```

## Best Practices
- Use high DPI (e.g., 300) for print-quality posters (multiply width/height accordingly).
- Use `ImageDraw.line` with specific widths for leader lines.
- Antialias lines by drawing at 2x size and resizing down.
