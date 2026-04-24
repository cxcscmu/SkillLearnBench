---
name: video-keyframe-extraction
description: Extract key frames (I-frames) from video files using FFmpeg.
---

# Video Keyframe Extraction

Use ffmpeg to extract key frames (I-frames) to save them as PNG files.

```bash
ffmpeg -i input.mp4 -vf "select='eq(pict_type,PICT_TYPE_I)'" -vsync vfr "output_%03d.png"
```
