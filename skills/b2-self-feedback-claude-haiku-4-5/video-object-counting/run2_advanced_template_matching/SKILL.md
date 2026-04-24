---
name: run2_advanced_template_matching
description: Advanced OpenCV template matching with dynamic threshold tuning, robust NMS filtering, and multi-scale detection for object counting in images.
---

# Advanced Template Matching for Object Counting

## Overview
Robust object detection and counting using OpenCV with improved threshold selection, non-maximum suppression, and diagnostic capabilities.

## Installation
```bash
apt-get install python3-opencv
```

## Core Matching Methods

### TM_CCOEFF_NORMED (Recommended)
- Range: -1 to 1 (higher is better match)
- Best for: Objects similar to template
- Invariance: Not scale/rotation invariant

### TM_SQDIFF_NORMED (Alternative)
- Range: 0 to 1 (lower is better match)
- Best for: Precise matching

## Dynamic Threshold Selection

### Method 1: Percentile-Based (Adaptive)
```python
import numpy as np

def count_objects_adaptive(frame, template, percentile=95):
    """Count using adaptive threshold based on match distribution"""

    result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)

    # Use top X% of matches as threshold
    threshold = np.percentile(result.flatten(), percentile)

    loc = np.where(result >= threshold)
    matches = list(zip(*loc[::-1]))

    return matches, threshold
```

### Method 2: Histogram Analysis
```python
def find_optimal_threshold(result, min_matches=1):
    """Find threshold that yields reasonable match count"""

    flat = result.flatten()

    # Test thresholds and count matches at each
    for threshold in np.arange(0.9, 0.5, -0.05):
        count = np.sum(flat >= threshold)
        if count >= min_matches:
            return threshold

    return 0.5  # Fallback
```

## Robust Non-Maximum Suppression (NMS)

### Basic NMS
```python
def nms_simple(matches, min_distance=10):
    """Remove overlapping detections based on distance"""

    if not matches:
        return []

    # Sort by confidence (highest first)
    filtered = []

    for match in matches:
        overlaps = False
        for existing in filtered:
            dist = np.sqrt((match[0] - existing[0])**2 + (match[1] - existing[1])**2)
            if dist < min_distance:
                overlaps = True
                break

        if not overlaps:
            filtered.append(match)

    return filtered
```

### Advanced NMS with Confidence Scores
```python
def nms_with_confidence(frame, template, result, threshold=0.7, min_distance=10):
    """NMS considering match confidence scores"""

    loc = np.where(result >= threshold)

    # Create list of (x, y, confidence)
    matches = [(loc[1][i], loc[0][i], result[loc[0][i], loc[1][i]])
               for i in range(len(loc[0]))]

    # Sort by confidence descending
    matches = sorted(matches, key=lambda x: x[2], reverse=True)

    # Apply NMS
    filtered = []
    for match in matches:
        overlaps = False
        for existing in filtered:
            dist = np.sqrt((match[0] - existing[0])**2 + (match[1] - existing[1])**2)
            if dist < min_distance:
                overlaps = True
                break

        if not overlaps:
            filtered.append(match)

    return len(filtered)
```

## Complete Detection Pipeline

```python
import cv2
import numpy as np

def count_objects_robust(frame_path, template_path,
                         threshold=None,
                         min_distance=10,
                         debug=False):
    """
    Robust object counting with automatic threshold and NMS

    Args:
        frame_path: Path to frame image
        template_path: Path to template image
        threshold: Match threshold (auto if None)
        min_distance: Minimum distance between matches
        debug: Print diagnostic information

    Returns:
        Count of detected objects
    """

    frame = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    if frame is None or template is None:
        return 0

    h, w = template.shape

    # Verify template fits in frame
    if h > frame.shape[0] or w > frame.shape[1]:
        if debug:
            print(f"Template larger than frame!")
        return 0

    # Perform matching
    result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)

    # Determine threshold
    if threshold is None:
        # Use 70th percentile of matches
        threshold = np.percentile(result.flatten(), 70)
        if debug:
            print(f"Auto threshold: {threshold:.3f}")

    # Find matches
    loc = np.where(result >= threshold)
    matches = list(zip(*loc[::-1]))

    if debug:
        print(f"Raw matches: {len(matches)}")

    # Apply NMS
    filtered = nms_simple(matches, min_distance)

    if debug:
        print(f"After NMS: {len(filtered)}")

    return len(filtered)

def nms_simple(matches, min_distance=10):
    """Simple NMS implementation"""

    if not matches:
        return []

    filtered = []
    for match in matches:
        overlaps = False
        for existing in filtered:
            dist = np.sqrt((match[0] - existing[0])**2 + (match[1] - existing[1])**2)
            if dist < min_distance:
                overlaps = True
                break

        if not overlaps:
            filtered.append(match)

    return filtered
```

## Tuning Guide

### If Overcounting (Too Many Detections)
1. Increase threshold: 0.65 → 0.70 → 0.75
2. Increase min_distance: 10 → 15 → 20
3. Verify template quality

### If Undercounting (Too Few Detections)
1. Decrease threshold: 0.70 → 0.65 → 0.60
2. Check template matches video content
3. Verify images are grayscale

### Template Quality Checks
```python
# Verify template is not too small/large
h, w = template.shape
aspect = w / h
print(f"Template size: {w}x{h}, aspect: {aspect:.2f}")

# Check template contrast
print(f"Template brightness range: {template.min()}-{template.max()}")
```

## Debugging Visualizations
```python
def visualize_matches(frame_path, template_path, threshold=0.7):
    """Visualize matches on frame (requires display)"""

    frame = cv2.imread(frame_path)
    template = cv2.imread(template_path)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(frame_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)

    h, w = template_gray.shape

    for pt in zip(*loc[::-1]):
        cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

    cv2.imwrite('/tmp/matches.png', frame)
    print(f"Saved visualization to /tmp/matches.png")
```
