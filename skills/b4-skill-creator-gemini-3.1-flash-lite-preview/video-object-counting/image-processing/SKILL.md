---
name: image-processing
description: Use this skill for image conversion, such as grayscale conversion, to prepare images for analysis.
---

# Image Processing

Use this skill to convert images to grayscale.

## Conversion
To convert an image to grayscale using ImageMagick:
`convert <input_image.png> -colorspace Gray <output_image.png>`
To overwrite the original:
`convert <file.png> -colorspace Gray <file.png>`
