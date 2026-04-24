---
name: ffmpeg-keyframes
description: Extract key frames (I-frames) from video files using FFmpeg for analysis and processing.
---

# FFmpeg Key Frame Extraction

## Overview
Extract I-frames (keyframes) from video files. Keyframes are complete frames that don't depend on other frames for decoding.

## Command

```bash
ffmpeg -i input.mp4 -vf "select=eq(pict_type\,I)" -vsync vfr output_%03d.png
```

### Flags
- `-vf "select=eq(pict_type\,I)"`: Select only I-frames (key frames)
- `-vsync vfr`: Variable frame rate to avoid duplicate frames
- `%03d`: Zero-padded 3-digit numbering

## Output
Produces files like `output_001.png`, `output_002.png`, etc. in timeline order.

## Verify
```bash
ffprobe -i input.mp4 -select_streams v -show_frames -show_entries frame=pict_type | grep -c "pict_type=I"
```
