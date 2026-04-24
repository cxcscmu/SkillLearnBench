---
name: mars-cloud-data-loading-matching
description: Load citizen science and expert annotation datasets, match them by image using file_rad column, handle missing data, and prepare data for clustering evaluation.
---

## Data Files

Located in `/root/data/`:

- **`citsci_train.csv`** — Citizen science annotations
  - Columns: `file_rad`, `x`, `y`
  - Format: CSV
  - Content: Crowd-sourced point annotations of Mars clouds

- **`expert_train.csv`** — Expert annotations
  - Columns: `file_rad`, `x`, `y`
  - Format: CSV
  - Content: Ground truth point annotations by domain experts

## File Matching Logic

The `file_rad` column contains base filenames that identify which image a point belongs to.

**Important:** `file_rad` may contain variant suffixes in the original image filenames, but the base name (without variants) should be used to match between datasets.

Use string preprocessing to extract the base filename if needed.

## Data Loading Steps

1. Load both CSV files using pandas or similar
2. Verify column names: `file_rad`, `x`, `y`
3. Extract unique `file_rad` values from expert dataset (these are the "all unique images" reference set)
4. For each hyperparameter combination evaluation:
   - Loop over each unique image from expert dataset
   - Filter citizen science data: `citsci_data[citsci_data['file_rad'] == image_id]`
   - Filter expert data: `expert_data[expert_data['file_rad'] == image_id]`
   - Extract x, y coordinates as numpy arrays

## Data Types and Validation

- `file_rad`: String identifier
- `x`, `y`: Numeric (float or int)
- Ensure x, y are convertible to float for distance calculations
- Handle missing/null values:
  - If any column contains NaN, drop those rows or skip those images
  - Log warnings for skipped images

## Coordinate System

- Coordinates are in pixel space (typically 0–2000 range for Mars orbital imagery)
- Use standard Euclidean distance for all metrics except DBSCAN clustering
- Distance thresholds and parameters are in pixel units