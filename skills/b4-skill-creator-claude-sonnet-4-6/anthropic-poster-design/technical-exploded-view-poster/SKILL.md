---
name: technical-exploded-view-poster
description: >
  How to generate a technical exploded-view hardware poster as a PNG using Python
  (matplotlib + Pillow). Use this skill whenever the user asks for an exploded-view
  diagram, hardware layer diagram, technical product poster, or engineering teardown
  illustration. Triggers on: "exploded view", "exploded-view", "hardware layers",
  "PCB diagram", "technical poster", "engineering poster", "teardown illustration".
---

# Technical Exploded-View Poster (Python / matplotlib)

## Overview

An exploded-view poster stacks hardware layers vertically with a vertical offset per
layer (isometric-style), draws connecting leader lines to annotation labels, and uses
brand-consistent colors for each layer rectangle.

## Layer Stack Convention

List layers bottom-to-top in render order (bottom-most drawn first):

```
Layer 0 (bottom) — Battery
Layer 1          — PCB
Layer 2          — Thermal Unit
Layer 3          — Interface / Connector board
Layer 4 (top)    — Outer Casing
```

## Core Drawing Pattern (matplotlib)

```python
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyArrowPatch
import numpy as np

fig, ax = plt.subplots(figsize=(14, 18))
ax.set_xlim(0, 14)
ax.set_ylim(0, 18)
ax.axis('off')
fig.patch.set_facecolor(IDENTITY_LIGHT)

# Layer definition: (y_center, height, width, x_left, color, label, detail_fn)
LAYERS = [
    {"y": 3.0,  "h": 1.0, "w": 8.0, "x": 3.0, "color": CORPORATE_DARK,   "label": "Outer Casing"},
    {"y": 5.5,  "h": 0.8, "w": 7.2, "x": 3.4, "color": SECONDARY_ACCENT, "label": "Thermal Management Unit"},
    {"y": 7.8,  "h": 0.7, "w": 7.0, "x": 3.5, "color": TERTIARY_ACCENT,  "label": "PCB / Main Board"},
    {"y": 10.0, "h": 1.2, "w": 6.8, "x": 3.6, "color": PRIMARY_ACCENT,   "label": "Interface / Connectors"},
    {"y": 12.5, "h": 0.9, "w": 6.5, "x": 3.75,"color": "#4A4A4A",        "label": "Battery Pack"},
]
```

## Isometric Offset Technique

To create depth illusion, each layer is offset slightly in y AND has a thin "side face"
drawn in a darker shade:

```python
def hex_darken(hex_color, factor=0.7):
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    return f"#{int(r*factor):02X}{int(g*factor):02X}{int(b*factor):02X}"

for layer in LAYERS:
    x, y, w, h = layer['x'], layer['y'], layer['w'], layer['h']
    # Top face
    rect = patches.FancyBboxPatch((x, y), w, h,
        boxstyle="round,pad=0.04", linewidth=1.2,
        edgecolor=MUTED_MID_GRAY, facecolor=layer['color'])
    ax.add_patch(rect)
    # Side face (bottom edge shadow)
    side = patches.FancyBboxPatch((x + 0.15, y - 0.18), w, 0.2,
        boxstyle="square,pad=0", linewidth=0,
        facecolor=hex_darken(layer['color']))
    ax.add_patch(side)
```

## Annotation Leader Lines

Use thin lines in MUTED_MID_GRAY from layer edge to label text:

```python
for layer in LAYERS:
    lx = layer['x'] + layer['w'] + 0.15          # right edge of layer
    ly = layer['y'] + layer['h'] / 2              # vertical center
    label_x = lx + 0.8
    # Leader line
    ax.annotate('', xy=(label_x, ly),
                xytext=(lx, ly),
                arrowprops=dict(arrowstyle='-', color=MUTED_MID_GRAY, lw=0.8))
    # Label text
    ax.text(label_x + 0.1, ly, layer['label'],
            fontfamily='DejaVu Sans', fontsize=9, color=CORPORATE_DARK,
            va='center')
```

## Title Block

```python
# "NOVA" heading in top-left
ax.text(0.5, 16.8, "NOVA",
        fontfamily='DejaVu Sans', fontsize=52, fontweight='bold',
        color=CORPORATE_DARK, va='top')
ax.text(0.5, 16.0, "Technical Exploded-View",
        fontfamily='DejaVu Sans', fontsize=13, color=MUTED_MID_GRAY, va='top')
ax.text(0.5, 15.4, "Edge Device — Internal Architecture",
        fontfamily='DejaVu Sans', fontsize=10, color=MUTED_MID_GRAY, va='top')
```

## Saving

```python
fig.savefig("/root/nova_technical_poster.png", dpi=150,
            bbox_inches='tight', facecolor=IDENTITY_LIGHT)
plt.close(fig)
```

## Checklist

- [ ] At least 5 distinct hardware layers rendered
- [ ] Each layer uses correct brand color per spec
- [ ] Annotation lines in MUTED_MID_GRAY only
- [ ] Title "NOVA" in top-left, bold, Corporate Dark
- [ ] Background is IDENTITY_LIGHT throughout
- [ ] No neon colors, no gradients
- [ ] DPI >= 150 for crisp output
