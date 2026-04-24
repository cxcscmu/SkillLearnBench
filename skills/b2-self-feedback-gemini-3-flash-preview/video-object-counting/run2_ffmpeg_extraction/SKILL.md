---
name: run2_ffmpeg_extraction
description: Advanced FFmpeg techniques for keyframe extraction with quality control.
---

# Advanced FFmpeg Keyframe Extraction

Extract only the keyframes (I-frames) from a video. This is much faster than extracting every frame and provides the most significant images.

## Basic Usage

```bash
ffmpeg -i input.mp4 -vf "select='eq(pict_type,I)'" -vsync vfr output_%03d.png
```

## Quality Control

If you need high quality JPEGs instead of PNGs:
```bash
ffmpeg -i input.mp4 -vf "select='eq(pict_type,I)'" -vsync vfr -q:v 2 output_%03d.jpg
```
(where `-q:v 2` is high quality, range 1-31).

## Parameters Explained

- `-vf "select='eq(pict_type,I)'"`: Filters for Intra-coded frames (keyframes).
- `-vsync vfr`: Variable Frame Rate, ensures we don't get duplicate frames if keyframe intervals vary.
- `output_%03d.png`: Standard printf-style naming for sequences.
