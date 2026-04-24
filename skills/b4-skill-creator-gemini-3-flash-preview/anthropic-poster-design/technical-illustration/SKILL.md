---
name: technical-illustration
description: Techniques and Python script patterns for generating technical exploded-view illustrations, including component layering, annotation leader lines, and isometric projection basics. Use this skill when generating hardware diagrams or exploded views.
---

# Technical Illustration Skill

This skill provides methods for generating technical illustrations, specifically exploded-view diagrams, using Python's Pillow library.

## Components of an Exploded View
An exploded-view diagram separates parts of a whole along a common axis (usually vertical or at an angle) to show internal assembly.

### Layering Strategy
1. **Casing (Top)**: Usually Corporate Dark or Neutral.
2. **Thermal Unit**: Below casing, often using secondary accents.
3. **PCB (Printed Circuit Board)**: Below thermal unit, often using tertiary accents.
4. **Battery**: Below PCB.
5. **Interface (Bottom)**: Connector highlights, primary accents.

### Annotation System
- **Leader Lines**: Thin lines connecting components to labels. Use Muted Mid Gray.
- **Title Block**: Clear, bold heading in the top-left or specified location.

## Python (Pillow) Implementation Pattern

### 1. Canvas Setup
```python
from PIL import Image, ImageDraw, ImageFont

# Initialize canvas with background identity color
canvas = Image.new('RGB', (2000, 2000), '#FAF9F5')
draw = ImageDraw.Draw(canvas)
```

### 2. Drawing Components
Represent hardware parts as stylized geometric shapes (rectangles with rounded corners or trapezoids for perspective).

```python
# Example: Drawing a layer (isometric-style)
def draw_layer(draw, top_y, color, width=600, height=400, offset=100):
    # Stylized trapezoid to simulate perspective
    points = [
        (1000 - width//2, top_y),
        (1000 + width//2, top_y),
        (1000 + width//2 + offset, top_y + height),
        (1000 - width//2 - offset, top_y + height)
    ]
    draw.polygon(points, fill=color, outline='#B0AEA5')
```

### 3. Annotations
```python
# Leader line logic
draw.line([(x1, y1), (x2, y2)], fill='#B0AEA5', width=2)
# Label logic (use Poppins if available, else standard)
draw.text((x2 + 10, y2 - 10), "LAYER NAME", fill='#141413')
```
