---
name: Identify Pacific Plate Identifier
description: Examine the plates dataset to find the exact identifier used for the Pacific plate (e.g., "PA", "Pacific", etc.). Use this skill early in the analysis to ensure consistent filtering across boundaries and plates.
---

```python
def find_pacific_plate_id(plates_gdf):
    """
    Identify the correct Pacific plate identifier in the dataset.
    
    Args:
        plates_gdf: GeoDataFrame containing plate data
        
    Returns:
        String representing the Pacific plate identifier
    """
    # Find plate identifier column (commonly 'PlateName', 'Name', or similar)
    plate_name_col = None
    for col in plates_gdf.columns:
        if col.lower() in ['platename', 'name', 'plate']:
            plate_name_col = col
            break
    
    if plate_name_col is None:
        raise ValueError("Could not identify plate name column")
    
    unique_plates = plates_gdf[plate_name_col].unique()
    print("Unique plates:", unique_plates)
    
    # Search for Pacific plate variations
    pacific_id = None
    for plate in unique_plates:
        if 'pac' in str(plate).lower():
            pacific_id = plate
            break
    
    if pacific_id is None:
        raise ValueError(f"Pacific plate not found. Available plates: {unique_plates}")
    
    return pacific_id, plate_name_col
```