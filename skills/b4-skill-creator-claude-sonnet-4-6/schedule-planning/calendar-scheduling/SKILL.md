---
name: calendar-scheduling
description: Parse a visual calendar PDF to extract existing appointments and find earliest available meeting slots. Handles blue (low-priority/flexible) blocks as overwritable free time. Use when given a calendar image/PDF and meeting requests that need to be scheduled without conflicts.
---

# Calendar Scheduling Skill

## Parsing a Visual Calendar

When reading a calendar PDF image:
- Each horizontal dashed line = 15 minutes
- Identify block colors:
  - **Dark gray** = Out of office (hard block, unavailable)
  - **Salmon/pink-red** = Busy (hard block, unavailable)
  - **Blue/purple** = Low priority task (soft block, treat as AVAILABLE/overwritable)
  - **Lime/yellow-green** = Other appointment (hard block, unavailable)
- Note the calendar's timezone (shown in the header)

## Extracting Block Times

Count horizontal lines from the nearest hour label to determine start/end:
- 1 line = 15 min, 2 lines = 30 min, 3 lines = 45 min, 4 lines = 1 hour

## Finding Available Slots

1. List all hard-blocked time ranges
2. Treat blue blocks as free
3. For each meeting request, find the earliest slot within the requester's availability window that doesn't conflict with hard blocks or already-assigned meetings
4. Process requests to maximize accommodation of all meetings ("all requests can be accommodated")

## Conflict Resolution

When multiple requests compete for the same time:
- Assign in the order that allows ALL requests to be accommodated
- Each meeting should get the earliest possible slot
- If assigning earlier slots to later requests would block earlier requests, adjust to find globally optimal assignment
