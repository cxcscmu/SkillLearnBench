---
name: data-analysis
description: This skill covers computing RMSE metrics from observational and simulated water temperature data.
---

# Data Analysis Skill

## Metrics Calculation
To calculate RMSE:
1. Load observed and simulated data.
2. Align data by date and depth.
3. Use exact date-time match and rounded depth (nearest integer meter) for pairing.
4. Calculate RMSE: `sqrt(mean((observed - simulated)^2))`

## RMSE Targets
- Overall RMSE: < 1.60
- Annual Deep RMSE: < 1.55 (depth >= 13 m)
- Summer Deep RMSE: < 1.70 (depth >= 13 m, months 6-9)
