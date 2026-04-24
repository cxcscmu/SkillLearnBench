---
name: glm-calibration
description: Calibrating GLM parameters (Kw, coef_mix_hyp, wind_factor, lw_factor, ch) to minimize RMSE against field observations.
---

# GLM Calibration Skill

## Allowed Calibration Parameters
| Parameter | Range | Description |
|-----------|-------|-------------|
| `Kw` | [0.1, 0.5] | Light extinction coefficient (m⁻¹) - affects thermocline depth |
| `coef_mix_hyp` | [0.3, 0.7] | Hypolimnetic mixing coefficient - affects deep mixing |
| `wind_factor` | [0.7, 1.3] | Wind speed scaling - affects surface mixing |
| `lw_factor` | [0.7, 1.3] | Longwave radiation scaling - affects surface heat budget |
| `ch` | [0.0005, 0.002] | Sensible heat transfer coefficient |

## Physical Intuition
- **Higher Kw**: More light attenuation, shallower thermocline, warmer epilimnion
- **Higher coef_mix_hyp**: More hypolimnetic mixing, warmer deeper waters
- **Higher wind_factor**: More surface mixing, weaker stratification
- **Higher lw_factor**: More downward longwave radiation, warmer surface
- **Higher ch**: More sensible heat exchange with atmosphere

## Calibration Strategy
1. Start with default parameters and compute baseline RMSE
2. Focus on deep RMSE (depths ≥ 13m): primarily affected by `coef_mix_hyp`
3. Focus on overall RMSE: balance all parameters
4. Use grid search or scipy.optimize for systematic calibration

## Modifying glm3.nml Parameters
```python
import re

def update_nml(param, value, nml_path='/root/glm3.nml'):
    with open(nml_path, 'r') as f:
        content = f.read()

    # For Kw in &light section
    if param == 'Kw':
        content = re.sub(r'Kw\s*=\s*[\d.]+', f'Kw = {value}', content)
    elif param == 'coef_mix_hyp':
        content = re.sub(r'coef_mix_hyp\s*=\s*[\d.]+', f'coef_mix_hyp = {value}', content)
    elif param == 'wind_factor':
        content = re.sub(r'wind_factor\s*=\s*[\d.]+', f'wind_factor = {value}', content)
    elif param == 'lw_factor':
        content = re.sub(r'lw_factor\s*=\s*[\d.]+', f'lw_factor = {value}', content)
    elif param == 'ch':
        content = re.sub(r'ch\s*=\s*[\d.]+', f'ch = {value}', content)

    with open(nml_path, 'w') as f:
        f.write(content)
```

## Running GLM and Computing Metrics
```python
import subprocess
result = subprocess.run(['glm'], cwd='/root', capture_output=True, text=True)
if result.returncode != 0:
    print("GLM failed:", result.stderr)
else:
    # Compute metrics from output.nc
    pass
```

## Typical Good Values for Lake Mendota
- `Kw`: ~0.25-0.35 (moderately productive lake)
- `coef_mix_hyp`: ~0.4-0.6
- `wind_factor`: ~0.9-1.1
- `lw_factor`: ~0.95-1.05
- `ch`: ~0.0010-0.0015
