---
name: video-keyframe-extraction
description: Use this skill to extract keyframes (I-frames) from an MP4 video file using ffmpeg. This produces numbered PNG files in a specified output directory.
---

## How to extract keyframes from a video

Use `ffmpeg` to extract only I-frames (keyframes) from the video:

```bash
ffmpeg -i /root/super-mario.mp4 -vf "select=eq(pict_type\,I)" -vsync vfp /root/keyframes_%03d.png -y
```

This will produce files like `/root/keyframes_001.png`, `/root/keyframes_002.png`, etc.

### Verifying extraction

After extraction, list the files to confirm how many keyframes were produced:

```bash
ls -1 /root/keyframes_*.png | sort
```

Count them:

```bash
ls -1 /root/keyframes_*.png | wc -l
```

### Important notes

- The output format `keyframes_%03d.png` is zero-padded to 3 digits, starting from 001.
- ffmpeg numbers sequentially starting at 1.
- All keyframes are in timeline order by default.
- If the number of keyframes seems wrong, you can also try extracting at a fixed interval (e.g., 1 fps) using `-vf fps=1` instead, but I-frame extraction is the standard approach for "key frames."
- Use `ffprobe` to check total number of I-frames beforehand if needed:

```bash
ffprobe -select_streams v -show_frames -show_entries frame=pict_type /root/super-mario.mp4 2>/dev/null | grep "pict_type=I" | wc -l
```