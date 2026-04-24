---
name: glm-calibration
description: Calibration guidance for GLM tasks. Often most effective after glm-basics has clarified the setup; glm-output is the companion skill for exact final metric computation.
license: MIT
---
# GLM Calibration Guide

## Overview

GLM calibration involves adjusting physical parameters to minimize the difference between simulated and observed water temperatures. The goal is to satisfy the task's stated evaluation metrics, not just to lower a single aggregate RMSE.

## Suggested Skill Flow

This skill works best after `glm-basics` has confirmed the file layout and editable parameters. The job of this skill is to find a candidate parameter set that passes the task metrics. Once a candidate setting appears to pass, stop calibration and hand off immediately to `glm-output` for the final verifier-matching metrics and `/root/metrics.json`.

## Task Checklist

For tasks that restrict the editable parameter set and require an exact self-evaluation:

- Only adjust the parameters explicitly allowed by the task
- Leave protected parameters and initialization profiles unchanged
- Stop only when every required task metric passes; do not use global RMSE alone as the stopping condition
- If a configuration already passes every required task metric, stop the calibration search immediately
- Do not launch a broad refinement search after finding a passing configuration
- If the task requires `/root/metrics.json`, hand the final reporting step to `glm-output` instead of a separately improvised evaluator

## Important Tips

- In many case, the surface fit becomes acceptable before the deep water is fixed.
- Single-knob moves can improve whole-lake RMSE while leaving the task-defining deep subsets too warm.
- Do not optimize only the global RMSE. Recompute the full task metric set after each promising run.

## Key Calibration Parameters

| Parameter        | Section          | Description                          | Default | Range          |
| ---------------- | ---------------- | ------------------------------------ | ------- | -------------- |
| `Kw`           | `&light`       | Light extinction coefficient (m⁻¹) | 0.3     | 0.1 - 0.5      |
| `coef_mix_hyp` | `&mixing`      | Hypolimnetic mixing coefficient      | 0.5     | 0.3 - 0.7      |
| `wind_factor`  | `&meteorology` | Wind speed scaling factor            | 1.0     | 0.7 - 1.3      |
| `lw_factor`    | `&meteorology` | Longwave radiation scaling           | 1.0     | 0.7 - 1.3      |
| `ch`           | `&meteorology` | Sensible heat transfer coefficient   | 0.0013  | 0.0005 - 0.002 |

## Parameter Effects

| Parameter        | Increase Effect                           | Decrease Effect                           |
| ---------------- | ----------------------------------------- | ----------------------------------------- |
| `Kw`           | Less light penetration, cooler deep water | More light penetration, warmer deep water |
| `coef_mix_hyp` | More deep mixing, weaker stratification   | Less mixing, stronger stratification      |
| `wind_factor`  | More surface mixing                       | Less surface mixing                       |
| `lw_factor`    | More heat input                           | Less heat input                           |
| `ch`           | More sensible heat exchange               | Less heat exchange                        |

## Calibration with Optimization

```python
from scipy.optimize import minimize

def objective(x):
    Kw, coef_mix_hyp, wind_factor, lw_factor, ch = x

    params = {
        'Kw': round(Kw, 4),
        'coef_mix_hyp': round(coef_mix_hyp, 4),
        'wind_factor': round(wind_factor, 4),
        'lw_factor': round(lw_factor, 4),
        'ch': round(ch, 6)
    }
    modify_nml('glm3.nml', params)
    subprocess.run(['glm'], capture_output=True)
    return calculate_task_metrics(sim_df, obs_df)['overall_rmse']

result = minimize(
    objective,
    [0.3, 0.5, 1.0, 1.0, 0.0013],
    method='Nelder-Mead',
    options={'maxiter': 150}
)
```

## Manual Calibration Strategy

1. Start from the provided seed and compute the exact deep-band metrics, not just overall RMSE.
2. First test changes that improve the deep layer over the full record rather than only cooling the whole lake; `Kw` and `coef_mix_hyp` are usually the first levers to inspect.
3. Once the annual deep metric improves, use smaller adjustments to `wind_factor` and `lw_factor` to reduce whole-lake bias without undoing the deep-water gains.
4. Leave `ch` for final fine-tuning after the main structure is already close.
5. Prefer a short hypothesis-driven search: keep candidates that improve both deep metrics together, discard one-knob moves that only make the global RMSE look better, and stop as soon as one candidate passes every required task metric.
6. After the first passing configuration is found, rerun GLM once at that setting, switch to `glm-output`, write `/root/metrics.json`, and end the task if the exact final metrics also pass.

## Common Issues

| Issue                                            | Likely Cause                                          | Solution                                          |
| ------------------------------------------------ | ----------------------------------------------------- | ------------------------------------------------- |
| Surface too warm                                 | Low wind mixing                                       | Increase `wind_factor`                          |
| Deep water too warm                              | Too much light penetration                            | Increase `Kw`                                   |
| Weak stratification                              | Too much mixing                                       | Decrease `coef_mix_hyp`                         |
| Overall warm bias                                | Heat budget too high                                  | Decrease `lw_factor` or `ch`                  |
| Annual deep improves but summer deep still fails | Deep water cooled too weakly during stratified months | Keep `Kw` high and lower `lw_factor` slightly |

## Best Practices

- Keep parameters within the published ranges
- Use the deep-band metrics as the stopping condition, not surface fit alone
- Save time by evaluating a few structured candidates instead of a long blind optimizer
- After you find a passing parameter set, do not keep refining it blindly
- Rerun GLM once at the chosen setting, then use `glm-output` to write the exact metrics file immediately
- If `glm-output` confirms that the exact final metrics pass, stop there instead of reopening calibration
