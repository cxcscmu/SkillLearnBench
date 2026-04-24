---
name: json-nested-list-formatting
description: Formats and saves answers to a JSON file where each entry requires a specific nested dictionary structure containing list-type values and positive numeric token counts.
---

When a task strictly requires JSON output where answers must be isolated into lists (even for single values) and metadata like token usage must be stored as numbers, it is critical to sanitize the data before passing it to `json.dump()`.

### Formatting Rules Implemented:
1. Output format requires dict structure: `{"q_id": {"answer": ["..."], "tokens": 123}}`.
2. `answer` must strictly be a list of items/names/ids. If there is only one item, it must be enclosed in a list.
3. `tokens` must be a positive numeric value, not a string.

```python
import json

def format_and_save_answers(results_dict, output_path):
    """
    results_dict format expected: 
    {
       'q1': {'answer': 'Value', 'tokens': 150},
       'q2': {'answer': ['Value1', 'Value2'], 'tokens': '40'}
    }
    """
    formatted_data = {}
    
    for q_id, data in results_dict.items():
        # 1. Ensure answer is a list
        ans = data.get('answer', [])
        if not isinstance(ans, list):
            # Convert single values to a list of length 1
            ans = [ans]
            
        # 2. Ensure tokens is a positive integer (not a string)
        try:
            tokens = int(data.get('tokens', 0))
        except ValueError:
            tokens = 0
            
        # Ensure it is positive
        if tokens <= 0:
            tokens = 1  # Fallback positive value if something goes wrong
            
        formatted_data[q_id] = {
            "answer": ans,
            "tokens": tokens
        }
        
    # Write to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(formatted_data, f, indent=4)
```