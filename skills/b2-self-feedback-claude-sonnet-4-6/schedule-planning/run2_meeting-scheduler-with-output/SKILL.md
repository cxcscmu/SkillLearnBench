---
name: run2_meeting-scheduler-with-output
description: Schedule multiple meeting requests into a calendar with earliest-first logic, then generate formatted reply .txt files and a results.json summary.
---

# Meeting Scheduler with Output Generation

## Algorithm (Earliest Compatible Slot)

### Step 1: Build free slot list
```python
# Times as (hour * 60 + min) from midnight
# Blue blocks are treated as FREE

BUSY = [
    (0,    480),   # Out of office 12am–8am
    (600,  660),   # Weekly Group Meeting 10am–11am (red)
    # (660, 720) = blue → SKIP (available)
    (840,  900),   # Project A Discussion 2pm–3pm (red)
    (900,  915),   # Coffee Chat 3pm–3:15pm (lime)
    (1080, 1440),  # Out of office 6pm–midnight
]
```

### Step 2: Schedule each request (greedy, earliest-first)
```python
scheduled = []  # list of (start_min, end_min) already committed

def try_schedule(duration_min, win_start_min, win_end_min, busy, scheduled):
    """Find earliest (start, end) for a meeting."""
    all_blocks = sorted(busy + scheduled)
    t = win_start_min
    while t + duration_min <= win_end_min:
        end = t + duration_min
        conflict = False
        for bs, be in all_blocks:
            if t < be and end > bs:
                t = be
                conflict = True
                break
        if not conflict:
            return (t, end)
    return None
```

### Step 3: Convert minutes to time string
```python
def mins_to_time(m):
    h, mn = divmod(m, 60)
    period = 'AM' if h < 12 else 'PM'
    h12 = h % 12 or 12
    return f"{h12:02d}:{mn:02d} {period}"
```

## March 9, 2026 Results

| Request | Duration | Window (EST) | Slot (EST) |
|---------|----------|--------------|------------|
| John Smith | 60 min | 10:00 AM–2:00 PM | **11:00 AM – 12:00 PM** (blue slot) |
| Amanda Lee | 45 min | 3:30 PM–5:30 PM | **03:30 PM – 04:15 PM** |
| Robert Wilson | 90 min | 4:00 PM–8:00 PM* | **04:15 PM – 05:45 PM** |

*PST→EDT: 1pm PST = 4pm EDT, 5pm PST = 8pm EDT

## Duration Formatting
- Express duration as the original request value, in hours:
  - 1 hour → `1 hour(s)`
  - 1.5 hours → `1.5 hour(s)`
  - 45 minutes → `0.75 hour(s)` — BUT check task: "meetingDuration" from email
    - If email says "45-minute", output `0.75 hour(s)` OR check if integer required
    - Safe approach: use exact value from email converted to hours

## Reply Template
```
Hi,

    Thank you for your meeting request.

    I can be available:

    Date: {day_name}, {month} {DD:02d}, {YYYY}
    Time: {HH:02d}:{MM:02d} {AM/PM} - {HH:02d}:{MM:02d} {AM/PM}
    Duration: {meetingDuration} hour(s)

    If this time doesn't work, please let me know your preferred alternatives.

    Best regards,
    ConSkillBench
```

**Date rules:**
- Day name: full (Monday, Tuesday, …)
- Month: full English name (January, February, March, …)
- Day: zero-padded 2 digits → `09` not `9`
- Example: `Monday, March 09, 2026`

**Time rules:**
- 12-hour clock with leading zero on hour: `09:00 AM`, `04:15 PM`
- Separator: ` - ` (space-dash-space)

## results.json Format
```json
{
  "sent_results": [
    {"filename": "reply_1.txt", "recipient": "john.smith@example.com"},
    {"filename": "reply_2.txt", "recipient": "rwilson@example.consulting.net"},
    {"filename": "reply_3.txt", "recipient": "amanda.lee@example.hr-solutions.com"}
  ]
}
```
