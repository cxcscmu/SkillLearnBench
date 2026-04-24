---
name: run2_glm-config
description: Advanced GLM configuration and calibration strategies for vertical temperature profiles.
---

# Advanced GLM Configuration

The General Lake Model (GLM) performance depends on several key parameters that govern energy balance and mixing.

## Calibration Parameters and Effects

- **Kw (Light Extinction):** Controls how deep light penetrates. Higher `Kw` keeps deep layers cooler and surface layers warmer. Range: `[0.1, 0.5]`.
- **wind_factor:** Scales input wind speed. Affects surface mixing and latent/sensible heat fluxes. Range: `[0.7, 1.3]`.
- **lw_factor:** Scales incoming longwave radiation. Affects the overall heat budget. Range: `[0.7, 1.3]`.
- **ch (Sensible Heat Transfer):** Bulk coefficient for sensible heat flux. Affects surface temperature. Range: `[0.0005, 0.002]`.
- **coef_mix_hyp:** Controls mixing below the thermocline. Lower values reduce heating of the hypolimnion. Range: `[0.3, 0.7]`.

## Configuration Workflow

1.  **Baseline Run:** Start with default parameters.
2.  **Energy Balance:** Adjust `lw_factor` and `ch` to align the overall temperature magnitude.
3.  **Stratification:** Adjust `Kw` and `wind_factor` to match the thermocline depth and surface temperatures.
4.  **Deep Mixing:** Adjust `coef_mix_hyp` to match deep water temperatures during summer.

Example `sed` command for precise replacement:
```bash
sed -i 's/\bKw\s*=\s*[0-9.e+-]*/Kw = 0.4/' glm3.nml
```
Or use Python regex for more complex cases.
