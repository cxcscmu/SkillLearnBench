---
name: pdf-calendar-parser
description: Extracts appointments, start/end times, and priority colors from a PDF calendar. Use this skill whenever you need to understand existing schedules from a visual PDF calendar document.
---

# PDF Calendar Parser

This skill facilitates the extraction of scheduling data from a visual PDF representation of a calendar.

## Calendar structure
- **Timeline axis**: Measure the position of appointment blocks relative to the vertical or horizontal time scale.
- **15-minute intervals**: Each gap between two adjacent horizontal lines represents exactly 15 minutes.
- **Priority colors**:
  - **Blue blocks**: Low-priority/flexible tasks that can be rescheduled or overwritten if needed for higher-priority meeting requests.
  - **Other colors**: Fixed appointments that cannot be moved.

## Extraction goals
- **Appointment block**: Identify each block's name, start time, end time, and color.
- **Available time**: Identify gaps between fixed (non-blue) appointments that are long enough to fit a meeting's requested duration.

## Tooling
Use tools like `pdf-to-text` or similar to extract visual coordinates if possible, or perform OCR/image analysis to identify block positions and colors.
- **Coordinate-to-Time Mapping**: Map vertical or horizontal positions to specific times based on the 15-minute grid.
- **Color detection**: Focus on identifying blue vs. non-blue blocks.
