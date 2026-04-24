---
name: run2_pdf-calendar-parsing
description: Precisely parse a PDF day-view calendar to extract event times, durations, and colors by reading visual block positions and the 15-minute grid.
---

# PDF Calendar Parsing (Improved)

## Grid Structure
- Each hour label (12am, 1am, …, 11pm) marks the TOP of that hour's row
- Between two adjacent dashed horizontal lines = **15 minutes**
- 4 intervals per hour

## Reading Block Times — Step by Step
1. Find the hour label closest ABOVE the block's top edge
2. Count how many 15-min ticks down from that label to the block's top → start time
3. Find the hour label closest ABOVE the block's bottom edge
4. Count ticks to block bottom → end time
5. If a block starts exactly at a label, start = that label's time on the dot

## Color Classification
| Color         | Hex range (approx)          | Status    |
|---------------|-----------------------------|-----------|
| Dark gray     | R<100, G<100, B<100         | Busy (OOO)|
| Red/salmon    | R>200, G<150, B<150         | Busy      |
| Blue/purple   | R~130, G~130, B~200-230     | **Available** (overwritable) |
| Lime/yellow-green | R>150, G>180, B<100    | Busy      |

## Example Calendar — March 9, 2026
```
12:00 AM – 08:00 AM  Out of office         (gray)   BUSY
08:00 AM – 10:00 AM  [empty]                         FREE
10:00 AM – 11:00 AM  Weekly Group Meeting  (red)    BUSY
11:00 AM – 12:00 PM  Busy with task B      (BLUE)   FREE (overwritable)
12:00 PM – 02:00 PM  [empty]                         FREE
02:00 PM – 03:00 PM  Project A Discussion  (red)    BUSY
03:00 PM – 03:15 PM  Coffee Chat           (lime)   BUSY  ← 1 tick = 15 min
03:15 PM – 06:00 PM  [empty]                         FREE
06:00 PM – 12:00 AM  Out of office         (gray)   BUSY
```

## Thin Block Disambiguation
A block taking exactly ONE 15-min slot looks like a thin line just above a dashed separator.
- If the label is at 3pm and the block bottom aligns with the first dashed line below → 3:00–3:15

## Python extraction with pdfplumber
```python
import pdfplumber

with pdfplumber.open("calendar.pdf") as pdf:
    text = pdf.pages[0].extract_text()
    # Text output lists event names and time labels
    # Visual block colors require image analysis
```
