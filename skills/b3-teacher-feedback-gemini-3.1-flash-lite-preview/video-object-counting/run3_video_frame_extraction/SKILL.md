---
name: video_frame_extraction
description: Use ffmpeg to extract keyframes from a video file into a target directory.
---
To extract keyframes from `/root/super-mario.mp4` and save them as PNG files in the `/root/` directory, use the following FFmpeg command:

```bash
ffmpeg -i /root/super-mario.mp4 -vf "select='eq(pict_type,I)'" -vsync vfr /root/keyframes_%03d.png
```

This command extracts only the I-frames (key frames) and saves them with the required naming convention (`/root/keyframes_%03d.png`).