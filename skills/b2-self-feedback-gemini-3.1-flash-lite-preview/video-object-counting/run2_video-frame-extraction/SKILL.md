---
name: run2_video-frame-extraction
description: Extracts all key frames from a video file into a specified output directory using FFmpeg.
---

## Overview
This skill extracts keyframes (I-frames) from video files into individual PNG files. This is useful for object detection over time.

## Usage
To extract keyframes as PNG files, use the following command:

```bash
ffmpeg -i <input_file> -vf "select='eq(pict_type,PICT_TYPE_I)'" -fps_mode vfr -vsync vfr /root/keyframes_%03d.png
```

- `-i`: Input video file.
- `-vf "select='eq(pict_type,PICT_TYPE_I)'"`: Select only I-frames.
- `-fps_mode vfr`: Specifies variable frame rate mode for keyframes.
- `-vsync vfr`: Maintains synchronization by setting variable frame rate.
- `/root/keyframes_%03d.png`: Output filename pattern.
