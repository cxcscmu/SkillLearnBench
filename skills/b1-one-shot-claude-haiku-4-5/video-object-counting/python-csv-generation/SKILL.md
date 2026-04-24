---
name: python-csv-generation
description: Generate structured CSV files from Python data using the csv module for tabular data export.
---

# Python CSV Generation

## Overview
The Python `csv` module provides functionality to read and write CSV (Comma-Separated Values) files. CSV is a standard format for tabular data that's widely compatible with spreadsheet applications.

## Installation
Built-in to Python, no installation needed.

## Basic Usage

### Writing CSV with DictWriter (Recommended)
```python
import csv

# Data to write
data = [
    {'frame_id': '/root/keyframes_001.png', 'coins': 5, 'enemies': 2, 'turtles': 1},
    {'frame_id': '/root/keyframes_002.png', 'coins': 3, 'enemies': 1, 'turtles': 0},
    {'frame_id': '/root/keyframes_003.png', 'coins': 7, 'enemies': 3, 'turtles': 2},
]

# Write to CSV file
with open('output.csv', 'w', newline='') as csvfile:
    fieldnames = ['frame_id', 'coins', 'enemies', 'turtles']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write header row
    writer.writeheader()

    # Write data rows
    writer.writerows(data)
```

### Writing CSV with writer (Simple approach)
```python
import csv

with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write header
    writer.writerow(['frame_id', 'coins', 'enemies', 'turtles'])

    # Write data rows
    writer.writerow(['/root/keyframes_001.png', 5, 2, 1])
    writer.writerow(['/root/keyframes_002.png', 3, 1, 0])
```

## Complete Example: Frame Analysis Results

```python
import csv
import os
from pathlib import Path

def write_counting_results(results, output_path):
    """
    Write object counting results to CSV.

    Args:
        results: List of dicts with keys:
                 'frame_id', 'coins', 'enemies', 'turtles'
        output_path: Path to output CSV file
    """
    fieldnames = ['frame_id', 'coins', 'enemies', 'turtles']

    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Results written to {output_path}")

# Example usage
results = [
    {
        'frame_id': '/root/keyframes_001.png',
        'coins': 5,
        'enemies': 2,
        'turtles': 1
    },
    {
        'frame_id': '/root/keyframes_002.png',
        'coins': 3,
        'enemies': 1,
        'turtles': 0
    }
]

write_counting_results(results, '/root/counting_results.csv')
```

## Tips

1. **newline=''**: Always use `newline=''` when opening CSV files to handle line endings correctly
2. **Fieldnames**: Define fieldnames in the exact order you want them in the CSV
3. **Data Consistency**: Ensure all rows have the same keys/columns
4. **Path Handling**: Convert Path objects to strings if using pathlib
5. **Reading CSV**: Use `csv.DictReader` to read back CSV files as dictionaries

## Reading CSV Files

```python
import csv

with open('output.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row)  # Each row is a dictionary
```

## Common Issues

- **Extra blank rows**: Use `newline=''` parameter
- **Encoding errors**: Specify `encoding='utf-8'` if needed
- **Quote handling**: Use `quoting=csv.QUOTE_MINIMAL` for automatic quoting
