---
name: ffmpeg-extraction
description: Extract key frames (I-frames) from video files using FFmpeg CLI. Use this skill whenever you need to pull out keyframes, thumbnails, or important frames from MP4, MKV, AVI, or other video formats for analysis, previews, or processing.
---

# FFmpeg Keyframe Extraction

Extract key frames (I-frames) from video files using FFmpeg CLI.

## Methods

### Extract I-frames

```bash
ffmpeg -i <input_video> -vf "select='eq(pict_type,I)'" -vsync vfr <output_pattern>
```

Example output pattern: `keyframes_%03d.png` for a 3-digit padded sequence.
