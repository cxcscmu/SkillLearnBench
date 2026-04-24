---
name: glm-calibration
description: Calibrating General Lake Model (GLM) parameters to match field observations of water temperature. Use this skill whenever you need to adjust light extinction (Kw), mixing coefficients (coef_mix_hyp), or atmospheric bulk transfer factors (wind_factor, lw_factor, ch) to improve model fit. Essential for reducing temperature RMSE and achieving model validation thresholds for lakes.
---

# GLM Parameter Calibration Strategy

## Overview

Calibration is the process of systematically adjusting model parameters to minimize error between simulated and observed water temperatures. For GLM on Lake Mendota, five parameters control temperature evolution:

- **Kw** (light extinction): Controls solar heating penetration depth
- **coef_mix_hyp** (hypolimnion mixing): Controls deep water turbulent mixing
- **wind_factor** (wind multiplier): Scales wind-driven surface mixing
- **lw_factor** (longwave multiplier): Adjusts atmospheric heat exchange
- **ch** (sensible heat coefficient): Controls air-water heat transfer

## Physical Basis for Parameter Effects

### Kw (Light Extinction, 0.1 - 0.5)
- **Low Kw** (0.1): More light penetrates to depth, warms deeper layers
- **High Kw** (0.5): Light absorbed quickly, heating concentrated at surface
- **Effect on RMSE**: Affects whole water column, especially sensitive to epilimnion heating
- **Tuning**: If summer surface temps too high, increase Kw. If deep winter temps too cold, decrease Kw.

### coef_mix_hyp (Hypolimnion Mixing, 0.3 - 0.7)
- **Low value** (0.3): Less deep mixing, sharper thermocline, deeper water stays colder longer
- **High value** (0.7): More mixing, faster temperature equilibration in hypolimnion
- **Effect on RMSE**: Primarily affects annual_deep_rmse (deep water temperatures)
- **Tuning**: If deep water temperatures lag observations, increase coef_mix_hyp. If too warm, decrease.

### wind_factor (Wind Speed Multiplier, 0.7 - 1.3)
- **Low value** (0.7): Less wind-driven mixing, stronger stratification
- **High value** (1.3): More wind-driven mixing, weaker stratification, mixed layer deepens faster
- **Effect on RMSE**: Affects thermocline depth, particularly impacts summer_deep_rmse
- **Tuning**: If summer thermocline too sharp (warm surface, cold deep), increase wind_factor.

### lw_factor (Longwave Radiation Multiplier, 0.7 - 1.3)
- **Low value** (0.7): Less downwelling IR radiation, surface cools faster at night
- **High value** (1.3): More IR radiation, surface warming enhanced
- **Effect on RMSE**: Affects diurnal and seasonal surface temperature amplitude
- **Tuning**: If winter surface temps too cold, increase lw_factor. If too warm, decrease.

### ch (Sensible Heat Coefficient, 0.0005 - 0.002)
- **Low value** (0.0005): Weak air-water heat exchange, slow surface temperature response
- **High value** (0.002): Strong air-water heat exchange
- **Effect on RMSE**: Affects spring/fall transition rates and surface temperature amplitude
- **Tuning**: If surface temps respond too slowly to weather, increase ch. If overly responsive, decrease.

## Calibration Workflow

### Phase 1: Baseline and Diagnosis (Iteration 1-3)
1. Run GLM with initial parameter set
2. Compute RMSE overall, annual_deep, summer_deep
3. Diagnose which RMSE threshold is violated most
4. Identify spatial/temporal patterns in error (e.g., always too warm at depth)

### Phase 2: Targeted Parameter Adjustment (Iteration 4-15)
Target parameters based on error pattern:

**If annual_deep_rmse is highest (deep cold bias):**
- Decrease coef_mix_hyp (0.05 step)
- OR increase lw_factor (0.05 step)

**If summer_deep_rmse is highest (summer stratification too strong):**
- Increase wind_factor (0.1 step)
- OR increase coef_mix_hyp (0.05 step)

**If overall_rmse is highest from surface temps (warming bias):**
- Increase Kw (0.05 step)
- OR decrease lw_factor (0.05 step)
- OR decrease ch (0.0001 step)

### Phase 3: Refinement (Iteration 16+)
Once close to thresholds:
- Make smaller adjustments (0.01-0.02 parameter steps)
- Focus on the single RMSE metric furthest from threshold
- Balance trade-offs (e.g., improving annual_deep might slightly worsen summer_deep)

## Step Size Guidelines

**Large steps** (when far from threshold):
- Kw: 0.05
- coef_mix_hyp: 0.1
- wind_factor: 0.1
- lw_factor: 0.1
- ch: 0.0001

**Small steps** (when within 0.2 of threshold):
- Kw: 0.01
- coef_mix_hyp: 0.02
- wind_factor: 0.05
- lw_factor: 0.05
- ch: 0.00005

## Constraints

Always maintain:
- Kw in [0.1, 0.5]
- coef_mix_hyp in [0.3, 0.7]
- wind_factor in [0.7, 1.3]
- lw_factor in [0.7, 1.3]
- ch in [0.0005, 0.002]

DO NOT modify: sw_factor, cd, ce, initial profiles, time period, or forcing data.

## Convergence Criteria

Stop tuning when:
1. overall_rmse < 1.60 AND
2. annual_deep_rmse < 1.55 AND
3. summer_deep_rmse < 1.70

If one metric oscillates around threshold after >20 iterations, accept as best feasible solution within constraints.

## Documentation

Record for each iteration:
- Parameters tested
- RMSE results (all three metrics)
- Number of matched pairs (overall, annual_deep, summer_deep)
- Reasoning for next parameter adjustment
- Iteration number and date
