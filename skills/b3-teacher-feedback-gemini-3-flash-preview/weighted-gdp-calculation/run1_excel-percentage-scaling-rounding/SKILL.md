---
name: excel-percentage-scaling-rounding
description: Convert decimal percentages to whole-number representations and round to a specific decimal place.
---

When a task requires a percentage to be displayed as a whole number (e.g., 0.1234 as 12.3), you must scale the value within the formula.

### Scaling and Rounding
1.  **Multiply by 100**: Convert the decimal (0.123) to a percentage-base (12.3).
2.  **Round**: Use the `ROUND` function to limit the decimal places.

**Formula:**
`=ROUND((calculation) * 100, 1)`

*   **calculation**: The math (e.g., `Net Exports / GDP`).
*   **1**: Specifies rounding to one decimal place.

**Contextual Example:**
If calculating Net Exports as % of GDP:
`=ROUND((NetExports_Value / GDP_Value) * 100, 1)`
This results in `15.2` instead of `0.15234...`.