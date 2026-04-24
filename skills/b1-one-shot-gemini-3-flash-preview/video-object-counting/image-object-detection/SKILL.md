---
name: image-object-detection
description: Techniques for image preprocessing and template matching to count objects in images.
---

# Image Object Detection

This skill covers grayscale conversion and template matching using Python's `opencv-python` and `numpy`.

## Grayscale Conversion

Converting an image to grayscale simplifies the data and is often a prerequisite for template matching.

```python
import cv2

def convert_to_grayscale(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(image_path, gray) # Overwrite original
```

## Template Matching for Object Counting

Template matching finds instances of a small "template" image within a larger "source" image.

```python
import cv2
import numpy as np

def count_objects(source_path, template_path, threshold=0.8):
    source = cv2.imread(source_path, 0) # Read as grayscale
    template = cv2.imread(template_path, 0) # Read as grayscale
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(source, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    
    # Group nearby matches to avoid double counting
    points = list(zip(*loc[::-1]))
    if not points:
        return 0
    
    rects = []
    for pt in points:
        rects.append([pt[0], pt[1], pt[0] + w, pt[1] + h])
    
    # Use cv2.groupRectangles to merge overlapping detections
    rects, weights = cv2.groupRectangles(rects, 1, 0.2)
    return len(rects)
```

### Key Considerations:
- **Threshold**: Adjust the threshold (usually 0.7 to 0.9) to balance precision and recall.
- **Scale**: Template matching is sensitive to scale. Ensure the template and objects in the source are roughly the same size.
- **Preprocessing**: Grayscale conversion is crucial for consistent results.
