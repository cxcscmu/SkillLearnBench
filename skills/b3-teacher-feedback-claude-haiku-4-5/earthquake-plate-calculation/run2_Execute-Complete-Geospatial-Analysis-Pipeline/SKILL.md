---
name: Execute Complete Geospatial Analysis Pipeline
description: Orchestrate the full analysis workflow: load data, identify Pacific plate, filter earthquakes and boundaries, project to EPSG:4087, calculate distances, find the furthest earthquake, and save results. Use this as the main execution skill.
---

```python
def execute_analysis():
    """
    Execute the complete geospatial analysis pipeline.
    """
    # Load all data
    earthquakes = load_earthquake_data('/root/earthquakes_2024.json')
    plates = load_plate_data('/root/PB2002_plates.json')
    boundaries = load_boundary_data('/root/PB2002_boundaries.json')
    
    # Identify Pacific plate
    pacific_id, plate_name_col = find_pacific_plate_id(plates)
    print(f"Pacific plate identifier: {pacific_id}")
    
    # Filter earthquakes and boundaries
    earthquakes_pacific = filter_earthquakes_within_pacific(earthquakes, plates, pacific_id, plate_name_col)
    boundaries_pacific = filter_pacific_boundaries(boundaries, pacific_id)
    
    # Project to EPSG:4087
    earthquakes_proj, boundaries_proj = project_for_distance_calculation(earthquakes_pacific, boundaries_pacific)
    
    # Calculate distances
    earthquakes_with_dist = calculate_distances_to_boundary(earthquakes_proj, boundaries_proj)
    
    # Find furthest earthquake
    result = find_furthest_earthquake(earthquakes_with_dist)
    
    # Save to JSON
    save_result_to_json(result)
    
    return result

# Execute
execute_analysis()
```