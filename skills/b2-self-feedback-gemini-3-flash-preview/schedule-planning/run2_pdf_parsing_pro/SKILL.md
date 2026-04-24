---
name: run2_pdf_parsing_pro
description: Advanced PDF parsing for calendar extraction, including sidebar filtering and color-based classification.
---

# Advanced PDF Calendar Extraction

When parsing complex PDF calendars, filtering non-calendar elements (like sidebars) and accurately mapping coordinates to time is crucial.

## Sidebar and Noise Filtering

- Identify the main calendar grid by filtering by x-coordinates (e.g., `x1 > 500`).
- Filtering by height to avoid icons/small labels.
- Map vertical coordinates (`top`) to minutes using a calibrated scale.
