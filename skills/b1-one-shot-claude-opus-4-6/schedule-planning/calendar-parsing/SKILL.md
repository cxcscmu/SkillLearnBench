---
name: calendar-parsing
description: Techniques for parsing visual calendar PDFs to extract appointment blocks, free slots, and time boundaries.
---

# Calendar Parsing from PDF

## Overview
Parse visual calendar layouts (e.g., Google Calendar exports) to extract structured time block data.

## Key Techniques

### 1. Reading Calendar Structure
- Identify the timeline axis (typically vertical, hourly labels from 12am-11pm)
- Each space between adjacent horizontal lines = 15 minutes
- Blocks are colored rectangles overlaid on the grid

### 2. Extracting Block Times
- Map each block's top/bottom edges to the nearest 15-minute gridline
- Read the block label text for the event name
- Note the block color to determine priority/type

### 3. Color Coding Conventions
- **Blue/purple blocks**: Low-priority or flexible tasks; can be overwritten by new meetings
- **Red/pink blocks**: Fixed appointments; cannot be moved
- **Green/yellow blocks**: Standard meetings; cannot be moved
- **Gray/dark blocks**: Out-of-office or unavailable time

### 4. Determining Free Slots
1. List all non-overwritable blocks (everything except blue)
2. Treat blue blocks as free time
3. Subtract blocked ranges from the full day to get available windows
4. Free slots appear as areas with only dashed horizontal gridlines (no colored blocks)

### 5. Timezone Handling
- Calendar header typically shows the timezone (e.g., "Eastern Time - New York")
- All times extracted are in the calendar's native timezone
- Convert external time references (e.g., PST) to the calendar timezone before comparison
