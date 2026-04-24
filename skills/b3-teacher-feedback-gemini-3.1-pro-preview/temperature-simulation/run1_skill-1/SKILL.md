[SKILL]
---
name: glm-nml-parameter-editor
description: Safely modifies specific calibration parameters in a GLM Fortran namelist (`glm3.nml`) using regular expressions, ensuring that restricted variables and formatting remain completely unchanged.
---

### Modifying GLM Namelists Safely
The General Lake Model (GLM) relies on a Fortran namelist file (typically `glm3.nml`) for configuration. When automating calibration, standard parsers like `f90nml` can sometimes reformat the file, inadvertently changing the initialization arrays (like `the_depths`, `the_temps`) or breaking strict parser rules. 

Using regular expressions to target and replace specific parameter values is often the safest approach when you have strict