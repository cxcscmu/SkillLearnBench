---
name: image-grayscale-conversion
description: Use ImageMagick to convert an image to grayscale inplace.
---

# Image Grayscale Conversion

To convert an image to grayscale using ImageMagick:

```bash
convert input.png -colorspace Gray output.png
```

To convert multiple images in a folder to grayscale inplace:

```bash
mogrify -colorspace Gray folder/*.png
```
