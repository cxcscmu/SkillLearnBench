---
name: opencv-template-matching
description: Count occurrences of a template in a target image.
---

# OpenCV Template Matching

Use `cv2.matchTemplate` to find objects matching a template image in the main image. Multiple detections of the same object can be filtered via Non-Maximum Suppression (NMS).

```python
import cv2
import numpy as np

def count_objects(main_img_path, template_path, threshold=0.8):
    img_gray = cv2.imread(main_img_path, 0)
    template = cv2.imread(template_path, 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    
    rects = []
    for pt in zip(*loc[::-1]):
        rects.append([int(pt[0]), int(pt[1]), int(w), int(h)])
    
    # Apply non-maximum suppression (requires imutils.object_detection or cv2.dnn.NMSBoxes)
    rects, weights = cv2.groupRectangles(rects, 1, 0.2)
    return len(rects)
```
