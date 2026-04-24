Please run the General Lake Model to simulate the vertical water temperature for Lake Mendota.

The data that you may use includes:
1. Meteorological and hydrological forcing data in `/root/bcs/`
2. Field water temperature observations data in `/root/field_temp_oxy.csv`
3. GLM configuration file in `/root/glm3.nml`

You should generate the simulation output from 2009-01-01 to 2015-12-30 at `/root/output/output.nc`.

This query is evaluated with three exact RMSE checks computed from the matched observation/simulation pairs obtained by an exact `datetime` + rounded-depth merge:
1. `overall_rmse < 1.60`
2. `annual_deep_rmse < 1.55`, where `annual_deep` means all matched pairs at rounded depths 13 m and deeper
3. `summer_deep_rmse < 1.70`, where `summer` means months June-September and `deep` again means rounded depths 13 m and deeper

Additional task rules:
1. You may modify only these calibration parameters in `/root/glm3.nml`: `Kw`, `coef_mix_hyp`, `wind_factor`, `lw_factor`, and `ch`.
2. Leave `sw_factor`, `cd`, `ce`, the initialization profile (`the_depths`, `the_temps`, `the_sals`), and all other settings unchanged.
3. Keep your final parameter values within these published calibration ranges: `Kw` in `[0.1, 0.5]`, `coef_mix_hyp` in `[0.3, 0.7]`, `wind_factor` in `[0.7, 1.3]`, `lw_factor` in `[0.7, 1.3]`, and `ch` in `[0.0005, 0.002]`.
4. Save your final exact self-evaluation to `/root/metrics.json` with JSON keys `overall_rmse`, `annual_deep_rmse`, `summer_deep_rmse`, `overall_n_pairs`, `annual_deep_n_pairs`, and `summer_deep_n_pairs`.
5. Do not use nearest-time matching, interpolation, or alternative depth binning in those final reported metrics.

I will verify that:
1. GLM runs successfully with the parameters you leave behind.
2. The final configuration still writes `/root/output/output.nc`.
3. Only the allowed calibration parameters were changed.
4. Your final parameter values stay within the published calibration ranges.
5. Your `/root/metrics.json` matches my exact recomputed metrics closely.
6. All three RMSE thresholds above are satisfied.
