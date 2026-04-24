---
name: image_preprocessing
description: Convert images to grayscale in-place using OpenCV.
---
To convert an image to grayscale and overwrite the original file, use a Python script with OpenCV:

```python
import cv2
import glob

files = sorted(glob.glob('/root/keyframes_*.png'))
for file_path in files:
    img = cv2.imread(file_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(file_path, gray)
```