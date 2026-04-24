---
name: run2_opencv-grayscale
description: Convert images to grayscale in-place using OpenCV, including both keyframes and template images.
---

# OpenCV Grayscale Conversion

## Convert All Images In-Place

Both keyframes AND template images must be converted to grayscale before template matching.

```python
import cv2
import glob

# Convert keyframes
for path in sorted(glob.glob('/root/keyframes_*.png')):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(path, gray)

# Convert templates
for path in ['/root/coin.png', '/root/enemy.png', '/root/turtle.png']:
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(path, gray)
```

## Important

- The `count_objects.py` script reads with `IMREAD_GRAYSCALE`, so files must be grayscale before counting
- Overwriting originals is required per the task specification
- Grayscale images are single-channel (H x W) vs RGB (H x W x 3)
