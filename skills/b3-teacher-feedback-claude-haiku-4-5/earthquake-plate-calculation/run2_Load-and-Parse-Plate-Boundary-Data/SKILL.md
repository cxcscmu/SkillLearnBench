---
name: Load and Parse Plate Boundary Data
description: Load plate boundary GeoJSON and create a GeoDataFrame with proper geometry parsing. Verify column names (PlateA, PlateB) match the dataset structure. Use this skill to prepare boundary data before filtering for Pacific plate relevance.
---

```python
def load_boundary_data(filepath):
    """
    Load plate boundary data and parse geometries correctly.
    
    Args:
        filepath: Path to PB2002_boundaries.json
        
    Returns:
        GeoDataFrame with boundary geometries and plate identifiers
    """
    boundaries = gpd.read_file(filepath)
    
    # Verify expected columns exist
    if 'PlateA' not in boundaries.columns or 'PlateB' not in boundaries.columns:
        print("Available columns:", boundaries.columns.tolist())
        raise ValueError("PlateA and PlateB columns not found")
    
    # Ensure geometry is valid
    boundaries = boundaries[boundaries.geometry.is_valid]
    boundaries = boundaries.reset_index(drop=True)
    
    return boundaries
```