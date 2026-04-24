---
name: run2_object-counting
description: Count the number of object occurrences in an image using OpenCV template matching in Python.
---
# Object Counting

Count the number of objects in an image using computer vision, specifically Normalized Cross-Correlation (Template Matching).

## Usage

The `count_objects.py` script provided in the environment performs template matching and outputs the number of matches found.

```bash
python3 /root/.agents/skills/object_counter/scripts/count_objects.py \
    --tool count \
    --input_image <image_file> \
    --object_image <object_template_file> \
    --threshold <threshold_value> \
    --dedup_min_dist <distance>
```

**Arguments Explained:**
- `--input_image`: The target image where objects should be counted.
- `--object_image`: The template image of the object you are searching for.
- `--threshold`: The matching confidence threshold (e.g., `0.9` for high fidelity).
- `--dedup_min_dist`: Minimum pixel distance to deduplicate overlapping matches (e.g., `3`).

### Example

```bash
python3 /root/.agents/skills/object_counter/scripts/count_objects.py \
    --tool count \
    --input_image frame_001.png \
    --object_image coin.png \
    --threshold 0.9 \
    --dedup_min_dist 3
```

### Parsing Output

The script prints the result in the following format to standard output:
`There are X objects (\`<template_path>\`) in file: \`<image_path>\``

You can parse this programmatically using regular expressions in a Python wrapper script:
```python
import re, subprocess

result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
match = re.search(r'There are (\d+) objects', result.stdout)
if match:
    count = int(match.group(1))
```
