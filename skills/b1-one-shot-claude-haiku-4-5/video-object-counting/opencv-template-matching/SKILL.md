---
name: opencv-template-matching
description: Use OpenCV for image processing, grayscale conversion, and template matching to detect objects in images.
---

# OpenCV Template Matching for Object Detection

## Overview
OpenCV is a computer vision library that enables template matching - finding occurrences of a template image within a larger source image. This is useful for counting objects in screenshots or video frames.

## Installation
```bash
pip install opencv-python numpy
```

## Key Concepts

### Template Matching
Template matching works by sliding a smaller template image across a larger image and computing a similarity score at each position. Objects are detected where the score exceeds a threshold.

### Matching Methods
- `cv2.TM_CCOEFF`: Correlation coefficient (recommended for most cases)
- `cv2.TM_CCORR`: Cross correlation
- `cv2.TM_SQDIFF`: Sum of squared differences

## Usage Examples

### Convert RGB Image to Grayscale
```python
import cv2

# Read image in color
image = cv2.imread('image.png')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Save grayscale image (overwrites original)
cv2.imwrite('image.png', gray)
```

### Basic Template Matching
```python
import cv2
import numpy as np

def count_objects(image_path, template_path, threshold=0.8):
    """Count occurrences of template in image"""
    # Read images in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    # Perform template matching
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF)

    # Find locations where correlation exceeds threshold
    locations = np.where(result >= threshold)

    # Count unique objects (accounting for nearby detections)
    count = len(locations[0])
    return count, locations
```

### Advanced: Non-Maximum Suppression
Template matching often produces overlapping detections. Use non-maximum suppression to remove duplicates:

```python
import cv2
import numpy as np

def count_objects_nms(image_path, template_path, threshold=0.8, min_distance=10):
    """Count objects using non-maximum suppression"""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF)

    # Get all locations above threshold with their scores
    locations = np.where(result >= threshold)
    scores = result[locations]

    # Convert to list of (x, y, score) tuples
    detections = list(zip(locations[1], locations[0], scores))

    # Sort by score descending
    detections.sort(key=lambda x: x[2], reverse=True)

    # Apply non-maximum suppression
    kept = []
    for x, y, score in detections:
        # Check if too close to already kept detection
        too_close = False
        for kx, ky in kept:
            if abs(x - kx) < min_distance and abs(y - ky) < min_distance:
                too_close = True
                break
        if not too_close:
            kept.append((x, y))

    return len(kept), kept
```

### Full Object Counting Pipeline
```python
import cv2
import os

def process_frame_and_count(frame_path, template_path, threshold=0.8):
    """
    Complete pipeline: read image, convert to grayscale,
    count objects, and return count
    """
    # Read image in color first
    image = cv2.imread(frame_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Overwrite original file with grayscale version
    cv2.imwrite(frame_path, gray)

    # Read template in grayscale
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    # Perform template matching
    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF)

    # Count detections above threshold
    count = np.sum(result >= threshold)

    return count
```

## Tips

1. **Threshold Selection**: Start with 0.7-0.8 for strict matching, go lower if missing objects
2. **Template Size**: Larger templates are faster but less flexible. Use templates that match object size in frames
3. **Grayscale**: Converting to grayscale makes matching more robust to color variations
4. **Normalization**: For noisy results, normalize the result map before thresholding
5. **Multi-scale**: Consider extracting at different scales if object sizes vary

## Common Issues

- **No detections**: Lower threshold or verify template is similar to objects in image
- **Too many detections**: Apply non-maximum suppression to filter nearby matches
- **Memory issues**: Process large images in chunks or reduce resolution
