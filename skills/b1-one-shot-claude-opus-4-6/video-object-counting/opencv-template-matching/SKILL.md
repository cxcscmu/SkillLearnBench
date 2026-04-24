---
name: opencv-template-matching
description: Count occurrences of a template object in an image using OpenCV template matching with non-maximum suppression.
---

# OpenCV Template Matching for Object Counting

## Overview
Use `cv2.matchTemplate` to find all occurrences of a small template image within a larger scene image. Apply thresholding and non-maximum suppression to count distinct objects.

## Code

```python
import cv2
import numpy as np

def count_objects(scene_path, template_path, threshold=0.8):
    """Count occurrences of template in scene using template matching."""
    scene = cv2.imread(scene_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    if scene is None or template is None:
        return 0

    th, tw = template.shape[:2]

    # Multi-scale matching can help if objects vary in size
    result = cv2.matchTemplate(scene, template, cv2.TM_CCOEFF_NORMED)

    # Find locations above threshold
    locations = np.where(result >= threshold)
    points = list(zip(*locations[::-1]))  # (x, y) pairs

    if len(points) == 0:
        return 0

    # Non-maximum suppression to avoid double counting
    boxes = [(x, y, x + tw, y + th) for x, y in points]
    scores = [result[y, x] for x, y in points]

    indices = cv2.dnn.NMSBoxes(
        [(x, y, tw, th) for x, y, _, _ in boxes],
        scores,
        threshold,
        0.3  # NMS IoU threshold
    )

    return len(indices)
```

## Multi-scale variant
If templates may appear at different sizes, iterate over scale factors:

```python
def count_objects_multiscale(scene_path, template_path, threshold=0.8, scales=None):
    scene = cv2.imread(scene_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    if scales is None:
        scales = [1.0]

    all_boxes = []
    all_scores = []
    th, tw = template.shape[:2]

    for scale in scales:
        if scale != 1.0:
            new_w = int(tw * scale)
            new_h = int(th * scale)
            if new_w < 5 or new_h < 5:
                continue
            tmpl = cv2.resize(template, (new_w, new_h))
        else:
            tmpl = template
            new_w, new_h = tw, th

        if tmpl.shape[0] > scene.shape[0] or tmpl.shape[1] > scene.shape[1]:
            continue

        result = cv2.matchTemplate(scene, tmpl, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)
        points = list(zip(*locations[::-1]))

        for x, y in points:
            all_boxes.append((x, y, new_w, new_h))
            all_scores.append(float(result[y, x]))

    if not all_boxes:
        return 0

    indices = cv2.dnn.NMSBoxes(all_boxes, all_scores, threshold, 0.3)
    return len(indices)
```

## Threshold tuning
- `0.8` is a good default for pixel-perfect matches
- Lower to `0.6-0.7` for partial matches or slight variations
- Use `TM_CCOEFF_NORMED` for best results with varying brightness
