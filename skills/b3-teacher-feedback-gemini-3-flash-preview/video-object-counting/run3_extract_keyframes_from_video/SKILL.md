---
name: extract_keyframes_from_video
description: Converts a video file into a series of keyframe images using FFmpeg with specific frame selection filters.
---

To extract high-quality keyframes from the video, use FFmpeg with the I-frame selection filter. This ensures only the primary frames are captured for analysis.

Command:
```bash
ffmpeg -i /root/super-mario.mp4 -vf "select='eq(pict_type\,I)'" -vsync vfr /root/keyframes_%03d.png
```

Parameters:
- `-vf "select='eq(pict_type\,I)'"`: Filters the video to select only Intra-coded frames (keyframes).
- `-vsync vfr`: Ensures variable frame rate is handled correctly so no frames are duplicated or dropped.
- `/root/keyframes_%03d.png`: The output pattern to save frames in chronological order (e.g., keyframes_001.png, keyframes_002.png).