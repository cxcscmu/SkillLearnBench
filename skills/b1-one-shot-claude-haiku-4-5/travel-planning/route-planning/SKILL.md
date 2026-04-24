---
name: route-planning
description: Plan multi-city road trip routes using distance matrices and constraints
---

# Route Planning Skill

## Overview
Plan efficient multi-city road trips with constraints like starting point, number of days, and no-fly requirements.

## Core Strategy

### Distance-Based Route Optimization
- Use distance matrix to calculate travel times/distances
- Minimize backtracking between cities
- Allocate days based on travel time and activities per city

### Day Allocation Strategy
- 1 day for initial travel to first city
- Remaining days distributed across 3 Ohio cities
- Typical allocation: 2-2-2 days or 2-2-3 depending on distances
- Last day may include return travel (not full return in this case)

## Python Code Example

```python
from typing import List, Dict, Tuple
from itertools import permutations

def find_best_route(
    start_city: str,
    num_cities: int,
    available_cities: List[str],
    distance_matrix: Dict[str, Dict[str, float]]
) -> Tuple[List[str], float]:
    """
    Find optimal route visiting num_cities starting from start_city.
    Returns (route, total_distance)
    """
    best_route = None
    best_distance = float('inf')

    # Try all permutations of available cities
    for perm in permutations(available_cities[:num_cities]):
        route = [start_city] + list(perm)
        total_distance = calculate_route_distance(route, distance_matrix)

        if total_distance < best_distance:
            best_distance = total_distance
            best_route = route

    return best_route, best_distance

def calculate_route_distance(route: List[str], distance_matrix: Dict) -> float:
    """Calculate total distance for a route"""
    total = 0
    for i in range(len(route) - 1):
        from_city = route[i]
        to_city = route[i + 1]

        if from_city in distance_matrix and to_city in distance_matrix[from_city]:
            total += float(distance_matrix[from_city][to_city])
        else:
            return float('inf')  # Invalid route

    return total

def allocate_days_to_cities(
    num_days: int,
    num_cities: int
) -> List[int]:
    """
    Allocate days across cities.
    First city gets 1 day (travel day), remaining split among other cities.
    """
    # First city gets 1 day for arrival/travel
    remaining_days = num_days - 1
    remaining_cities = num_cities

    days_per_city = [1]  # First city

    # Distribute remaining days
    base_days = remaining_days // remaining_cities
    extra_days = remaining_days % remaining_cities

    for i in range(remaining_cities):
        days = base_days + (1 if i < extra_days else 0)
        days_per_city.append(days)

    return days_per_city

def estimate_travel_time(distance: float, mph: float = 60) -> float:
    """Estimate driving time in hours"""
    return distance / mph
```

## Route Selection Considerations

1. **Starting Point**: Minneapolis, Minnesota
2. **Destination**: 3 Ohio cities (Cleveland, Columbus, Cincinnati are major options)
3. **No Flights**: Must use self-driving/ground transport
4. **Distance Budget**: 7-day trip with reasonable daily driving (6-8 hours max)
5. **Circular vs Linear**: Consider if returning to Minneapolis or ending in Ohio

## Typical Route Pattern

```
Day 1: Minneapolis → City 1 (travel day, possibly long drive)
Day 2-3: City 1 (explore attractions, dining)
Day 4: City 1 → City 2 (short/medium drive)
Day 5-6: City 2 (explore attractions, dining)
Day 7: City 2 → City 3 OR City 2 (final day)
```

## Usage Example

```python
route, distance = find_best_route(
    start_city='Minneapolis',
    num_cities=3,
    available_cities=['Cleveland', 'Columbus', 'Cincinnati'],
    distance_matrix=distances
)

days_allocation = allocate_days_to_cities(
    num_days=7,
    num_cities=3
)
```
