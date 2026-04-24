---
name: Output Result to JSON File
description: Write the final result dictionary to a JSON file at `/root/answer.json` with proper formatting and field validation. Use this skill as the final step to save the analysis result.
---

```python
import json

def save_result_to_json(result, output_path='/root/answer.json'):
    """
    Save result to JSON file with proper formatting.
    
    Args:
        result: Dictionary with earthquake result data
        output_path: Path where JSON file should be written
    """
    # Validate all required fields are present
    required_fields = ['id', 'place', 'time', 'magnitude', 'latitude', 'longitude', 'distance_km']
    for field in required_fields:
        if field not in result:
            raise ValueError(f"Missing required field: {field}")
    
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"Result saved to {output_path}")
```