---
name: parse-key-value-text
description: Parses a text file containing key-value pairs (like question IDs and question text) into a Python dictionary.
---

When reading a file that contains keys and values representing distinct items (e.g., `q1: What is the company name?`), you can extract them into a Python dictionary by iterating through the file and splitting each line by a predefined delimiter.

```python
def parse_key_value_file(file_path, delimiter=":"):
    """
    Reads a file with key-value pairs and returns a dictionary.
    
    Args:
        file_path (str): The path to the text file.
        delimiter (str): The character separating the key and the value.
    """
    parsed_data = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Split only on the first occurrence of the delimiter
            if delimiter in line:
                key, value = line.split(delimiter, 1)
                parsed_data[key.strip()] = value.strip()
            else:
                # Handle cases where the format might differ or fallback
                pass
                
    return parsed_data
```