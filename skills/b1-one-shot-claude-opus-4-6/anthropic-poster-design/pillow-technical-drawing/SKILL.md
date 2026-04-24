---
name: pillow-technical-drawing
description: Creating technical diagrams and exploded-view illustrations using Python Pillow with geometric primitives and text annotations.
---

# Technical Drawing with Pillow

## Setup

```bash
pip install Pillow
```

## Key Patterns

### Rounded Rectangles (component layers)
```python
from PIL import Image, ImageDraw, ImageFont

img = Image.new('RGB', (1800, 2400), '#F5F4ED')
draw = ImageDraw.Draw(img)

# Rounded rectangle for a component layer
draw.rounded_rectangle([x1, y1, x2, y2], radius=12, fill='#D97757', outline='#141413', width=2)
```

### Exploded-View Layout
- Stack layers vertically with consistent vertical gaps (60-100px)
- Offset each layer slightly on the X-axis for 3D depth illusion
- Use isometric-style parallelogram shapes for depth perception

### Annotation Leader Lines
```python
# Thin annotation line from component to label
draw.line([(comp_x, comp_y), (label_x, label_y)], fill='#B0ADA5', width=1)
# Small circle at the component end
draw.ellipse([comp_x-3, comp_y-3, comp_x+3, comp_y+3], fill='#B0ADA5')
```

### Text Labels
```python
font_heading = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
font_label = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
draw.text((x, y), "NOVA", fill='#141413', font=font_heading)
```

### Isometric 3D Effect with Polygons
```python
# Create parallelogram for isometric top face
top_face = [(x, y), (x+w, y-skew), (x+w+d, y-skew+d), (x+d, y+d)]
draw.polygon(top_face, fill=color, outline='#141413', width=1)
```

### Saving
```python
img.save('output.png', dpi=(300, 300))
```
