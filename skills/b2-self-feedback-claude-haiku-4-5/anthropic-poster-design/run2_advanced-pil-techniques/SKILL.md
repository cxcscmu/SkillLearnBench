---
name: run2_advanced-pil-techniques
description: Advanced PIL/Pillow techniques for depth effects, sophisticated shapes, and professional visual design
---

# Advanced PIL/Pillow Design Techniques

## Creating Depth & Layering

### Shadow Effects
```python
# Create drop shadow by drawing offset rectangles
def draw_shadow(draw, coords, offset_x=4, offset_y=4, shadow_color=(200, 200, 200)):
    x1, y1, x2, y2 = coords
    # Draw shadow first (behind main shape)
    shadow_coords = (x1 + offset_x, y1 + offset_y, x2 + offset_x, y2 + offset_y)
    draw.rectangle(shadow_coords, fill=shadow_color, outline=None)
    # Then draw main shape on top
```

### Gradient Effects (Simplified)
Since PIL doesn't natively support gradients, use layered semi-transparent rectangles:
```python
from PIL import ImageDraw

# Draw gradient-like effect with stacked rectangles
for i in range(10):
    alpha = 255 * (1 - i/10)  # Fade from 255 to 0
    y_pos = start_y + (i * height // 10)
    # Use grayscale value proportional to alpha
    color = int(200 + alpha // 25)
    draw.rectangle([x1, y_pos, x2, y_pos + height//10], fill=(color, color, color))
```

## Sophisticated Shape Drawing

### Beveled Rectangles (3D Effect)
```python
def draw_beveled_rect(draw, coords, bevel_width=3, light_color=(255,255,255),
                      dark_color=(100,100,100), fill_color=(200,200,200)):
    x1, y1, x2, y2 = coords
    # Draw main rectangle
    draw.rectangle(coords, fill=fill_color, outline=None)
    # Draw light edge (top-left)
    draw.rectangle([x1, y1, x2 - bevel_width, y1 + bevel_width], fill=light_color)
    draw.rectangle([x1, y1, x1 + bevel_width, y2], fill=light_color)
    # Draw dark edge (bottom-right)
    draw.rectangle([x1 + bevel_width, y2 - bevel_width, x2, y2], fill=dark_color)
    draw.rectangle([x2 - bevel_width, y1 + bevel_width, x2, y2], fill=dark_color)
```

### Connector Lines with Arrows
```python
def draw_arrow_line(draw, start, end, color, width=2, arrow_size=10):
    # Draw main line
    draw.line([start, end], fill=color, width=width)

    # Calculate arrow angle
    import math
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    angle = math.atan2(dy, dx)

    # Draw arrow head
    arrow_x = end[0] - arrow_size * math.cos(angle)
    arrow_y = end[1] - arrow_size * math.sin(angle)

    # Create arrow triangle points
    p1 = (end[0], end[1])
    p2 = (int(arrow_x - arrow_size/2 * math.sin(angle)),
          int(arrow_y + arrow_size/2 * math.cos(angle)))
    p3 = (int(arrow_x + arrow_size/2 * math.sin(angle)),
          int(arrow_y - arrow_size/2 * math.cos(angle)))

    draw.polygon([p1, p2, p3], fill=color, outline=color)
```

## Professional Layout Techniques

### Text Bounding Box (for proper spacing)
```python
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

# Center text properly
centered_x = container_center_x - text_width // 2
```

### Component Accent Highlights
```python
# Draw accent stroke on component edge
def highlight_edge(draw, coords, color, width=2, edge='top'):
    x1, y1, x2, y2 = coords
    if edge == 'top':
        draw.rectangle([x1, y1, x2, y1 + width], fill=color)
    elif edge == 'bottom':
        draw.rectangle([x1, y2 - width, x2, y2], fill=color)
    elif edge == 'left':
        draw.rectangle([x1, y1, x1 + width, y2], fill=color)
    elif edge == 'right':
        draw.rectangle([x2 - width, y1, x2, y2], fill=color)
```

## Best Practices

1. **Draw Order**: Shadows first, then fills, then outlines, then highlights
2. **Color Consistency**: Use color functions to ensure palette consistency
3. **Scaling**: Use proportional calculations for responsive layouts
4. **Anti-aliasing**: PIL provides basic anti-aliasing; consider using `SMOOTH` mode
5. **Optimization**: Group related draw calls, minimize coordinate recalculations
