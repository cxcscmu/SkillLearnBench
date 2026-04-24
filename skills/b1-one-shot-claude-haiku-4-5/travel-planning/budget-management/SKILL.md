---
name: budget-management
description: Track and manage travel budget across accommodations, meals, and activities
---

# Budget Management Skill

## Overview
Manage and allocate a fixed travel budget across accommodations, meals, attractions, and other expenses.

## Budget Allocation Strategy

### Typical 7-Day Budget Split (for $5,100)
- Accommodations: 50-55% ($2,550-2,805)
- Meals: 25-30% ($1,275-1,530)
- Attractions/Activities: 10-15% ($510-765)
- Transportation: 5-10% ($255-510)
- Contingency: 5% ($255)

### Per-Day Meal Budget
- For 2 people, 3 meals/day
- Budget: $75-100 per day for meals
- Average per meal: $12-17 per person

### Accommodation Budget
- Per night pet-friendly hotel: $200-300
- 6 nights total: $1,200-1,800
- Or split between budget/mid-range options

## Python Code Example

```python
from typing import Dict, List

class BudgetTracker:
    def __init__(self, total_budget: float):
        self.total_budget = total_budget
        self.expenses: Dict[str, List[float]] = {
            'accommodation': [],
            'breakfast': [],
            'lunch': [],
            'dinner': [],
            'attractions': [],
            'transportation': []
        }

    def add_expense(self, category: str, amount: float) -> None:
        """Add expense to tracker"""
        if category in self.expenses:
            self.expenses[category].append(amount)

    def get_total_by_category(self, category: str) -> float:
        """Get total spent in a category"""
        return sum(self.expenses.get(category, []))

    def get_remaining_budget(self) -> float:
        """Calculate remaining budget"""
        total_spent = sum(
            sum(expenses) for expenses in self.expenses.values()
        )
        return self.total_budget - total_spent

    def get_budget_summary(self) -> Dict[str, float]:
        """Get spending summary by category"""
        summary = {}
        for category, expenses in self.expenses.items():
            total = sum(expenses)
            summary[category] = {
                'total': total,
                'count': len(expenses),
                'average': total / len(expenses) if expenses else 0
            }
        return summary

    def is_within_budget(self) -> bool:
        """Check if spending is within budget"""
        return self.get_remaining_budget() >= 0

def estimate_accommodation_cost(
    num_nights: int,
    price_per_night: float
) -> float:
    """Estimate total accommodation cost"""
    return num_nights * price_per_night

def estimate_meal_cost(
    num_days: int,
    num_people: int,
    cost_per_meal_per_person: float
) -> float:
    """Estimate total meal cost (3 meals per day)"""
    return num_days * num_people * 3 * cost_per_meal_per_person

def find_affordable_options(
    data: List[Dict],
    budget_per_item: float,
    price_field: str
) -> List[Dict]:
    """Filter options within budget"""
    affordable = []
    for item in data:
        try:
            price = float(item.get(price_field, 0))
            if price <= budget_per_item:
                affordable.append(item)
        except (ValueError, TypeError):
            continue
    return affordable
```

## Budget Constraints for This Trip

### Fixed Costs
- **Accommodations**: 6 nights of pet-friendly lodging
- **Meals**: 7 days × 2 people × 3 meals

### Flexible Costs
- Attractions (some may be free)
- Parking/tolls

### Budget Per Meal
- Budget: $5,100 total for 2 people, 7 days
- Meal budget: ~$1,500 (30% of total)
- Per day per person: ~$107 including accommodations + meals + activities
- Per meal per person: ~$12-15

## Usage Example

```python
tracker = BudgetTracker(5100)

# Add expenses as itinerary is built
tracker.add_expense('accommodation', 250)  # Per night
tracker.add_expense('breakfast', 25)  # For 2 people
tracker.add_expense('lunch', 40)
tracker.add_expense('dinner', 60)

# Check status
print(f"Remaining: ${tracker.get_remaining_budget()}")
print(f"Within budget: {tracker.is_within_budget()}")
```
