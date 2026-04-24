---
name: run2_matplotlib-technical-poster
description: Complete guide to generating polished technical poster PNGs with matplotlib, including typography, pseudo-3D layers, and annotations.
---

# Matplotlib Technical Poster Generation (Refined)

## Installation
```bash
pip3 install matplotlib pillow --break-system-packages
```

## Setup (headless rendering — critical for servers)
```python
import matplotlib
matplotlib.use('Agg')  # MUST be set before importing pyplot
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import json
```

## Figure Setup
```python
fig, ax = plt.subplots(figsize=(14, 20))   # portrait poster
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)
ax.set_xlim(0, 14)
ax.set_ylim(0, 20)
ax.axis('off')
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # remove default margins
```

## Saving (high quality)
```python
plt.savefig('/root/output.png', dpi=200, bbox_inches='tight',
            facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
```
- `dpi=200` → ~2800×4000px for 14×20in figure (better quality than dpi=150)

## Known matplotlib Limitations
| Feature | Issue | Workaround |
|---|---|---|
| `letter_spacing` | Not a Text property → AttributeError | Use spaced chars: `"N O V A"` |
| `fontfamily='Inter'` | May not be installed | Use `'DejaVu Sans'` as fallback |
| `alpha` on patches | Works fine | N/A |
| `linestyle='dotted'` | Use `linestyle=':'` or `(0, (1,3))` | N/A |

## Color Utilities
```python
def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16)/255 for i in (0,2,4))

def lighten(h, factor=0.25):
    r,g,b = hex_to_rgb(h)
    return (r+(1-r)*factor, g+(1-g)*factor, b+(1-b)*factor)

def darken(h, factor=0.25):
    r,g,b = hex_to_rgb(h)
    return (r*(1-factor), g*(1-factor), b*(1-factor))
```

## Pseudo-3D Hardware Layer (three-face box)
```python
def draw_layer(ax, x, y, w, h_front, depth, skew,
               face_color, edge_color='#9B9B9B', z=3):
    """Front face + top face + right face = pseudo-3D box."""
    # Front face
    front = patches.Rectangle((x, y), w, h_front,
        facecolor=face_color, edgecolor=edge_color, linewidth=0.9, zorder=z)
    ax.add_patch(front)
    # Top face
    tx = [x, x+w, x+w+skew, x+skew, x]
    ty = [y+h_front]*2 + [y+h_front+depth]*2 + [y+h_front]
    ax.fill(tx, ty, color=lighten(face_color, 0.28), zorder=z)
    ax.plot(tx, ty, color=edge_color, linewidth=0.8, zorder=z+1)
    # Right side face
    rx = [x+w, x+w+skew, x+w+skew, x+w, x+w]
    ry = [y, y+depth, y+h_front+depth, y+h_front, y]
    ax.fill(rx, ry, color=darken(face_color, 0.22), zorder=z)
    ax.plot(rx, ry, color=edge_color, linewidth=0.8, zorder=z+1)
```

## Leader Line Annotations
```python
def add_leader(ax, tip_x, tip_y, label_x, label_y, label,
               gray='#9B9B9B', text_color='#1A1816', font='DejaVu Sans'):
    """Diagonal leader + horizontal rule + label."""
    ax.plot([tip_x, label_x], [tip_y, label_y],
            color=gray, linewidth=0.65, zorder=6)
    ax.plot([label_x, label_x + 2.0], [label_y, label_y],
            color=gray, linewidth=0.65, zorder=6)
    ax.text(label_x + 2.1, label_y, label,
            fontsize=8.5, va='center', color=text_color,
            fontfamily=font, fontweight='light')
```

## Component Detail Overlays
```python
# PCB chip pads (small rectangles)
for cx in chip_x_positions:
    chip = patches.Rectangle((cx-0.1, pcb_y-0.07), 0.2, 0.14,
        facecolor=PRIMARY, edgecolor=GRAY, linewidth=0.4, zorder=7)
    ax.add_patch(chip)

# Thermal fins (vertical dashed lines within thermal layer)
for fx in np.arange(x_start, x_end, 0.3):
    ax.plot([fx, fx], [y_bottom, y_top],
            color=SECONDARY, linewidth=0.5, alpha=0.5,
            linestyle='--', zorder=5)

# Battery cells (horizontal bands)
for by in np.arange(y_bottom+0.1, y_top, 0.2):
    ax.plot([x_start, x_end], [by, by],
            color=lighten(BATTERY_COLOR, 0.1), linewidth=0.5,
            alpha=0.6, zorder=5)
```
