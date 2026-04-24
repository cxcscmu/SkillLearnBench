---
name: pillow-technical-diagrams
description: Create technical poster and diagram images using Pillow (PIL), including shapes, text, lines, and layered composition.
---

# Pillow Technical Diagrams

## Installation
```bash
pip install Pillow numpy --break-system-packages
```

## Core Setup
```python
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Create canvas
W, H = 2400, 3200  # portrait poster
img = Image.new("RGB", (W, H), color="#F5F0E8")
draw = ImageDraw.Draw(img)
```

## Drawing Shapes
```python
# Rectangle with rounded corners (Pillow 9+)
draw.rounded_rectangle([x0,y0,x1,y1], radius=12, fill="#hex", outline="#hex", width=2)

# Ellipse / circle
draw.ellipse([x0,y0,x1,y1], fill="#hex", outline="#hex", width=1)

# Polygon
draw.polygon([(x1,y1),(x2,y2),(x3,y3)], fill="#hex", outline="#hex")

# Line with width
draw.line([(x0,y0),(x1,y1)], fill="#hex", width=2)
```

## Text Rendering
```python
# Load system font (fallback chain)
import os

def load_font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

font_title = load_font(120, bold=True)
draw.text((x, y), "NOVA", fill="#1A1A1A", font=font_title)
```

## Centered / Anchored Text
```python
# Anchor options: "lt" (left-top), "mm" (middle-middle), "rt" (right-top)
draw.text((cx, cy), "label", fill="#hex", font=font, anchor="mm")

# Get bounding box for manual centering
bbox = draw.textbbox((0,0), "text", font=font)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
draw.text((cx - tw//2, cy - th//2), "text", fill="#hex", font=font)
```

## Saving
```python
img.save("/root/output.png", dpi=(300, 300))
```

## Alpha / Compositing
```python
layer = Image.new("RGBA", (W, H), (0,0,0,0))
d = ImageDraw.Draw(layer)
d.rectangle([...], fill=(200,200,200,120))  # semi-transparent
img_rgba = img.convert("RGBA")
img_rgba = Image.alpha_composite(img_rgba, layer)
img = img_rgba.convert("RGB")
```

## Tips
- Use `draw.line` with `width=1` for fine annotation leader lines.
- Build exploded layers from bottom to top in draw order.
- Use `numpy` for computing evenly-spaced offsets along an explode axis.
- For dashed lines, draw segments manually in a loop.
