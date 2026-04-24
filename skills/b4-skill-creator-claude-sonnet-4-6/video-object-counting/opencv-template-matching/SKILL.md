---
name: opencv-template-matching
description: Count occurrences of an object in an image using OpenCV template matching (cv2.matchTemplate). Use this skill whenever the user needs to detect and count how many times a small reference image (template) appears in a larger image, such as counting coins, enemies, or other game sprites. Works on both grayscale and color images.
---

# Object Counting with OpenCV Template Matching

Count how many times a template image appears in a scene image using `cv2.matchTemplate`.

## Core Pattern

```python
import cv2
import numpy as np

def count_objects(scene_path, template_path, threshold=0.7):
    scene = cv2.imread(scene_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    # Try multiple scales if needed
    best_count = 0
    h, w = template.shape

    result = cv2.matchTemplate(scene, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)

    # Non-maximum suppression to avoid counting the same object multiple times
    points = list(zip(*locations[::-1]))  # (x, y) pairs
    count = nms_count(points, w, h)
    return count

def nms_count(points, w, h):
    """Count unique detections using simple grid-based NMS."""
    if not points:
        return 0
    used = set()
    count = 0
    for (x, y) in points:
        key = (x // (w // 2), y // (h // 2))
        if key not in used:
            used.add(key)
            count += 1
    return count
```

## Parameters

- `threshold` — confidence threshold (0.0–1.0). Start with 0.7; lower if missing detections, raise if false positives appear.
- `cv2.TM_CCOEFF_NORMED` — normalized cross-correlation; robust to lighting differences.

## Multi-Scale Matching (when template size differs from scene)

```python
scales = [0.5, 0.75, 1.0, 1.25, 1.5]
for scale in scales:
    resized = cv2.resize(template, None, fx=scale, fy=scale)
    if resized.shape[0] > scene.shape[0] or resized.shape[1] > scene.shape[1]:
        continue
    result = cv2.matchTemplate(scene, resized, cv2.TM_CCOEFF_NORMED)
    ...
```

## Writing Results to CSV

```python
import csv

rows = []
for frame_path in sorted_frames:
    coins = count_objects(frame_path, '/root/coin.png')
    enemies = count_objects(frame_path, '/root/enemy.png')
    turtles = count_objects(frame_path, '/root/turtle.png')
    rows.append({'frame_id': frame_path, 'coins': coins, 'enemies': enemies, 'turtles': turtles})

with open('/root/counting_results.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['frame_id', 'coins', 'enemies', 'turtles'])
    writer.writeheader()
    writer.writerows(rows)
```

## Tuning Tips

- If template and scene are both grayscale already, `IMREAD_GRAYSCALE` is fine.
- If counts seem off, visualize matches with `cv2.rectangle` to debug.
- For very small sprites (< 10px), lower NMS suppression window.
