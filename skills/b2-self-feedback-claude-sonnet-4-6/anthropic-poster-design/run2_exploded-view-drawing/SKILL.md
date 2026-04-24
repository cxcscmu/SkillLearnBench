---
name: run2_exploded-view-drawing
description: Production-ready technique for technical exploded-view hardware diagrams in matplotlib, with layer details, annotations, and title blocks.
---

# Technical Exploded-View Drawing (Refined)

## Concept
An exploded-view diagram separates hardware components along a vertical axis to show
internal structure. Each layer gets equal spacing ("explosion gap") between them,
with a central dashed axis line and annotation leaders pointing to layer labels.

## Layout Geometry
```
         ←── LW=8.0 ──→  ←SKEW→
         ┌───────────────┐╲
         │  Top Casing   │ ╲  ← top face
         └───────────────┘  ╲
                             ╲  ← right face
         [gap = 2.2 units]

         ┌───────────────┐╲
         │  Thermal Unit │ ╲
         └───────────────┘  ╲

         ... (PCB, Battery, Interface)

LX=1.8: left edge x-position
LW=8.0: layer width
SKEW=1.2: 3D depth perspective offset
DEPTH=0.4: face height of perspective top
```

## Complete Layer Stack
```python
# y_bottom, h_front, depth, face_color, label
LAYERS = [
    (15.2, 0.85, 0.45, CORP_DARK,     "Top Casing · ABS + Mg Alloy"),
    (12.2, 0.80, 0.40, SECONDARY,     "Thermal Unit · Vapor Chamber"),
    ( 9.2, 0.65, 0.38, TERTIARY,      "Main PCB · 6-Layer FR4"),
    ( 6.2, 0.75, 0.38, BATTERY_COLOR, "Battery Pack · 7400 mAh"),
    ( 3.2, 0.85, 0.45, CORP_DARK,     "Interface · I/O + USB-C"),
]
```

## Explosion Axis Line
```python
axis_x = LX + LW/2 + SKEW/2  # center of the 3D volume
ax.plot([axis_x, axis_x], [2.8, 16.5],
        color=MID_GRAY, linewidth=0.6, linestyle=':', zorder=2, alpha=0.5)
# Arrow caps at each end
ax.annotate('', xy=(axis_x, 17.0), xytext=(axis_x, 16.5),
            arrowprops=dict(arrowstyle='->', color=MID_GRAY, lw=0.7))
ax.annotate('', xy=(axis_x, 2.2), xytext=(axis_x, 2.8),
            arrowprops=dict(arrowstyle='->', color=MID_GRAY, lw=0.7))
ax.text(axis_x + 0.15, 17.1, "AXIS", fontsize=6.5, color=MID_GRAY,
        fontfamily=FONT, va='bottom')
```

## PCB Detail Layer
```python
pcb_y_mid = 9.2 + 0.65/2
# Trace lines across PCB
for t_off in [-0.12, 0.0, 0.12]:
    ax.plot([LX+0.3, LX+LW-0.3], [pcb_y_mid+t_off]*2,
            color=PRIMARY, linewidth=0.4, alpha=0.35, zorder=6)
# Connector pads (circles)
for cx in [2.8, 3.6, 4.8, 6.2, 7.5, 8.4]:
    ax.add_patch(patches.Circle((cx, pcb_y_mid), 0.11,
        facecolor=PRIMARY, edgecolor=MID_GRAY, linewidth=0.5, zorder=7))
# IC chips (small rectangles)
for chip_x, chip_w, chip_h in [(3.0, 0.7, 0.35), (5.5, 1.0, 0.4), (7.2, 0.6, 0.3)]:
    ax.add_patch(patches.Rectangle((chip_x, pcb_y_mid-chip_h/2), chip_w, chip_h,
        facecolor=darken(TERTIARY, 0.3), edgecolor=MID_GRAY, linewidth=0.5, zorder=7))
```

## Thermal Unit Detail
```python
# Fin array (vertical dashed lines inside thermal layer)
for fin_x in np.arange(LX+0.4, LX+LW-0.2, 0.28):
    ax.plot([fin_x, fin_x], [12.2, 12.2+0.80],
            color=darken(SECONDARY, 0.15), linewidth=0.55,
            alpha=0.55, linestyle='--', zorder=5)
```

## Battery Detail
```python
# Battery cell horizontal bands
for cell_y in np.arange(6.2+0.12, 6.2+0.75, 0.18):
    ax.plot([LX+0.3, LX+LW-0.3], [cell_y]*2,
            color=darken(BATTERY_COLOR, 0.1), linewidth=0.6, alpha=0.5, zorder=5)
```

## Interface Layer Detail
```python
# I/O port cutouts
for port_x in [2.3, 3.8, 5.2, 7.0, 8.5]:
    ax.add_patch(patches.Rectangle((port_x, 3.2+0.25), 0.6, 0.35,
        facecolor=PRIMARY, edgecolor=MID_GRAY, linewidth=0.5, zorder=7, alpha=0.85))
```

## Annotation Placement
- Leader tips: right edge of each layer → `tip_x = LX + LW + SKEW + 0.05`
- Label column: `label_x = 10.8` (consistent x for all labels)
- Horizontal rule extension: `+2.0` units from label_x
- Labels at exact y-midpoints of each layer

## Title Block
```python
# Dark header bar at top
ax.add_patch(patches.Rectangle((0, 17.8), 14, 2.2,
    facecolor=CORP_DARK, edgecolor='none', zorder=8))
# Display title (spaced for letter-spacing effect)
ax.text(0.55, 19.35, "N O V A",
    fontsize=56, fontweight='bold', color=BG,
    fontfamily=FONT, va='top', ha='left', zorder=9)
# Subtitle
ax.text(0.55, 18.35, "EDGE DEVICE  —  TECHNICAL EXPLODED VIEW",
    fontsize=9.5, fontweight='light', color=MID_GRAY,
    fontfamily=FONT, va='top', ha='left', zorder=9)
# Primary accent rule under subtitle
ax.plot([0.55, 7.5], [18.1, 18.1], color=PRIMARY, linewidth=1.6, zorder=9)
```

## Common Pitfalls
- `letter_spacing` does NOT exist in matplotlib → use `"N O V A"` spacing trick
- Always set `matplotlib.use('Agg')` before importing pyplot for headless rendering
- Verify `zorder` hierarchy: bg=0 → grid=1 → layers=3 → faces=4 → details=5–7 → annotations=6 → title=8–9
- `list + list` concatenation works for polygon closing in `ax.plot()` calls
