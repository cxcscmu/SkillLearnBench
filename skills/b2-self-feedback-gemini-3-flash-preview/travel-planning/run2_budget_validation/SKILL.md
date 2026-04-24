---
name: run2_budget_validation
description: Validate travel budgets using accommodation and restaurant data.
---

# Budget Validation for Travel Planning

To stay within a given budget (e.g., $5,100 for 7 days for two), calculate and track costs meticulously.

## Calculating Daily Costs
1. **Accommodation:** Multiply the `price` by the number of nights. Check `minimum nights` for eligibility.
2. **Food:** Estimate food costs using `Average Cost` from `clean_restaurant_2022.csv`. Assume this cost is for two people.
3. **Transport:** Estimate gas or rental costs for self-driving based on distances in `distance.csv`.

## Cumulative Tracking
Sum all estimated costs (accommodation + 21 meals + transportation) and compare against the total budget. Prioritize high-value attractions and meals while keeping within the limit.
