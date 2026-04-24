---
name: run2_pillow-technical-poster
description: Pillow techniques for technical posters including 3D layers, annotations, and balanced layouts.
---

# Pillow Technical Poster — Improved Patterns

## Layout Balance Strategy
**Problem**: Content clustered at top with empty space below.
**Solution**: Calculate total content height and center vertically, or use full vertical space.

```python
total_content_h = sum(layer_heights) + (num_layers - 1) * gap
start_y = (canvas_h - total_content_h) // 2  # Center vertically
# Or: distribute layers to fill available space between header and footer
```

## Enhanced 3D Layer Rendering

```python
def draw_layer_3d(draw, x, y, w, h, radius, fill, depth=10):
    """3D effect: shadow → side → face."""
    # 1. Drop shadow (soft, offset)
    draw.rounded_rectangle(
        [x+5, y+depth, x+w+5, y+h+depth],
        radius=radius, fill='#D5D3C9'
    )
    # 2. Side edge (darker variant of fill)
    draw.rounded_rectangle(
        [x+2, y+3, x+w+2, y+h+3],
        radius=radius, fill=darken(fill, 0.85)
    )
    # 3. Top face
    draw.rounded_rectangle(
        [x, y, x+w, y+h],
        radius=radius, fill=fill
    )
```

## Annotation Leader Lines — Best Practice
- Start with a small circle (4px radius) at component edge
- Horizontal line in muted gray, width=1
- Consistent right-margin alignment for all labels
- Label: bold font, description: regular font below

## Vertical Assembly Axis
- Dashed line to the left of all layers
- Arrow tips at top and bottom
- Indicates assembly/disassembly direction
- Use segments of 10px line + 10px gap

## Professional Metadata Footer
- Thin separator line
- Company name, document title, classification
- Revision number, view type, distribution notice
- Scale reference bar with tick marks
