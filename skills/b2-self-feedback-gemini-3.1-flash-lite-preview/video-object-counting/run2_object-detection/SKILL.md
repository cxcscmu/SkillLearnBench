---
name: run2_object-detection
description: Counts object occurrences in an image using OpenCV template matching with non-maximum suppression.
---

## Overview
This skill uses template matching to locate objects and applies non-maximum suppression (NMS) to avoid double-counting overlapping regions.

## Usage
Use OpenCV `matchTemplate` and define an NMS function to filter overlapping results.

```python
import cv2
import numpy as np

def count_objects(scene_path, template_path, threshold=0.8):
    scene = cv2.imread(scene_path, 0)
    template = cv2.imread(template_path, 0)
    if scene is None or template is None: return 0
    
    res = cv2.matchTemplate(scene, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    matches = list(zip(*loc[::-1]))
    
    # Filter matches
    filtered_matches = []
    w, h = template.shape[::-1]
    for pt in matches:
        if not any(np.linalg.norm(np.array(pt) - np.array(f)) < max(w, h) * 0.5 for f in filtered_matches):
            filtered_matches.append(pt)
    return len(filtered_matches)
```
