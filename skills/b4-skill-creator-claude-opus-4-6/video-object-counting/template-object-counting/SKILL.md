---
name: template-object-counting
description: Count occurrences of objects in images using OpenCV template matching. Use this skill when the user needs to detect and count specific objects (coins, enemies, items) in game screenshots or similar images using a reference template image.
---

# Template-Based Object Counting

Count object occurrences in an image using OpenCV's `matchTemplate` with non-maximum suppression.

## Algorithm

1. Load the scene image and template image (both grayscale)
2. Run `cv2.matchTemplate` with `cv2.TM_CCOEFF_NORMED`
3. Threshold the result to find match locations
4. Apply non-maximum suppression (NMS) to remove overlapping detections
5. Count remaining detections

## Python Implementation

```python
import cv2
import numpy as np

def count_objects(scene_path, template_path, threshold=0.8, nms_overlap=0.5):
    """Count template occurrences in a scene image."""
    scene = cv2.imread(scene_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    if scene is None or template is None:
        return 0

    th, tw = template.shape[:2]

    # Multi-scale template matching for robustness
    # Try the template at its original size
    result = cv2.matchTemplate(scene, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)

    # Collect bounding boxes
    boxes = []
    for pt in zip(*locations[::-1]):  # x, y
        boxes.append([pt[0], pt[1], pt[0] + tw, pt[1] + th])

    if not boxes:
        return 0

    # Non-maximum suppression
    boxes = np.array(boxes)
    scores = result[locations]
    indices = nms(boxes, scores, nms_overlap)

    return len(indices)

def nms(boxes, scores, overlap_thresh):
    """Non-maximum suppression to remove overlapping detections."""
    if len(boxes) == 0:
        return []

    x1, y1, x2, y2 = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = scores.argsort()[::-1]

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        overlap = (w * h) / areas[order[1:]]

        inds = np.where(overlap <= overlap_thresh)[0]
        order = order[inds + 1]

    return keep
```

## Threshold Tuning

- `threshold=0.8` is a good starting point for game sprites
- Lower (0.6-0.7) if objects have visual variations
- Higher (0.85-0.9) to reduce false positives
- Examine match scores to calibrate per-template

## Notes

- Both scene and template must be grayscale for consistent results
- NMS prevents double-counting overlapping detections
- For game sprites, single-scale matching usually suffices since sprites have fixed sizes
