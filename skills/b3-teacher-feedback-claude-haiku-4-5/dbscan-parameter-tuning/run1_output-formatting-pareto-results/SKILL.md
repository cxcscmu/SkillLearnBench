---
name: output-formatting-pareto-results
description: Format and write Pareto frontier results to CSV file with proper rounding and column ordering.
---

## Output File

Write results to: `/root/pareto_frontier.csv`

## CSV Format

```csv
F1,delta,min_samples,epsilon,shape_weight
```

**Column order (exactly as shown):**
1. `F1` — F1 score (float)
2. `delta` — Average Euclidean distance of matches (float)
3. `min_samples` — DBSCAN parameter (integer)
4. `epsilon` — DBSCAN parameter (integer)
5. `shape_weight` — Custom distance weight (float)

## Rounding Requirements

- `F1`: Round to 5 decimal places
- `delta`: Round to 5 decimal places
- `min_samples`: Integer (no decimal)
- `epsilon`: Integer (no decimal)
- `shape_weight`: Round to 1 decimal place

## Row Ordering

Sort rows by:
1. F1 (descending) — highest F1 first
2. delta (ascending) — lowest delta second (for ties in F1)

## Example Format

```csv
F1,delta,min_samples,epsilon,shape_weight
0.75234,12.34567,5,12,1.2
0.74891,13.45678,6,14,1.3
0.72345,11.23456,4,10,1.1
```

## Handling Special Values

- If delta is NaN for a Pareto solution (no matches found), it should not be included in final results (it would be filtered out during F1 > 0.5 check or during Pareto detection)
- All reported solutions should have valid (non-NaN) F1 and delta values