---
name: run2_image-processing
description: Performs image format conversion and color space modification using ImageMagick tools.
---

## Overview
This skill covers efficient image manipulation, specifically converting files to grayscale for easier processing.

## Usage
To convert image(s) to grayscale in-place:

```bash
mogrify -colorspace Gray <image_pattern>
```

- `mogrify`: ImageMagick tool for batch in-place processing.
- `-colorspace Gray`: Changes the color space to grayscale.
