---
name: run2_imagemagick-grayscale
description: Convert a batch of images to grayscale in-place using ImageMagick's mogrify command.
---
# ImageMagick Grayscale Conversion

Use ImageMagick to edit images in batch on the Linux command-line.

## Usage

To convert images to grayscale in-place, the `mogrify` command is the most efficient choice as it overwrites the original files, avoiding the need to manage new filenames.

```bash
mogrify -colorspace Gray <image_files>
```

**Options Explained:**
- `mogrify`: The ImageMagick tool for in-place batch image manipulation.
- `-colorspace Gray`: Changes the colorspace of the image to grayscale, discarding RGB color information.

### Example

Convert all PNG files in the current directory to grayscale in-place:
```bash
mogrify -colorspace Gray *.png
```

Alternatively, if you want to create new files without modifying the originals, use `convert`:
```bash
convert input.png -colorspace Gray output.png
```
