---
name: glm-calibration
description: Calibrating the General Lake Model (GLM) by modifying parameter bounds for lake simulation.
---

# glm-calibration

This skill involves adjusting physical coefficients such as Kw, wind_factor, and sensible heat flux in a model configuration file (e.g., `glm3.nml`) to optimize the root mean square error (RMSE) against observations.

## Example Pattern
```python
import f90nml
import subprocess

def run_simulation(params):
    # Load default settings
    nml = f90nml.read('glm3.nml')

    # Assign new parameters
    nml['light']['Kw'] = params['Kw']
    nml['meteorology']['wind_factor'] = params['wind_factor']

    # Overwrite configuration
    nml.write('glm3_new.nml', force=True)
    
    # Run GLM executable with new parameters
    subprocess.run(['glm', '--nml', 'glm3_new.nml'])
```