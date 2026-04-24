---
name: csv_generation
description: Aggregate object counts into a structured CSV file.
---
Iterate through the sorted list of frame files, perform object detection for each, and write the data to `/root/counting_results.csv` with the header: `frame_id,coins,enemies,turtles`.

```python
import csv
import glob
import subprocess

files = sorted(glob.glob('/root/keyframes_*.png'))
with open('/root/counting_results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['frame_id', 'coins', 'enemies', 'turtles'])
    
    for file_path in files:
        counts = []
        for template in ['/root/coin.png', '/root/enemy.png', '/root/turtle.png']:
            result = subprocess.run(['python3', 'scripts/count_objects.py', '--image', file_path, '--template', template], capture_output=True, text=True)
            counts.append(result.stdout.strip())
        writer.writerow([file_path] + counts)
```