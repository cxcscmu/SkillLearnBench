---
name: glm-calibration
description: Calibration strategy for GLM lake temperature simulations, including parameter sensitivity and typical ranges.
---

# GLM Calibration for Lake Temperature

## Key Calibration Parameters (Lake Mendota)
| Parameter | Range | Effect |
|-----------|-------|--------|
| `Kw` | [0.1, 0.5] | Light extinction; higher = less deep heating, stronger stratification |
| `coef_mix_hyp` | [0.3, 0.7] | Hypolimnetic mixing; higher = more deep mixing, warmer hypolimnion |
| `wind_factor` | [0.7, 1.3] | Wind speed multiplier; higher = more surface mixing |
| `lw_factor` | [0.7, 1.3] | Longwave radiation multiplier; affects surface energy balance |
| `ch` | [0.0005, 0.002] | Sensible heat transfer coefficient |

## Calibration Strategy
1. Start with defaults, run, compute RMSE
2. Adjust `Kw` first (strongest control on stratification)
3. Then `coef_mix_hyp` (controls deep temperatures)
4. Fine-tune `wind_factor` and `lw_factor` for surface/overall bias
5. `ch` has moderate effect on surface heat exchange

## RMSE Computation
- Match observations to simulation by exact datetime and rounded depth
- depth_sim = round(lake_depth - z) to get depth from surface
- Overall RMSE, deep (>=13m) RMSE, summer deep (Jun-Sep, >=13m) RMSE
