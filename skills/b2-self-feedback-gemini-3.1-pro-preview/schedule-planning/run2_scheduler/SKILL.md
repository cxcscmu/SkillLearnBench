---
name: run2_scheduler
description: An improved scheduling algorithm to find the earliest compatible free slots under time constraints.
---

# Optimal Scheduling Algorithm

This skill dynamically assigns overlapping interval constraints by sweeping over available free slots, factoring in required meeting durations and available windows.

## Merging Intervals
```python
def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = []
    for interval in intervals:
        if not merged or merged[-1][1] <= interval[0]:
            merged.append(interval)
        else:
            merged[-1][1] = max(merged[-1][1], interval[1])
    return merged
```

## Earliest Fit Logic
Finds the earliest possible block large enough to fit the request that intersects both the user availability and your availability.

```python
def find_earliest_slot(available_times, req_start, req_end, duration):
    for avail_start, avail_end in available_times:
        start = max(avail_start, req_start)
        end = min(avail_end, req_end)
        
        if end - start >= duration:
            return start, start + duration
    return None, None
```

## Advanced Considerations
When multiple requests might conflict, the optimal approach involves sorting the requests (e.g., by end deadline or duration constraint), attempting to schedule them, and committing slots recursively to ensure all can be accommodated.
