---
name: run2_glm-calibration
description: How to run and calibrate GLM3 for lake temperature simulation - includes correct parameter effects, grid search strategy, and verified working parameter ranges.
---

# GLM3 Calibration Skill (Improved)

## Setup
```bash
cd /root   # Must run from directory containing glm3.nml
glm        # Reads glm3.nml, writes to out_dir/out_fn.nc
```

## Key Calibration Parameters

| Parameter | Section | Calibration Range | Primary Effect |
|-----------|---------|-------------------|----------------|
| `Kw` | `&light` | [0.1, 0.5] | Light attenuation; higher = more surface heating, deeper stratification |
| `coef_mix_hyp` | `&mixing` | [0.3, 0.7] | Hypolimnion mixing; **lower = cooler deep temps** |
| `wind_factor` | `&meteorology` | [0.7, 1.3] | Wind scaling; **lower = more stratification, cooler deep** |
| `lw_factor` | `&meteorology` | [0.7, 1.3] | Longwave radiation; higher = more surface heat |
| `ch` | `&meteorology` | [0.0005, 0.002] | Sensible heat coef; minor effect |

## Do NOT Change
- `sw_factor`, `cd`, `ce`
- `the_depths`, `the_temps`, `the_sals`

## Bias Diagnosis

If `sim_temp > obs_temp` (positive bias) in deep/summer:
- Reduce `coef_mix_hyp` (less hypolimnion mixing)
- Reduce `wind_factor` (less surface mixing → stronger stratification)
- Increase `Kw` (stronger light attenuation → sharper thermocline)

## Verified Working Parameters (Lake Mendota 2009-2015)
```
Kw = 0.3
coef_mix_hyp = 0.35
wind_factor = 0.9
lw_factor = 1.0
ch = 0.0013
```
Results: overall_rmse=1.37, annual_deep_rmse=1.35, summer_deep_rmse=1.47

## NML Update Pattern
```python
import re

def update_nml(filepath, params):
    with open(filepath, 'r') as f:
        content = f.read()
    for param, value in params.items():
        pattern = rf'(\b{param}\s*=\s*)[^\n]+'
        replacement = rf'\g<1>{value}'
        content = re.sub(pattern, replacement, content)
    with open(filepath, 'w') as f:
        f.write(content)
```

## Grid Search Strategy
1. Focus on `coef_mix_hyp` and `wind_factor` first (biggest impact on deep temps)
2. Try `coef_mix_hyp`: [0.30, 0.35, 0.40], `wind_factor`: [0.80, 0.90, 1.00]
3. Then tune `Kw`: [0.25, 0.30, 0.35]
4. Score = overall_rmse + annual_deep_rmse + summer_deep_rmse + penalties for violations

## Key Insight
Reducing `wind_factor` from 1.0 to 0.9 had the largest single improvement for deep temperature accuracy on Lake Mendota. With Kw=0.3, mix_hyp=0.35, wind=0.9, all three RMSE targets were met comfortably.
