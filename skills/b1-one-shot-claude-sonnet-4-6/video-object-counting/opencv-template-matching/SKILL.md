---
name: opencv-template-matching
description: Count occurrences of a template object in an image using OpenCV template matching with NMS.
---

# OpenCV Template Matching for Object Counting

## Installation
```bash
pip install opencv-python numpy
```

## Basic Template Matching
```python
import cv2
import numpy as np

def count_objects(scene_path, template_path, threshold=0.7):
    scene = cv2.imread(scene_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    # Resize template if needed (optional multi-scale)
    result = cv2.matchTemplate(scene, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    return len(locations[0])
```

## With Non-Maximum Suppression (NMS) to Avoid Duplicates
```python
import cv2
import numpy as np

def count_objects_nms(scene_path, template_path, threshold=0.7):
    scene = cv2.imread(scene_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    h, w = template.shape[:2]

    result = cv2.matchTemplate(scene, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)

    boxes = []
    scores = []
    for pt in zip(*locations[::-1]):  # (x, y) pairs
        boxes.append([pt[0], pt[1], pt[0] + w, pt[1] + h])
        scores.append(result[pt[1], pt[0]])

    if not boxes:
        return 0

    boxes = np.array(boxes, dtype=np.float32)
    scores = np.array(scores, dtype=np.float32)
    indices = cv2.dnn.NMSBoxes(
        boxes.tolist(), scores.tolist(),
        score_threshold=threshold, nms_threshold=0.3
    )
    return len(indices)
```

## Multi-Scale Matching (handles size variation)
```python
def count_objects_multiscale(scene_path, template_path, threshold=0.7, scales=None):
    if scales is None:
        scales = [0.5, 0.75, 1.0, 1.25, 1.5]

    scene = cv2.imread(scene_path, cv2.IMREAD_GRAYSCALE)
    template_orig = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    all_boxes, all_scores = [], []

    for scale in scales:
        h = int(template_orig.shape[0] * scale)
        w = int(template_orig.shape[1] * scale)
        if h < 5 or w < 5:
            continue
        template = cv2.resize(template_orig, (w, h))
        result = cv2.matchTemplate(scene, template, cv2.TM_CCOEFF_NORMED)
        locs = np.where(result >= threshold)
        for pt in zip(*locs[::-1]):
            all_boxes.append([pt[0], pt[1], pt[0]+w, pt[1]+h])
            all_scores.append(result[pt[1], pt[0]])

    if not all_boxes:
        return 0
    indices = cv2.dnn.NMSBoxes(
        all_boxes, all_scores, threshold, nms_threshold=0.3
    )
    return len(indices)
```

## Threshold Guidelines
| Scenario | Threshold |
|----------|-----------|
| Exact match | 0.95+ |
| Near-identical | 0.85 |
| Moderate variation | 0.7 |
| Loose match | 0.5-0.6 |

## Notes
- `TM_CCOEFF_NORMED` is most robust; values range [-1, 1]
- NMS prevents counting the same object multiple times
- For grayscale scenes + templates, ensure both are loaded as grayscale
- Template must be smaller than scene image
