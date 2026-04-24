---
name: run2_pdf-visual-extraction
description: Extract calendar event times by analyzing visual block positions relative to hour markers
---

# PDF Visual Extraction for Calendar Events

## Purpose
Accurately extract event times from calendar PDF by measuring visual block heights and positions relative to hour markers on the timeline axis.

## Key Strategy

### 1. Identify Hour Marker Positions
- Calendar PDFs typically list hours on the left axis (12am, 1am, ..., 11pm)
- Use pdfplumber to extract text and identify hour positions
- Calculate pixel-to-time conversion using hour positions

```python
import pdfplumber
import re

def get_hour_positions(pdf_path):
    """Extract positions of hour markers"""
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()

        # Find all hour markers
        hours = {}
        for line in text.split('\n'):
            match = re.match(r'(\d{1,2}(?:am|pm))', line, re.IGNORECASE)
            if match:
                hour_str = match.group(1)
                # Note: Would need OCR or position data to get pixel y-coordinates

        return hours
```

### 2. Identify Colored Blocks Using OCR/Text Extraction
- Use pdfplumber to extract all text elements
- Match event names with their labels
- Identify block color types:
  - **Red blocks** (RGB ~200, 100, 100): Busy/important (fixed)
  - **Blue blocks** (RGB ~100, 100, 200): Flexible/low-priority (can override)
  - **Gray blocks** (RGB ~150, 150, 150): Unavailable (fixed)
  - **Yellow/Green blocks** (RGB high-G): Semi-busy (fixed)

### 3. Visual Measurement Approach (Manual Inspection)

When automated extraction is insufficient, measure block heights manually:

```python
def estimate_block_duration(visual_inspection):
    """
    Based on visual inspection of PDF:

    Measure each block's height relative to hour markers:
    - If block spans exactly from one hour line to next = 1 hour
    - If block is half the height of 1-hour span = 30 minutes
    - If block is 2 hour-spans tall = 2 hours

    Cross-check by comparing block heights:
    - Blocks of similar visual height likely have similar durations
    - Use known 1-hour blocks as reference
    """
    pass
```

### 4. Cross-validation Strategy

```python
def validate_event_times(events, constraints):
    """
    Validate extracted times make sense:

    1. Events don't overlap (except where explicitly flexible)
    2. Events fit within business hours shown on calendar
    3. Event durations are reasonable (not 20+ hours)
    4. Sequence is correct (no events starting before earlier events)
    """
    pass
```

## Implementation Notes

### For this PDF format:
- Calendar shows: "Mon Mar 9, 2026 (Eastern Time - New York)"
- Timeline: 12am through 11pm (24-hour period)
- Events visible: Out of office, Weekly Group Meeting, Busy with task B, Project A Discussion, Coffee Chat, Out of office
- Blue blocks are flexible; all others are fixed

### Visual Inspection Checklist:
- [ ] Identify all hour markers (12am through 11pm on left axis)
- [ ] For each colored block, note start time (which hour line it touches)
- [ ] For each colored block, estimate height relative to hour-spans
- [ ] Identify block colors and map to priority level
- [ ] Cross-check total timeline adds up to 24 hours

## Example Output

```python
events = [
    {"name": "Out of office", "start": "00:00", "end": "09:00", "color": "gray", "flexible": False},
    {"name": "Weekly Group Meeting", "start": "10:00", "end": "11:00", "color": "red", "flexible": False},
    {"name": "Busy with task B", "start": "11:00", "end": "13:00", "color": "blue", "flexible": True},
    {"name": "Project A Discussion", "start": "14:00", "end": "15:00", "color": "red", "flexible": False},
    {"name": "Coffee Chat with someone", "start": "15:00", "end": "15:45", "color": "yellow", "flexible": False},
    {"name": "Out of office", "start": "18:00", "end": "23:00", "color": "gray", "flexible": False},
]
```
