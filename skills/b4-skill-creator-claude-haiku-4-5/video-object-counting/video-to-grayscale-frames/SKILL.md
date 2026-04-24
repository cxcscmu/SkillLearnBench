---
name: video-to-grayscale-frames
description: Extract keyframes from MP4 video files and convert them to grayscale. Use this skill when you need to process video files for analysis by extracting I-frames (keyframes) and converting them to grayscale images for computer vision tasks.
---

# Video to Grayscale Frames

This skill guides you through extracting keyframes from MP4 video files and converting them to grayscale images for analysis.

## Overview

The workflow has two main steps:
1. **Extract keyframes** from the MP4 video using FFmpeg
2. **Convert to grayscale** and save frames as PNG files

## Step 1: Extract Keyframes from MP4

Use the `ffmpeg` skill to extract I-frames (keyframes) from the video.

### Command Structure
```bash
ffmpeg -i <input.mp4> -vf "select=eq(pict_type\,I)" -vsync vfr <output_pattern>
```

### Parameters
- `input.mp4`: Path to your video file
- `output_pattern`: Output file pattern (e.g., `/root/keyframes_%03d.png`)
  - `%03d` creates zero-padded numbers: keyframes_001.png, keyframes_002.png, etc.

### Example
For a video at `/root/super-mario.mp4`, extracting to `/root/keyframes_%03d.png`:
```bash
ffmpeg -i /root/super-mario.mp4 -vf "select=eq(pict_type\,I)" -vsync vfr /root/keyframes_%03d.png
```

This creates: keyframes_001.png, keyframes_002.png, keyframes_003.png, etc.

## Step 2: Convert Extracted Frames to Grayscale

Use the `image_editing` skill to convert each extracted keyframe to grayscale IN-PLACE (overwriting the original RGB image).

### Conversion Process
For each keyframe image:
- Input: `/root/keyframes_001.png` (RGB)
- Operation: Convert to grayscale
- Output: `/root/keyframes_001.png` (grayscale, overwrites original)

### Batch Processing
When converting multiple frames, process them sequentially or in parallel depending on available resources. Ensure each frame is converted and saved before proceeding to analysis.

## Output Format

After this skill completes:
- Keyframes are stored as `/root/keyframes_001.png`, `/root/keyframes_002.png`, etc.
- All files are in grayscale format
- Files are ready for object detection and counting

## Common Issues

- **FFmpeg not installed**: The ffmpeg skill should handle installation
- **No keyframes extracted**: Video may have no I-frames; consider extracting all frames with `-fps 1` instead
- **Image format errors**: Ensure images are valid PNG files before grayscale conversion
