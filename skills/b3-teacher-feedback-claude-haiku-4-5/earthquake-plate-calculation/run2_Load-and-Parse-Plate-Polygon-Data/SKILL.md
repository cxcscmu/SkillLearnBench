---
name: Load and Parse Plate Polygon Data
description: Load plate polygon GeoJSON and parse geometries correctly. Verify the column name used for plate identifiers (e.g., 'PlateName' or similar). Use this skill to prepare plate polygon data for containment checks.
---

```python
def load_plate_data(filepath):
    """
    Load plate polygon data and validate geometries.
    
    Args:
        filepath: Path to PB2002_plates.json
        
    Returns:
        GeoDataFrame with plate polygons and identifiers
    """
    plates = gpd.read_file(filepath)
    
    # Print available columns to identify plate name column
    print("Plate data columns:", plates.columns.tolist())
    print("Sample plate names:", plates.head())
    
    # Ensure geometry is valid
    plates = plates[plates.geometry.is_valid]
    plates = plates.reset_index(drop=True)
    
    return plates
```