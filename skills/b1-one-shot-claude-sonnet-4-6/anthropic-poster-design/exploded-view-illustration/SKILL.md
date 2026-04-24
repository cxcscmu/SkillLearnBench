---
name: exploded-view-illustration
description: Techniques for drawing isometric or orthographic exploded-view hardware diagrams programmatically using Pillow, with annotation leader lines and layer separation.
---

# Exploded-View Illustration Technique

## Concept
An exploded-view diagram shows the internal components of a device separated along a common axis (usually vertical for portrait posters), with leader lines and labels identifying each component.

## Layout Strategy
```
Poster (portrait, e.g. 2400x3200)
  ├── Title block (top-left)
  ├── Exploded component stack (center)
  │   ├── Layer 5: Top Casing        ← highest Y offset (top)
  │   ├── Layer 4: Thermal Unit
  │   ├── Layer 3: PCB Board
  │   ├── Layer 2: Battery Pack
  │   └── Layer 1: Interface / Bottom ← lowest (bottom)
  └── Legend / spec block (bottom)
```

## Isometric Slab Drawing (Pillow)
Each hardware layer is drawn as a parallelogram/trapezoid to suggest 3D depth:

```python
def draw_slab(draw, cx, cy, w, h, depth, fill, outline, line_w=2):
    """
    Draw an isometric rectangular slab centered at (cx, cy).
    w = width, h = thickness (vertical), depth = isometric depth offset
    """
    # Top face (parallelogram)
    top = [
        (cx - w//2,          cy - h//2),
        (cx + w//2,          cy - h//2),
        (cx + w//2 + depth,  cy - h//2 - depth//2),
        (cx - w//2 + depth,  cy - h//2 - depth//2),
    ]
    # Front face
    front = [
        (cx - w//2, cy - h//2),
        (cx + w//2, cy - h//2),
        (cx + w//2, cy + h//2),
        (cx - w//2, cy + h//2),
    ]
    # Right side face
    right = [
        (cx + w//2,          cy - h//2),
        (cx + w//2 + depth,  cy - h//2 - depth//2),
        (cx + w//2 + depth,  cy + h//2 - depth//2),
        (cx + w//2,          cy + h//2),
    ]
    # Draw back-to-front
    draw.polygon(top,   fill=lighten(fill), outline=outline, width=line_w)
    draw.polygon(right, fill=darken(fill),  outline=outline, width=line_w)
    draw.polygon(front, fill=fill,          outline=outline, width=line_w)
```

## Layer Separation (Explode Axis)
```python
import numpy as np

layers = ["Interface", "Battery", "PCB", "Thermal Unit", "Casing"]
n = len(layers)
explode_gap = 120        # px between layers
center_x = poster_w // 2
base_y = poster_h // 2 + (n * explode_gap) // 2

for i, name in enumerate(layers):
    cy = base_y - i * (slab_height + explode_gap)
    draw_slab(draw, center_x, cy, ...)
```

## Annotation Leader Lines
```python
def draw_leader(draw, slab_right_x, slab_cy, label_x, label_y, color, font):
    """
    Draw an L-shaped leader line from the slab edge to a label.
    """
    elbow_x = label_x - 40
    draw.line([(slab_right_x, slab_cy), (elbow_x, slab_cy)],   fill=color, width=1)
    draw.line([(elbow_x, slab_cy),      (elbow_x, label_y)],   fill=color, width=1)
    draw.line([(elbow_x, label_y),      (label_x, label_y)],   fill=color, width=1)
    # Small dot at attachment point
    r = 4
    draw.ellipse([slab_right_x-r, slab_cy-r, slab_right_x+r, slab_cy+r], fill=color)
```

## Color Utilities
```python
def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def lighten(hex_color, factor=0.25):
    r,g,b = hex_to_rgb(hex_color)
    r = int(r + (255-r)*factor)
    g = int(g + (255-g)*factor)
    b = int(b + (255-b)*factor)
    return (r,g,b)

def darken(hex_color, factor=0.25):
    r,g,b = hex_to_rgb(hex_color)
    return (int(r*(1-factor)), int(g*(1-factor)), int(b*(1-factor)))
```

## PCB Detail Elements
```python
def draw_pcb_traces(draw, cx, cy, w, h, color):
    """Draw simple trace lines on the PCB top face."""
    for x_offset in range(-w//2+20, w//2-20, 30):
        draw.line([(cx+x_offset, cy-h//2-2), (cx+x_offset, cy-h//2-40)], fill=color, width=1)
    # Connector pads
    for x_offset in [-80, 0, 80]:
        x = cx + x_offset
        y = cy - h//2 - 5
        draw.rectangle([x-8, y-8, x+8, y+8], fill=color)
```

## Minimalist Styling Tips
- Use `outline` color one shade darker than `fill` for depth without harshness.
- Keep `depth` offset at 15-25% of `w` for subtle isometric effect.
- Avoid gradients; use flat fills with face-shading for minimalist look.
- Annotation text: uppercase, 24-32px, letter-spaced, aligned right of the device.
