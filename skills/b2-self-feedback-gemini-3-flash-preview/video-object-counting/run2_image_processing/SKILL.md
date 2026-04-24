---
name: run2_image_processing
description: Efficient inplace image processing using ImageMagick's mogrify.
---

# Efficient Inplace Image Processing

While `convert` is great for single files, `mogrify` is designed for batch processing files in place.

## Grayscale Conversion

To convert all PNG files in the current directory to grayscale inplace:

```bash
mogrify -colorspace Gray *.png
```

## Resizing

To resize all images to 50% inplace:
```bash
mogrify -resize 50% *.png
```

## Why use mogrify?
- It overwrites the original files by default.
- It is more concise for batch operations than a `for` loop with `convert`.
