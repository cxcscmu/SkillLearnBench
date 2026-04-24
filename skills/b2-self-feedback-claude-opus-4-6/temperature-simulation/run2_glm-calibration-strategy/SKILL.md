---
name: run2_glm-calibration-strategy
description: Two-phase grid search calibration for GLM parameters with parameter sensitivity analysis and regex-based nml editing.
---

# GLM Calibration Strategy

## Overview
Calibrate GLM by minimizing RMSE between simulated and observed temperature profiles using a two-phase grid search.

## Phase 1: Coarse Search (Most Impactful Parameters)
Test 3-4 values per parameter for Kw, coef_mix_hyp, wind_factor. Fix lw_factor=1.0, ch=0.0013.

```python
for kw in [0.20, 0.25, 0.30, 0.35]:
    for cmh in [0.4, 0.5, 0.6]:
        for wf in [0.85, 0.90, 0.95, 1.0]:
            # ~48 runs, ~2 min each = ~96 min
```

## Phase 2: Fine-Tune Secondary Parameters
Around best Phase 1 point, vary lw_factor and ch:
```python
for lw in [0.93, 0.95, 0.97, 1.0, 1.05]:
    for ch in [0.0010, 0.0012, 0.0013, 0.0015]:
```

## Phase 3 (Optional): Narrow Refinement
Small grid ±0.02 around best values across all 5 params:
```python
# Keep to ~100 combinations max for reasonable runtime
```

## Safe NML Parameter Editing
```python
import re

def set_param(nml_text, param, value):
    """Replace a parameter value in GLM nml text.

    Note: For 'ch', need to be careful not to match 'catchrain'.
    The pattern matches 'param = value' at any position.
    """
    pattern = rf'({param}\s*=\s*)[\d.eE+-]+'
    return re.sub(pattern, rf'\g<1>{value}', nml_text)
```

**Important**: Always read the original nml, apply ALL params fresh, then write. Don't accumulate edits.

## Scoring Function
Minimize total RMSE across all targets:
```python
score = overall_rmse + annual_deep_rmse + summer_deep_rmse
```

## Lake Mendota Calibrated Values
| Parameter | Default | Calibrated | Effect |
|-----------|---------|------------|--------|
| Kw | 0.30 | 0.35 | Increased extinction → cooler deep water |
| coef_mix_hyp | 0.50 | 0.45 | Slightly less hypolimnetic mixing |
| wind_factor | 1.00 | 0.88 | Reduced wind → stronger stratification |
| lw_factor | 1.00 | 0.93 | Reduced LW radiation → overall cooling |
| ch | 0.0013 | 0.0012 | Reduced sensible heat transfer |

**Results**: O=1.34, AD=1.10, SD=1.07 (all well below thresholds of 1.60, 1.55, 1.70)

## Key Lessons
- wind_factor < 1 and Kw slightly above default are the biggest improvements for deep metrics
- lw_factor < 1 provides overall cooling that helps all metrics
- The parameter space has multiple local minima; grid search is more robust than gradient descent here
- Each GLM run takes ~30-60 seconds; budget ~2-3 hours for thorough calibration
