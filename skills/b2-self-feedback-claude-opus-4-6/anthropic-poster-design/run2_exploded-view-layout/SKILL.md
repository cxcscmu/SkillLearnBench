---
name: run2_exploded-view-layout
description: Improved layout strategy for technical exploded-view diagrams with better spacing and visual balance.
---

# Exploded-View Layout — Improved Strategy

## Key Improvement: Vertical Distribution
Instead of fixed START_Y with large bottom gap, calculate layout to fill the available space between header and footer zones.

```
header_zone = 0 to ~350px (title, subtitle, separator)
content_zone = 400px to (H - 350px) (layers + gaps)
footer_zone = last 300px (metadata, scale bar)
```

### Dynamic Gap Calculation
```python
available_h = footer_y - header_end_y - padding
total_layer_h = sum(layer['height'] for layer in layers)
gap = (available_h - total_layer_h) // (len(layers) - 1)
# Clamp gap to reasonable range
gap = max(80, min(gap, 250))
```

## Layer Stack (5 layers, top to bottom)
1. **Outer Casing** (160px) — Corporate Dark #141413, vent slots
2. **Thermal Management** (100px) — Secondary Accent #CC785C, heat channels
3. **PCB Assembly** (140px) — Tertiary Accent #EDA100, chips + traces
4. **Battery Pack** (110px) — Dark neutral #4A4A48, cell outlines
5. **Interface Board** (90px) — Dark neutral w/ Primary Accent #D97757 connectors

## Annotation Positioning
- All labels right-aligned at a consistent x-position
- Leader line starts at layer right edge + 10px
- Leader line ends at label x - 20px
- Label name: bold, 30px, corporate dark
- Description: regular, 24px, muted gray, 1-2 lines

## Isometric Depth Cues
- Each layer slightly narrower than the one above: -20px per layer
- OR all same width for clean engineering aesthetic (preferred for minimalist style)
- Subtle shadow beneath each layer using cream-dark (#D5D3C9)

## Additional Polish
- Part numbers (e.g., "NV-001") next to each layer
- Hatching/crosshatch patterns for material indication
- Dimension callouts on select layers
- Exploded offset consistent (same gap throughout)
