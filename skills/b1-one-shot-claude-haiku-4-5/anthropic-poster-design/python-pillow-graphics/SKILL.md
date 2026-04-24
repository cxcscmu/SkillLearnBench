---
name: python-pillow-graphics
description: Create technical graphics, diagrams, and posters using Python Pillow library with precise color control and typography.
---

# Python Pillow Graphics Generation

## Overview
Pillow (PIL) is the standard Python library for image manipulation and creation. It's ideal for generating technical diagrams, posters, and graphics with precise control over colors, shapes, and text.

## Installation
```bash
pip install Pillow
```

## Key Concepts

### Image Creation
```python
from PIL import Image, ImageDraw, ImageFont

# Create a new image with specific background color
width, height = 1920, 1200
background_color = (240, 240, 240)  # RGB tuple
image = Image.new('RGB', (width, height), background_color)
draw = ImageDraw.Draw(image)
```

### Color Management
- **RGB Tuples**: (R, G, B) where each value is 0-255
- **Hex to RGB Conversion**:
  ```python
  def hex_to_rgb(hex_color):
      hex_color = hex_color.lstrip('#')
      return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
  ```

### Drawing Shapes
```python
# Rectangles
draw.rectangle([x1, y1, x2, y2], fill=color, outline=color, width=stroke)

# Circles/Ellipses
draw.ellipse([x1, y1, x2, y2], fill=color, outline=color)

# Lines
draw.line([(x1, y1), (x2, y2)], fill=color, width=stroke_width)

# Polygons (for 3D perspective)
draw.polygon([(x1, y1), (x2, y2), (x3, y3)], fill=color, outline=color)
```

### Typography
```python
# Load system fonts or TTF files
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size=48)
except:
    font = ImageFont.load_default()

# Draw text
draw.text((x, y), "TEXT", fill=color, font=font, anchor="lm")  # anchor: "lm"=left-middle
```

### Best Practices
- Use anchor parameter for precise text positioning
- Work with RGB tuples consistently throughout
- Set image DPI metadata for high-quality output
- Use layers approach: background → shapes → text → details
- Save as PNG for transparency or high-quality technical graphics

### Saving Output
```python
image.save('/path/to/image.png', quality=95, dpi=(300, 300))
```

## Advanced Techniques

### Creating 3D Perspective
Use polygons and shading to create depth:
```python
# Front face (lighter)
draw.polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], fill=light_color)
# Side face (darker for depth)
draw.polygon([(x2, y2), (x3, y3), (x5, y5), (x6, y6)], fill=dark_color)
```

### Leader Lines with Arrows
```python
def draw_annotation_line(draw, start, end, text, color, font):
    # Line
    draw.line([start, end], fill=color, width=2)
    # Arrow head
    draw.polygon([end, (end[0]-8, end[1]-5), (end[0]-8, end[1]+5)], fill=color)
    # Text
    draw.text((end[0]+10, end[1]), text, fill=color, font=font)
```

## Use Cases
- Technical diagrams and exploded views
- Engineering documentation posters
- System architecture visualizations
- Device component breakdowns
