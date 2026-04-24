---
name: run2_image-grayscale
description: Convert PNG images to grayscale inplace using ImageMagick; covers both keyframes and template images for consistent matching.
---

# Convert Images to Grayscale (Inplace)

## Prerequisites
- ImageMagick: `sudo apt install imagemagick`

## Convert Single Image Inplace
```bash
convert image.png -colorspace Gray image.png
```

## Batch Convert Keyframes Inplace
```bash
for f in /root/keyframes_*.png; do
    convert "$f" -colorspace Gray "$f"
done
```

## Convert Template Images to Grayscale (Important!)
When keyframes are converted to grayscale, template images used for matching should ALSO be converted to grayscale for consistent comparison:
```bash
for f in /root/coin.png /root/enemy.png /root/turtle.png; do
    convert "$f" -colorspace Gray "$f"
done
```

## Notes
- `-colorspace Gray` converts to grayscale while keeping PNG format and file extension
- Overwriting the input path makes the operation inplace
- Template images must match the colorspace of the frames they are compared against
- Works for PNG, JPG, BMP, and other formats
