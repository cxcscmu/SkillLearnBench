---
name: video-frame-extraction
description: Use this skill to extract key frames from MP4 video files into a target directory.
---

# Video Frame Extraction

Use FFmpeg to extract key frames from video files.

## Usage
Run the following command in the terminal to extract frames:
`ffmpeg -i <input_video.mp4> -vf "select='eq(pict_type,PICT_TYPE_I)'" -vsync vfr /root/keyframes_%03d.png`

## Parameters
- `<input_video.mp4>`: Path to the input video file.
- `/root/keyframes_%03d.png`: Target file pattern for extracted frames.
