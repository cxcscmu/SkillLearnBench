---
name: travel-budget-optimizer
description: Optimize travel costs including accommodations, meals, transportation, and attractions while respecting budget constraints. Use this skill whenever building a trip with specific budget limits that require cost calculation, price comparison, or financial constraint satisfaction. Essential for maximizing trip value within fixed budgets.
---

# Travel Budget Optimizer

This skill provides techniques for cost estimation, budget allocation, and financial constraint satisfaction in multi-day travel planning.

## Budget Constraint Overview

**Total Budget**: $5,100 for 2 people + 1 dog for 7 days

**Primary Cost Categories**:
1. Accommodations (6 nights)
2. Meals (breakfast, lunch, dinner × 7 days)
3. Attractions and activities
4. Transportation (fuel, tolls, parking)
5. Contingency/Emergency buffer

## Cost Estimation Framework

### 1. Accommodations

**Average pet-friendly hotel rates** (2022 data):
- Budget: $60-80/night
- Mid-range: $80-120/night
- Higher-end: $120-180/night

**For this trip**:
- 6 nights needed
- Budget allocation: $480-720 (6 nights × $80-120/night)
- Recommended: $600 to allow flexibility for better-rated pet-friendly properties

**Database lookup**:
```python
def estimate_accommodation_cost(accommodations_list, nights=6):
    if not accommodations_list:
        return 0

    # Extract price from accommodation data
    prices = []
    for acc in accommodations_list:
        price = acc.get('price_per_night', 0)
        if isinstance(price, str):
            price = float(price.replace('$', '').strip())
        prices.append(price)

    avg_price = sum(prices) / len(prices) if prices else 100
    return avg_price * nights
```

### 2. Meals

**Cost per person per meal** (2022 pricing):
- Breakfast: $8-15/person
- Lunch: $12-20/person
- Dinner: $20-35/person
- **Daily cost per person**: $40-70
- **Daily cost for 2 people**: $80-140

**Budget allocation for meals**:
- Conservative: $700 (7 days × $100/day for 2)
- Comfortable: $840 (7 days × $120/day for 2)
- Recommended: $900 (7 days × $128/day for 2) - allows nicer dinners

**Meal cost examples by cuisine**:
- American casual: $12-18/person lunch, $18-28/person dinner
- Mediterranean: $15-22/person lunch, $25-40/person dinner
- Chinese: $10-15/person lunch, $15-25/person dinner
- Italian: $12-20/person lunch, $20-35/person dinner

**Optimization strategy**:
```python
def optimize_meal_costs(daily_budget_per_person):
    # Allocate less to breakfast, more to dinner
    breakfast_budget = daily_budget_per_person * 0.2  # 20%
    lunch_budget = daily_budget_per_person * 0.3      # 30%
    dinner_budget = daily_budget_per_person * 0.5     # 50%
    return breakfast_budget, lunch_budget, dinner_budget

# For $50/person/day budget:
# breakfast: $10, lunch: $15, dinner: $25
```

### 3. Attractions

**Typical attractions cost** (2022):
- Museum entry: $10-20/person
- Paid tours: $25-50/person
- Outdoor activities: $0-15/person (often free)
- Theme parks: $40-80/person

**Budget allocation**:
- Daily attractions budget: $20-30/person × 7 days = $140-210 for 2
- Recommended: $280-350 (higher-priced attractions in major cities)

**Optimization**: Mix free attractions (parks, public sites, walks) with 2-3 paid attractions per city.

### 4. Transportation (Fuel & Tolls)

**Route**: Minneapolis ↔ Ohio (3 cities)
- Minneapolis to Cleveland: ~500 miles
- Regional driving in Ohio: ~300 miles
- Total: ~1,100 miles roundtrip

**Fuel cost estimation**:
- Average car: 25 MPG
- Gas price (2022): ~$3.50/gallon
- Fuel cost: (1,100 miles ÷ 25 MPG) × $3.50 = 44 gallons × $3.50 = **~$154**

**Tolls** (Ohio has minimal tolls):
- Estimated: $0-50

**Parking**:
- Street parking in major cities: Free-$5/day
- Parking garages: $5-15/day
- Hotel parking: Often free at pet-friendly hotels
- Estimated: $30-50 total

**Total transportation**: $184-254 (budget $300 to be safe)

### 5. Contingency Buffer

Reserve 5-10% for:
- Emergency repairs
- Unexpected meals out
- Additional activities
- Pet care (vet emergency, special food)

**Recommended contingency**: $200-250

## Total Budget Allocation Table

```
Category                 Allocated      Maximum
────────────────────────────────────────────────
Accommodations (6 nights)   $600         $720
Meals (2 people, 7 days)    $900       $1,050
Attractions                 $350         $500
Transportation              $300         $400
Contingency                 $250         $350
────────────────────────────────────────────────
TOTAL                     $2,400       $3,020

Remaining from $5,100 budget: $2,080-2,700
```

The budget provides substantial flexibility for upgrades or premium experiences.

## Cost-Saving Strategies

### 1. Meal Optimization
- Book 1 nice dinner per city (Italian/Mediterranean)
- Breakfast from coffee shops/casual spots ($8-10)
- Lunch at casual restaurants ($12-18)
- Mix with quick/casual options

### 2. Accommodation Optimization
- Select mid-range pet-friendly hotels ($80-100/night)
- Verify extended stay discounts (if available)
- Choose hotels with included breakfast if available

### 3. Attraction Optimization
- Mix free attractions (parks, walks) with paid ones
- Buy combo tickets if available
- Focus on high-value attractions (museums with broad collections)

### 4. Transportation Optimization
- Minimize daily driving; cluster activities
- Route efficiently to reduce mileage
- Take advantage of hotel parking (free for guests)

## Budget Validation Checklist

Before finalizing itinerary:

- [ ] Sum all accommodation costs: _________ (target: ≤$720)
- [ ] Sum all meal costs: _________ (target: ≤$1,050)
- [ ] Sum all attraction costs: _________ (target: ≤$500)
- [ ] Estimate transportation: _________ (target: ≤$400)
- [ ] Reserve contingency: _________ (target: ≥$250)
- [ ] **Grand Total**: _________ (must be ≤$5,100)

## Python Implementation

```python
def validate_budget(itinerary_costs):
    total = sum(itinerary_costs.values())
    budget = 5100

    if total > budget:
        shortfall = total - budget
        print(f"Budget exceeded by ${shortfall}")
        return False

    remaining = budget - total
    print(f"Total spent: ${total}")
    print(f"Remaining: ${remaining}")
    return True

# Example usage
costs = {
    'accommodations': 600,
    'meals': 900,
    'attractions': 350,
    'transportation': 300,
    'contingency': 250
}

validate_budget(costs)  # Returns True if ≤ $5,100
```

## Price Data Sources

- Accommodation prices: Query `accommodations/clean_accommodations_2022.csv` for `price_per_night`
- Restaurant prices: Query `restaurants/clean_restaurant_2022.csv` for `price_range` or `avg_price`
- Attraction prices: Query `attractions/attractions.csv` for `entry_fee` or `price`
- Distance/fuel: Use `googleDistanceMatrix/distance.csv` to calculate mileage
