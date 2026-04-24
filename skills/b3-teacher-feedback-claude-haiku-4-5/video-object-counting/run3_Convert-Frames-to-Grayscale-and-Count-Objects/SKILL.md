---
name: Convert Frames to Grayscale and Count Objects
description: Processes all extracted keyframes by converting them to grayscale, then counts coins, enemies, and turtles in each frame using template matching. Generates a CSV file with frame-by-frame object counts. Use this as the main analysis pipeline after keyframe extraction.
---

```python
import os
import cv2
import subprocess
import csv
from pathlib import Path

# Step 3: Convert all keyframes to grayscale in-place
keyframes_dir = "/root"
keyframe_files = sorted([f for f in os.listdir(keyframes_dir) if f.startswith("keyframes_") and f.endswith(".png")])

for keyframe_file in keyframe_files:
    keyframe_path = os.path.join(keyframes_dir, keyframe_file)
    img = cv2.imread(keyframe_path)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(keyframe_path, gray_img)
    print(f"Converted {keyframe_file} to grayscale")

# Step 4, 5: Count objects in each frame
results = []

for keyframe_file in keyframe_files:
    keyframe_path = os.path.join(keyframes_dir, keyframe_file)
    
    # Extract frame number from filename (e.g., "keyframes_001.png" -> 1)
    frame_id = keyframe_file.replace("keyframes_", "").replace(".png", "")
    frame_id_int = int(frame_id)
    
    # Count coins
    coin_result = subprocess.run(
        ["python", "-m", "object_counter", "--tool", "count", "--input_image", keyframe_path, "--object_image", "/root/coin.png"],
        capture_output=True,
        text=True
    )
    coin_count = int(coin_result.stdout.strip())
    
    # Count enemies
    enemy_result = subprocess.run(
        ["python", "-m", "object_counter", "--tool", "count", "--input_image", keyframe_path, "--object_image", "/root/enemy.png"],
        capture_output=True,
        text=True
    )
    enemy_count = int(enemy_result.stdout.strip())
    
    # Count turtles
    turtle_result = subprocess.run(
        ["python", "-m", "object_counter", "--tool", "count", "--input_image", keyframe_path, "--object_image", "/root/turtle.png"],
        capture_output=True,
        text=True
    )
    turtle_count = int(turtle_result.stdout.strip())
    
    results.append({
        "frame_id": f"/root/keyframes_{frame_id}.png",
        "coins": coin_count,
        "enemies": enemy_count,
        "turtles": turtle_count
    })
    
    print(f"Frame {frame_id}: coins={coin_count}, enemies={enemy_count}, turtles={turtle_count}")

# Step 6: Generate CSV file
csv_path = "/root/counting_results.csv"
with open(csv_path, "w", newline="") as csvfile:
    fieldnames = ["frame_id", "coins", "enemies", "turtles"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in results:
        writer.writerow(row)

print(f"CSV file generated at {csv_path}")
```