---
name: run2_pdf-calendar-parsing
description: Extract calendar events from PDF by mapping colored rectangles to a 15-min grid using PyMuPDF.
---

# PDF Calendar Parsing with PyMuPDF

## Installation
```bash
pip install pymupdf
```

## Approach
1. Use `page.get_drawings()` to extract all drawn shapes.
2. Identify the 15-min grid: horizontal lines with `width > 100` and `height < 3`. Sort by y-position. The first line is time 0 (12:00 AM), each subsequent line is +15 min.
3. Identify event blocks: filled rectangles with `height > 5` and `width > 100`.
4. Map each block's top/bottom y to the nearest grid line: `slot = round((y - grid[0]) / spacing)`, time = `slot * 15` minutes from midnight.
5. Blue blocks: check if `fill[2] > 0.6` and `fill[0] < 0.55` (blue-dominant). These are low-priority and overwritable.

## Grid line to time mapping
```python
lines = sorted([d["rect"].y0 for d in drawings if d["rect"].width > 100 and d["rect"].height < 3])
spacing = lines[1] - lines[0]  # ~7.5 px

def y_to_slot(y):
    return round((y - lines[0]) / spacing)

def slot_to_time(slot):
    total_min = slot * 15
    h, m = divmod(total_min, 60)
    return h, m  # 24-hour format
```

## Block padding
Blocks have ~1px padding on each side, so `round()` to nearest slot gives correct results. Always verify by checking that durations are multiples of 15 minutes.

## Identifying block colors
- Gray (out of office): `fill ≈ (0.38, 0.38, 0.38)`
- Red/Pink (meetings): `fill ≈ (0.90, 0.49, 0.45)`
- Blue (low-priority): `fill ≈ (0.47, 0.53, 0.80)` — OVERWRITABLE
- Yellow/Green (labels): `fill ≈ (0.75, 0.79, 0.20)` — these are small label squares inside blocks, ignore
