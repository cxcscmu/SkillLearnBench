---
name: extract-video-keyframes
description: Extract key frames from an MP4 video file and save them as PNG images in a target directory. Use this skill when you need to convert a video into individual frame images for further analysis.
---

## Extract Video Keyframes

Use `ffmpeg` to extract key frames from the video and save them as sequentially numbered PNG files.

```bash
ffmpeg -i /root/super-mario.mp4 -vf "select=eq(pict_type\,I)" -vsync vfr /root/keyframes_%03d.png
```

This extracts only I-frames (keyframes) from the video and saves them as `/root/keyframes_001.png`, `/root/keyframes_002.png`, etc., in timeline order.

After extraction, verify the files exist:
```bash
ls /root/keyframes_*.png | sort
```