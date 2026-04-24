---
name: run2_parameter-optimization-strategy
description: Systematic parameter search strategies for GLM calibration with multiple metrics
---

# Parameter Optimization Strategy for GLM

## Challenge
GLM has 5 calibration parameters to optimize across 3 RMSE metrics with tight thresholds:
- overall_rmse < 1.60
- annual_deep_rmse < 1.55 (depth ≥13m)
- summer_deep_rmse < 1.70 (Jun-Sep, depth ≥13m)

Brute force grid search becomes expensive quickly (10^5 combinations at 5-10 minutes each).

## Optimization Strategy

### Phase 1: Diagnosis

Before optimization, run one baseline simulation and diagnose:

```python
def diagnose_baseline():
    """Identify which metrics fail and by how much"""
    metrics = compute_metrics()

    failures = {}
    for key, threshold in THRESHOLDS.items():
        if metrics[key] >= threshold:
            gap = metrics[key] - threshold
            failures[key] = gap

    return metrics, failures

# Example diagnosis:
# overall_rmse: 7.421 (gap: +5.821)
# annual_deep_rmse: 8.022 (gap: +6.472)  ← Largest error
# summer_deep_rmse: 10.949 (gap: +9.249) ← Worst metric
```

### Phase 2: Domain Knowledge Application

Before systematic search, use physical reasoning:

#### Temperature Profile Issues

If all metrics show overestimation of temperatures (sim > obs):
- **Increase heat loss**: Raise `ch` (sensible heat transfer)
- **Reduce heating**: Lower `lw_factor` (longwave radiation)
- **Reduce light penetration**: Lower `Kw` (more opaque water)

If simulation shows stratification issues:
- **Reduce mixing**: Lower `coef_mix_hyp` (less hypolimnetic mixing)
- **Increase mixing**: Raise `coef_mix_hyp` (more mixing)
- **Adjust wind effect**: Modify `wind_factor`

#### Deep Water Specifics

If annual_deep_rmse >> overall_rmse:
- Problem is concentrated in deep water (>13m)
- Likely: Deep water stratification or mixing is wrong
- Adjust: `coef_mix_hyp` primarily, possibly `Kw`

If summer_deep_rmse is worst:
- Summer stratification is wrong
- Likely: `wind_factor` or `coef_mix_hyp` issues
- Adjust: Focus on stability/mixing parameters

### Phase 3: Focused Grid Search

Don't search all 5 parameters simultaneously. Use sequential focusing:

#### Tier 1: Most Impactful Parameters
Start with 2-3 parameters showing largest physical effects:

```python
# Example: Cooling-focused search
test_configs = []
for ch in [0.0015, 0.0017, 0.0019, 0.002]:           # Heat loss
    for lw_factor in [0.7, 0.85, 1.0]:               # Atmospheric heating
        for kw in [0.1, 0.2, 0.3]:                   # Light penetration
            # Keep other parameters at baseline
            test_configs.append({
                ('meteorology', 'ch'): ch,
                ('meteorology', 'lw_factor'): lw_factor,
                ('light', 'Kw'): kw,
                ('mixing', 'coef_mix_hyp'): 0.5,      # Default
                ('meteorology', 'wind_factor'): 1.0   # Default
            })
# Total: 4 × 3 × 3 = 36 tests
```

#### Tier 2: Secondary Parameters
Once best Tier 1 parameters identified, optimize secondary:

```python
# Keep best from Tier 1, vary mixing and wind
best_ch = 0.0019
best_lw = 0.85
best_kw = 0.2

for coef_mix_hyp in [0.3, 0.4, 0.5, 0.6, 0.7]:
    for wind_factor in [0.8, 0.9, 1.0, 1.1, 1.2]:
        test_configs.append({
            ('meteorology', 'ch'): best_ch,
            ('meteorology', 'lw_factor'): best_lw,
            ('light', 'Kw'): best_kw,
            ('mixing', 'coef_mix_hyp'): coef_mix_hyp,
            ('meteorology', 'wind_factor'): wind_factor
        })
# Total: 5 × 5 = 25 tests
```

### Phase 4: Sensitivity Analysis

Identify parameters most affecting each metric:

```python
def compute_sensitivity(baseline_params, param_to_vary, values):
    """Test parameter range, return sensitivity"""

    rmse_results = {name: [] for name in ['overall', 'annual_deep', 'summer_deep']}

    for value in values:
        test_params = baseline_params.copy()
        test_params[param_to_vary] = value

        metrics = test_parameter_set(test_params)
        rmse_results['overall'].append(metrics['overall_rmse'])
        rmse_results['annual_deep'].append(metrics['annual_deep_rmse'])
        rmse_results['summer_deep'].append(metrics['summer_deep_rmse'])

    # Compute sensitivity (change in RMSE / change in parameter)
    return rmse_results
```

## Metric-Specific Optimization

### Reduce overall_rmse
Focus on: `Kw`, `lw_factor`, `ch` (temperature regulation)

### Reduce annual_deep_rmse
Focus on: `coef_mix_hyp` (deep water mixing), `Kw`

### Reduce summer_deep_rmse
Focus on: `coef_mix_hyp`, `wind_factor` (stratification in warm season)

## Practical Workflow

```python
def optimize():
    print("1. Baseline diagnosis...")
    metrics, failures = diagnose_baseline()

    if all(m < t for m, t in zip(metrics.values(), THRESHOLDS.values())):
        print("✓ All metrics already meet thresholds!")
        return metrics

    print(f"\n2. Identifying main issues...")
    if failures['summer_deep_rmse'] > 5:  # Large error
        print("   Focus: summer stratification and deep mixing")
        # Run Tier 1 with coef_mix_hyp, wind_factor emphasis

    print(f"\n3. Running focused grid search...")
    best_metrics = run_tier1_optimization()

    print(f"\n4. Refining with Tier 2...")
    final_metrics = run_tier2_optimization(best_metrics)

    return final_metrics
```

## Success Criteria

Stop optimization when:
- All three RMSE metrics below thresholds, OR
- No improvement after 50+ tests with top parameters tried multiple ways, OR
- Resource limits reached

## Parameter Interaction Effects

Some parameter combinations interact:
- `ch` × `lw_factor`: Both affect surface heat balance
- `coef_mix_hyp` × `wind_factor`: Both affect stratification strength
- `Kw` × `coef_mix_hyp`: Light penetration affects density gradients, which interact with mixing

Consider this when choosing next test after each tier.
