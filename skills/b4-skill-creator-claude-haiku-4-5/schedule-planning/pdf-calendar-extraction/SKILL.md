---
name: pdf-calendar-extraction
description: Extract appointments and time blocks from a calendar PDF. This skill helps parse calendar.pdf to identify appointment blocks, their positions on the timeline, duration, and color coding (including blue blocks that represent flexible/overwritable slots). Use this whenever you need to extract calendar data from a PDF document.
---

# PDF Calendar Extraction

## Overview

This skill extracts appointment information from a calendar PDF by analyzing:
- Appointment block positions and dimensions
- Time slots based on 15-minute intervals between horizontal lines
- Color coding (blue = flexible/overwritable, other colors = fixed appointments)
- Start and end times calculated from vertical position relative to timeline

## Extracting Calendar Data from PDF

### Step 1: Read the PDF

Use the Read tool to load the calendar PDF:

```
Read /root/calendar.pdf
```

The PDF will display as a visual image in the interface.

### Step 2: Identify the Timeline Structure

Look for:
- **Vertical timeline axis** (usually on the left side) showing hours or time markers
- **Horizontal grid lines** dividing the calendar into 15-minute intervals
- **Time labels** indicating the start hour(s) of the day

Example: If you see "9:00 AM" label and horizontal lines below it, each line represents 15 minutes.

### Step 3: Locate and Measure Appointment Blocks

For each visible appointment block:

1. **Identify the block**: Rectangular areas representing appointments
2. **Determine color**: Note if the block is blue (flexible) or another color (fixed)
3. **Measure vertical position**:
   - Identify which horizontal lines the block spans
   - Count lines from the start time to get duration
   - Each line = 15 minutes
4. **Calculate times**:
   - Start time = position from top of timeline
   - End time = start time + (number of 15-minute intervals)

### Step 4: Record Appointment Data

Create a structured list of appointments:

```json
{
  "timezone": "[Extracted from PDF if visible]",
  "appointments": [
    {
      "name": "Appointment Name",
      "start_time": "HH:MM",
      "end_time": "HH:MM",
      "duration_minutes": 30,
      "color": "blue|other",
      "flexible": true|false
    }
  ]
}
```

## Color Coding Rules

- **Blue blocks**: Flexible or low-priority tasks that can be overwritten by meeting requests
- **Other colors** (gray, black, etc.): Fixed appointments that cannot be moved
- When a meeting request overlaps with a blue block, treat it as available time and schedule the meeting

## Tips for Accurate Extraction

- If the PDF shows a full day view, identify the start and end hours clearly
- Double-check time calculations by counting 15-minute intervals
- Note any timezone information displayed on the calendar
- If blocks are adjacent with no gap, verify they are separate appointments vs. one longer block

## Output Format

Return extracted data as a structured list suitable for the meeting slot finder algorithm to process.
