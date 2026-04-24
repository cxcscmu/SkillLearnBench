---
name: object-counting-in-images
description: Detect and count occurrences of template images within a larger target image.
---

# Object Counting

To count occurrences of a template object within a scene image, use OpenCV in Python:

```python
import cv2
import numpy as np

def count_objects(scene_path, template_path, threshold=0.8):
    img = cv2.imread(scene_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    w, h = template.shape[::-1]
    
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    
    # Filter matches to ensure they are distinct objects
    count = 0
    matches = []
    for pt in zip(*loc[::-1]):
        if not any([abs(pt[0]-m[0]) < w and abs(pt[1]-m[1]) < h for m in matches]):
            matches.append(pt)
            count += 1
    return count
```
