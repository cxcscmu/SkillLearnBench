---
name: run_glm_simulation
description: Executes the GLM simulation and retrieves lake-specific depth data to ensure accurate mapping between model output and field observations.
---

Before processing, extract the `lake_depth` from the `&init_profiles` section of the namelist to correctly derive the depth of water layers (`depth = lake_depth - z`). Ensure the output at `/root/output/output.nc` is generated successfully.

```python
import subprocess
import f90nml
import xarray as xr

def run_simulation():
    # Extract lake depth from nml for correct depth calculation
    nml = f90nml.read('/root/glm3.nml')
    lake_depth = nml['init_profiles']['lake_depth']
    
    # Run the model
    subprocess.run(['glm', 'x86_64', '--nml', '/root/glm3.nml'], check=True)
    return lake_depth
```