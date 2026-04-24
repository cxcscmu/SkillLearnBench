---
name: update_glm_config
description: Safely updates specific calibration parameters in the glm3.nml file using f90nml, maintaining correct namelist group mapping and file integrity.
---

To update the configuration, use the `f90nml` library to parse the existing file. Map the parameters to their respective namelist groups: `Kw` to `&light`, `coef_mix_hyp` to `&mixing`, and `wind_factor`, `lw_factor`, and `ch` to `&meteorology`. 

```python
import f90nml

def update_glm_parameters(params):
    nml = f90nml.read('/root/glm3.nml')
    # Map parameters to their correct namelist groups
    nml['light']['Kw'] = params.get('Kw')
    nml['mixing']['coef_mix_hyp'] = params.get('coef_mix_hyp')
    nml['meteorology']['wind_factor'] = params.get('wind_factor')
    nml['meteorology']['lw_factor'] = params.get('lw_factor')
    nml['meteorology']['ch'] = params.get('ch')
    
    # Write back without modifying unrelated sections
    nml.write('/root/glm3.nml', force=True)
```