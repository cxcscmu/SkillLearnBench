---
name: opencv-grayscale
description: Convert images from RGB/BGR to grayscale using OpenCV and save in-place.
---

# OpenCV Grayscale Conversion

## Code

```python
import cv2

img = cv2.imread("input.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("input.png", gray)  # overwrite in-place
```

## Batch conversion
```python
import cv2
import glob

for f in sorted(glob.glob("/root/keyframes_*.png")):
    img = cv2.imread(f)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(f, gray)
```
