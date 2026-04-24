---
name: glm-lake-calibration
description: >
  Calibrate the General Lake Model (GLM) for lake temperature simulation.
  Use this skill whenever calibrating GLM parameters, running GLM simulations,
  or tuning Kw, coef_mix_hyp, wind_factor, lw_factor, or ch to match observed
  water temperature profiles. Covers Lake Mendota and similar dimictic lakes.
---

# GLM Lake Calibration

## Key Calibration Parameters and Their Effects

These five parameters most influence vertical temperature structure:

| Parameter       | Range         | Effect |
|-----------------|---------------|--------|
| `Kw`            | [0.1, 0.5]   | Light extinction coefficient. Higher values trap more heat near surface, warming epilimnion and cooling hypolimnion. Controls thermocline sharpness. |
| `coef_mix_hyp`  | [0.3, 0.7]   | Hypolimnetic mixing coefficient. Higher values increase deep mixing, warming the hypolimnion and reducing stratification strength. |
| `wind_factor`   | [0.7, 1.3]   | Scales wind speed input. Higher values deepen the mixed layer and increase surface cooling via latent/sensible heat. |
| `lw_factor`     | [0.7, 1.3]   | Scales incoming longwave radiation. Higher values warm the surface. Affects overall heat budget. |
| `ch`            | [0.0005, 0.002] | Bulk transfer coefficient for sensible heat. Higher values increase sensible heat exchange, cooling the surface in summer. |

## Calibration Strategy for Lake Mendota

Lake Mendota is a large dimictic lake (43°N, max depth ~25m). Key calibration targets:

1. **Overall RMSE**: Get surface and mid-depth temperatures right first via `wind_factor` and `lw_factor`
2. **Deep temperature (≥13m)**: Controlled primarily by `Kw` and `coef_mix_hyp`
3. **Summer deep**: Most sensitive to `coef_mix_hyp` (hypolimnetic mixing during stratification)

### Recommended Calibration Approach

1. Start with reasonable defaults: Kw=0.30, coef_mix_hyp=0.5, wind_factor=1.0, lw_factor=1.0, ch=0.0013
2. Adjust `Kw` first — affects light penetration and thermal structure
3. Tune `coef_mix_hyp` — controls deep water warming during stratification
4. Fine-tune `wind_factor` and `lw_factor` for overall bias
5. Adjust `ch` last — fine-tunes surface heat exchange

### Parameter Interactions

- Increasing `Kw` + decreasing `coef_mix_hyp` = stronger stratification
- `wind_factor` and `ch` both affect surface heat loss but through different mechanisms
- `lw_factor` primarily shifts mean temperature of the whole lake

## Running GLM

```bash
cd /root && mkdir -p output && glm --xdisp
# Or simply: glm (if no X display needed, use glm 2>&1)
```

GLM reads `glm3.nml` from the current directory. Output goes to `output/output.nc`.

## Modifying Parameters in glm3.nml

Parameters are in Fortran namelist format. Key sections:
- `&light`: contains `Kw`
- `&mixing`: contains `coef_mix_hyp`
- `&meteorology`: contains `wind_factor`, `lw_factor`, `ch`
