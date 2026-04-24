---
name: generate-counting-csv
description: Use this skill to generate the final CSV file at /root/counting_results.csv with columns frame_id, coins, enemies, turtles. Frame IDs must be in the format /root/keyframes_%03d.png.
---

## CSV format specification

The output CSV file must be at `/root/counting_results.csv` with the following structure:

```
frame_id,coins,enemies,turtles
/root/keyframes_001.png,3,1,0
/root/keyframes_002.png,2,0,1
...
```

### Requirements

- **Columns**: `frame_id`, `coins`, `enemies`, `turtles` (exactly these names, in this order)
- **frame_id format**: `/root/keyframes_%03d.png` — zero-padded 3-digit numbers starting from 001
- **Rows**: One per keyframe, sorted in timeline order (001, 002, 003, ...)
- **Values**: Non-negative integers for coins, enemies, turtles

### Writing the CSV

```python
import csv

# results is a list of dicts with keys: frame_id, coins, enemies, turtles
with open('/root/counting_results.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['frame_id', 'coins', 'enemies', 'turtles'])
    writer.writeheader()
    writer.writerows(results)
```

### Verification

```python
import csv

with open('/root/counting_results.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    print(f"Number of rows: {len(rows)}")
    print(f"Columns: {reader.fieldnames}")
    for row in rows:
        print(row)
```

Check that:
1. The number of rows matches the number of extracted keyframes
2. All frame_id values follow the `/root/keyframes_%03d.png` format
3. All count values are valid integers >= 0