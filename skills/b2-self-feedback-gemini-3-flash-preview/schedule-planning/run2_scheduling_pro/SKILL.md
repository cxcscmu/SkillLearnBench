---
name: run2_scheduling_pro
description: Advanced scheduling with priority-based sorting (EDF) and flexible slot overwriting.
---

# Optimal Meeting Scheduling

When scheduling multiple requests with different constraints and durations, use the Earliest Deadline First (EDF) strategy to maximize the chance of fitting everyone.

## EDF Scheduling Logic

1.  **Extract Constraints:** Identify `start_min`, `end_min`, and `duration` for each request.
2.  **Sort Requests:** Sort requests by their `end_min` (deadline).
3.  **Find Slots:** Iterate through sorted requests and find the earliest compatible slot within their window.
4.  **Overwrite Logic:** Consider blue blocks as free space during search but record them as busy once a meeting is booked.
