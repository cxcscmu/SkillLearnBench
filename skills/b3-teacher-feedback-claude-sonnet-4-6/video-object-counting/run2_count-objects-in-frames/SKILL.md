---
name: count-objects-in-frames
description: Count coins, enemies, and turtles in each keyframe using the provided count_objects.py script with threshold=0.9 and dedup_min_dist=3. Parse stdout for integer counts. Write results to /root/counting_results.csv.
---

## Count Objects in Frames and Write CSV

Use the provided `count_objects.py` script to count each object type in each frame. Parse the integer from stdout. Write results to CSV.

```python
#!/usr/bin/env python3
import glob
import subprocess
import csv
import os

keyframes = sorted(glob.glob('/root/keyframes_*.png'))

def count_objects(frame_path, object_image_path, threshold=0.9, dedup_min_dist=3):
    """Run count_objects.py script and parse the integer count from stdout."""
    cmd = [
        'python3', 'scripts/count_objects.py',
        '--tool', 'count',
        '--input_image', frame_path,
        '--object_image', object_image_path,
        '--threshold', str(threshold),
        '--dedup_min_dist', str(dedup_min_dist)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd='/root')
    output = result.stdout.strip()
    # Parse integer from output
    # The script prints the count directly, possibly as last token or whole line
    try:
        # Try to parse the entire output as int first
        count = int(output)
    except ValueError:
        # Try to find an integer in the output
        tokens = output.split()
        count = 0
        for token in reversed(tokens):
            try:
                count = int(token)
                break
            except ValueError:
                continue
    return count

rows = []
for frame_path in keyframes:
    frame_id = frame_path  # already in /root/keyframes_%03d.png format
    
    coins = count_objects(frame_path, '/root/coin.png')
    enemies = count_objects(frame_path, '/root/enemy.png')
    turtles = count_objects(frame_path, '/root/turtle.png')
    
    print(f"{frame_id}: coins={coins}, enemies={enemies}, turtles={turtles}")
    rows.append({
        'frame_id': frame_id,
        'coins': coins,
        'enemies': enemies,
        'turtles': turtles
    })

# Write CSV
csv_path = '/root/counting_results.csv'
with open(csv_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['frame_id', 'coins', 'enemies', 'turtles'])
    writer.writeheader()
    writer.writerows(rows)

print(f"CSV written to {csv_path}")
print(f"Total frames processed: {len(rows)}")
```

Save as `/root/count_and_write_csv.py` and run:
```bash
cd /root && python3 /root/count_and_write_csv.py
```

Verify the output:
```bash
cat /root/counting_results.csv
```

The CSV will have columns: `frame_id`, `coins`, `enemies`, `turtles` with frame_id values like `/root/keyframes_001.png`, `/root/keyframes_002.png`, etc., sorted in timeline order.