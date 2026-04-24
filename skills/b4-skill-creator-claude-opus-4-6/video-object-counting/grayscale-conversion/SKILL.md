---
name: grayscale-conversion
description: Convert RGB images to grayscale using OpenCV (cv2) in Python. Use this skill when the user needs to convert color images to grayscale for image processing, template matching, or analysis.
---

# Grayscale Image Conversion

Convert RGB/BGR images to grayscale using OpenCV.

## Python Code

```python
import cv2

img = cv2.imread("input.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("input.png", gray)  # overwrite in-place
```

## Batch Conversion

```python
import cv2
import glob

for path in sorted(glob.glob("/root/keyframes_*.png")):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(path, gray)
```

## Notes

- OpenCV reads images in BGR format, so use `COLOR_BGR2GRAY`
- Writing a grayscale image back with `cv2.imwrite` produces a single-channel PNG
- Grayscale conversion is often a prerequisite for template matching with `cv2.matchTemplate`
