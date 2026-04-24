---
name: object-counting
description: Use this skill to count occurrences of a template image within a larger target image using template matching techniques.
---

# Object Counting Skill

This skill provides instructions for counting objects in an image based on a template.

## Using OpenCV Template Matching

```python
import cv2
import numpy as np

def count_objects(image_path, template_path, threshold=0.8):
    img_gray = cv2.imread(image_path, 0)
    template = cv2.imread(template_path, 0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    
    # Simple counting (might need non-maximum suppression for better results)
    points = list(zip(*loc[::-1]))
    # Filter points to avoid double counting close matches
    filtered_points = []
    for p in points:
        if not any(np.linalg.norm(np.array(p) - np.array(fp)) < min(w, h)/2 for fp in filtered_points):
            filtered_points.append(p)
            
    return len(filtered_points)
```

## Considerations
- **Threshold**: Adjust the threshold based on the similarity required.
- **Scale/Rotation**: Template matching is sensitive to scale and rotation.
- **Non-Maximum Suppression**: Crucial for avoiding multiple detections of the same object.

## Output
The result should be an integer count of the detected objects.
