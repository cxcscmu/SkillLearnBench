---
name: mars-cloud-data-grouping
description: Organizing annotation data by image identifiers to prepare for image-by-image clustering analysis.
---

The dataset uses a `file_rad` identifier to link citizen science observations to expert labels. Since evaluations must happen per image:

1.  Load CSVs using `pandas`.
2.  Pre-group the DataFrames using `.groupby('file_rad')` and store them in a dictionary for fast lookup.
3.  Ensure that the evaluation loop iterates over all `file_rad` values present in the **expert** dataset to account for missed detections (FNs).

```python
import pandas as pd

citsci = pd.read_csv('citsci_train.csv')
expert = pd.read_csv('expert_train.csv')

# Grouping for efficient access
cit_groups = {name: group[['x', 'y']].values for name, group in citsci.groupby('file_rad')}
exp_groups = {name: group[['x', 'y']].values for name, group in expert.groupby('file_rad')}

all_image_ids = expert['file_rad'].unique()
```