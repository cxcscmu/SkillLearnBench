---
name: run2_timezone-dst
description: Convert US time zones to the calendar's local timezone, correctly handling Daylight Saving Time for dates in March through November.
---

# Timezone Conversion with DST Awareness

## DST in the US
- **Starts**: 2nd Sunday of March at 2:00 AM → clocks spring forward 1 hour
- **Ends**: 1st Sunday of November at 2:00 AM → clocks fall back 1 hour
- During DST: PST→PDT, MST→MDT, CST→CDT, EST→EDT

## March 9, 2026 Check
- DST started: Sunday, March 8, 2026 at 2:00 AM
- March 9 is AFTER the DST change → all US zones are in summer (DT) variants

## Offset Table for March 9, 2026
| Sender says | Actual zone | UTC offset | vs EDT (calendar) |
|-------------|-------------|------------|-------------------|
| PST         | PDT         | UTC-7      | **+3 hours**      |
| MST         | MDT         | UTC-6      | +2 hours          |
| CST         | CDT         | UTC-5      | +1 hour           |
| EST/ET      | EDT         | UTC-4      | same              |

## Conversion Examples for March 9, 2026
```
Sender says "1:00 PM PST":
  → PDT (UTC-7) → EDT (UTC-4) → add 3 hours
  → 4:00 PM EDT (Eastern)

Sender says "5:00 PM PST":
  → 8:00 PM EDT (Eastern)
```

## Python (pytz)
```python
from datetime import datetime
import pytz

pacific = pytz.timezone('America/Los_Angeles')  # handles PDT automatically
eastern = pytz.timezone('America/New_York')     # handles EDT automatically

dt = pacific.localize(datetime(2026, 3, 9, 13, 0))  # "1 PM PST"
dt_et = dt.astimezone(eastern)
print(dt_et.strftime('%I:%M %p'))  # 04:00 PM
```

## Key Rule
When an email says "PST" but the date is in March/April–October/November, assume PDT.
The +3 hour offset to Eastern still applies (PDT to EDT both shift by 1 hour each).
