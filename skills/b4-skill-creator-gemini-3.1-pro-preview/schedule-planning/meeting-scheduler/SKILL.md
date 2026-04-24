---
name: meeting-scheduler
description: Use this skill whenever you need to schedule meetings, parse calendar PDFs, resolve overlapping time windows across timezones, and format schedule responses.
---

# Meeting Scheduler Skill

This skill provides domain knowledge and workflows for scheduling meetings based on PDF calendars and email requests.

## 1. Extracting Request Details
- Read JSON files containing emails.
- Identify the requested meeting date, duration, and time constraints.
- Pay attention to timezones (e.g., PST vs EST). Remember that Pacific Time is generally 3 hours behind Eastern Time.

## 2. Parsing Calendar PDFs
- Use `fitz` (PyMuPDF) in Python to extract text and shapes.
- The timeline Y-coordinates often map linearly to time. Calculate the mapping using horizontal grid lines (e.g., if 12am is at Y=43.89 and 1am is at Y=73.85, then 1 hour = 29.96 points).
- Extract filled rectangles (events) and their colors.
- Blue-colored blocks typically indicate low-priority or flexible tasks that can be overwritten.

## 3. Resolving Time Constraints
- Find the earliest compatible time for EACH request.
- Ensure no meetings overlap with each other or with hard commitments (non-blue blocks).
- Overwrite blue blocks if necessary to accommodate a meeting.

## 4. Formatting Output
Use the following strict templates:
Date: `{day_name}, {month} {DD}, {YYYY}` (e.g., `Thursday, January 08, 2026`)
Time: `{HH:MM AM/PM} - {HH:MM AM/PM}` (e.g., `09:00 AM - 10:30 AM`)
Duration: `{meetingDuration} hour(s)` (e.g., `1`, `1.5`, `0.75`)
