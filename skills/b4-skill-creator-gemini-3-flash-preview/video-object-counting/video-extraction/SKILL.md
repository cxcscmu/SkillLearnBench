---
name: video-extraction
description: Use this skill to extract keyframes from video files using FFmpeg. It covers selecting the right extraction frequency and naming conventions for image sequences.
---

# Video Extraction Skill

This skill provides instructions for extracting keyframes from video files (e.g., MP4) using `ffmpeg`.

## Prerequisites
- `ffmpeg` must be installed in the environment.

## Extraction Commands

To extract keyframes from a video file:

```bash
ffmpeg -i input_video.mp4 -vf "select='eq(pict_type,PICT_TYPE_I)'" -vsync vfr output_prefix_%03d.png
```

- `-i input_video.mp4`: Specifies the input video file.
- `-vf "select='eq(pict_type,PICT_TYPE_I)'"`: Filters for I-frames (keyframes).
- `-vsync vfr`: Variable frame rate, ensures only selected frames are output.
- `output_prefix_%03d.png`: The output filename pattern.

## Naming Convention
For this task, use the following pattern:
`/root/keyframes_%03d.png`

## Verification
After extraction, list the files in the output directory to confirm they were created.
