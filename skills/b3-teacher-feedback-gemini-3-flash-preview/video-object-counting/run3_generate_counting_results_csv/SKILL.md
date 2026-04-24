---
name: generate_counting_results_csv
description: Aggregates counting data for all frames and objects into a final CSV file formatted as required.
---

Use `python3` to compile the results from individual object counts into a single CSV file located at `/root/counting_results.csv`.

```python
import csv
import glob
import os

def create_results_csv(frames_dir, results_data, output_file="/root/counting_results.csv"):
    """
    results_data: A list of dictionaries, each containing:
    {'frame_id': '/root/keyframes_001.png', 'coins': X, 'enemies': Y, 'turtles': Z}
    """
    fieldnames = ["frame_id", "coins", "enemies", "turtles"]
    
    # Ensure the data is sorted by frame_id to maintain timeline order
    results_data.sort(key=lambda x: x['frame_id'])
    
    with open(output_file, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results_data:
            writer.writerow(row)

# Example usage:
# results = []
# for frame in sorted(glob.glob("/root/keyframes_*.png")):
#     c = run_count_logic(frame, "coin.png")
#     e = run_count_logic(frame, "enemy.png")
#     t = run_count_logic(frame, "turtle.png")
#     results.append({"frame_id": frame, "coins": c, "enemies": e, "turtles": t})
# create_results_csv("/root", results)
```