---
name: glm_output_parsing
description: Use this skill to correctly parse GLM NetCDF output (output.nc) into a DataFrame of (datetime, depth, temperature) triples. Handles the 4D variable shape (ntime, nlayer, 1, 1), correct depth conversion using fixed lake_depth from glm3.nml, and datetime reconstruction using manual timedelta from a fixed reference date.
---

# GLM Output Parsing

## Key Facts About GLM NetCDF Output
- Variables `z` and `temp` have shape `(n_times, n_layers, 1, 1)` — always index with `[:, :, 0, 0]`
- `z` contains layer *elevations* (meters above lake bottom), not depths
- Depth = `lake_depth - z_elevation` where `lake_depth` is the **fixed** constant from `glm3.nml`
- Time is stored as hours since simulation start; use manual timedelta, not `num2date`, to avoid cftime/timezone issues
- Layers may have NaN/fill values — filter those out

## Parsing Function

```python
import netCDF4 as nc
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def parse_glm_output(nc_path='/root/output/output.nc', lake_depth=25.0):
    """
    Parse GLM NetCDF output into a DataFrame.
    
    Parameters
    ----------
    nc_path : str
        Path to output.nc
    lake_depth : float
        Fixed maximum lake depth from glm3.nml (e.g., from get_lake_depth_from_nml)
    
    Returns
    -------
    pd.DataFrame with columns: datetime, depth, sim_temp
    """
    ds = nc.Dataset(nc_path, 'r')
    
    # Time: hours since start — reconstruct manually
    time_var = ds.variables['time']
    time_vals = time_var[:]  # shape (n_times,)
    
    # Parse units string: "hours since YYYY-MM-DD HH:MM:SS"
    units_str = time_var.units  # e.g., "hours since 2009-01-01 00:00:00"
    # Extract reference date from units
    parts = units_str.split('since')
    ref_str = parts[1].strip().split('.')[0].strip()
    # Try multiple formats
    for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
        try:
            ref_date = datetime.strptime(ref_str, fmt)
            break
        except ValueError:
            continue
    
    # z and temp: shape (n_times, n_layers, 1, 1)
    z_all = ds.variables['z'][:]        # elevations above bottom
    temp_all = ds.variables['temp'][:]  # temperatures
    
    ds.close()
    
    n_times = len(time_vals)
    records = []
    
    for t_idx in range(n_times):
        # Reconstruct datetime
        dt = ref_date + timedelta(hours=float(time_vals[t_idx]))
        
        # Extract layer values for this timestep — shape (n_layers,)
        z_layers = z_all[t_idx, :, 0, 0]
        temp_layers = temp_all[t_idx, :, 0, 0]
        
        for i in range(len(z_layers)):
            z_val = float(z_layers[i])
            t_val = float(temp_layers[i])
            
            # Skip fill/NaN values
            if np.isnan(z_val) or np.isnan(t_val):
                continue
            if z_val < -1e10 or t_val < -1e10:
                continue
            
            # Convert elevation to depth
            depth = lake_depth - z_val
            if depth < 0:
                depth = 0.0
            
            records.append({
                'datetime': dt,
                'depth': depth,
                'sim_temp': t_val
            })
    
    df = pd.DataFrame(records)
    return df
```

## Usage Example

```python
from glm_lake_mendota_setup import get_lake_depth_from_nml

lake_depth = get_lake_depth_from_nml('/root/glm3.nml')
sim_df = parse_glm_output('/root/output/output.nc', lake_depth=lake_depth)
print(sim_df.head())
print(f"Depth range: {sim_df['depth'].min():.1f} – {sim_df['depth'].max():.1f} m")
print(f"Time range: {sim_df['datetime'].min()} – {sim_df['datetime'].max()}")
```