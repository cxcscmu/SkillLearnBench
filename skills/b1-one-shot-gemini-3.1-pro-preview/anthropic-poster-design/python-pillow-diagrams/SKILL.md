---
name: python-pillow-diagrams
description: Create clean technical posters and diagrams using the Python Pillow library, including shape drawing, typography placement, and annotation.
---

# python-pillow-diagrams

This skill demonstrates how to use the Python `Pillow` library to programmatically generate technical diagrams, exploded views, and presentation-ready posters.

## Installation

Ensure Pillow is installed in your Python environment. For system-wide install in certain Linux environments, you might need to bypass PEP 668:

```bash
pip install Pillow --break-system-packages
```

## Basic Concepts

`Pillow`'s `ImageDraw` module provides methods to render text and geometric primitives like rectangles, polygons, and lines.

### Creating a Base Canvas

```python
from PIL import Image, ImageDraw, ImageFont

# Define dimensions and background color
width, height = 1200, 1600
background_color = "#faf9f5"  # Identity Light

# Create image and drawing context
image = Image.new("RGB", (width, height), background_color)
draw = ImageDraw.Draw(image)
```

### Drawing an Exploded View

Exploded views usually consist of isometric or staggered 2D layers stacked vertically or diagonally. To create a simple vertical exploded view:

```python
layers = [
    {"name": "Casing", "color": "#141413"},
    {"name": "Thermal Unit", "color": "#6a9bcc"},
    {"name": "PCB", "color": "#788c5d"},
    {"name": "Battery", "color": "#d97757"},
    {"name": "Interface", "color": "#141413"},
]

center_x = width // 2
start_y = 400
y_spacing = 200
layer_w, layer_h = 600, 100

# Draw layers from bottom to top (Interface up to Casing)
for i, layer in enumerate(reversed(layers)):
    current_y = start_y + (len(layers) - 1 - i) * y_spacing
    
    # Draw simple isometric-like polygon or simple rectangle
    rect = [
        (center_x - layer_w//2, current_y),
        (center_x + layer_w//2, current_y + layer_h)
    ]
    draw.rectangle(rect, fill=layer["color"])
    
    # Add annotation line and text
    line_color = "#b0aea5"
    draw.line([(center_x + layer_w//2, current_y + layer_h//2), 
               (center_x + layer_w//2 + 100, current_y + layer_h//2)], fill=line_color, width=2)
    # Text (simplified, usually requires loading a font)
    draw.text((center_x + layer_w//2 + 110, current_y + layer_h//2 - 10), layer["name"], fill=line_color)
```

### Loading Fonts

For typography, you can load a system font or default font. Since "Poppins" might not be installed on the system natively, we use default fonts or download the TTF first.

```python
try:
    font = ImageFont.truetype("Poppins-Regular.ttf", 48)
except IOError:
    font = ImageFont.load_default()
    
# Draw heading
draw.text((100, 100), "NOVA", fill="#141413", font=font)
```

### Saving the Image

```python
image.save("nova_technical_poster.png")
```

## Best Practices
1. **Low Saturation/Clean Look:** Use soft neutral backgrounds and reserve accent colors for primary interaction highlights or specific components.
2. **Alignment:** Ensure layers are geometrically aligned (e.g., sharing a center X coordinate).
3. **Typography Consistency:** Apply heading and body styles uniformly.
