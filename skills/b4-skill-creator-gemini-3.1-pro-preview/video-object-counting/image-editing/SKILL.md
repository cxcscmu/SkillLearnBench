---
name: image-editing
description: Command-line tools for modifying and manipulating images, such as resizing, blurring, or changing colorspace. Use this skill whenever the user mentions modifying images, converting to grayscale, or changing image properties.
---

# Image Editing using ImageMagick

Use the `convert` command to modify images.

## Useful image operations

- **Convert to Grayscale**: Use `-colorspace Gray`.
  Example to edit in-place:
  ```bash
  convert input.png -colorspace Gray input.png
  ```

- **Resize**: `-resize 50%` or `-resize 256x256`

- **Format conversion**: `convert -format jpg *.png`

## Dependencies
- convert: Run `sudo apt install imagemagick` to install. After that, you can use `convert` command.
