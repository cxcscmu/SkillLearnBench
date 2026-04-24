---
name: video-keyframe-extraction
description: Extract key frames (I-frames) from video files using FFmpeg. Use this skill when the user needs to pull out keyframes from MP4, MKV, AVI, or other video formats for analysis or processing.
---

# Video Keyframe Extraction

Extract I-frames (keyframes) from video files using FFmpeg's `select` filter.

## Command

```bash
ffmpeg -i <input_video> -vf "select=eq(pict_type\,I)" -vsync vfr <output_pattern>
```

- `-vf "select=eq(pict_type\,I)"` selects only I-frames (intra-coded frames, the "key" frames in video compression)
- `-vsync vfr` uses variable frame rate to avoid duplicating frames
- Output pattern uses `%03d` for sequential numbering: e.g., `keyframes_%03d.png`

## Example

```bash
ffmpeg -i /root/video.mp4 -vf "select=eq(pict_type\,I)" -vsync vfr /root/keyframes_%03d.png
```

This produces `/root/keyframes_001.png`, `/root/keyframes_002.png`, etc., one per I-frame in timeline order.

## Notes

- I-frames are complete images (not predicted from other frames), making them ideal for analysis
- The number of keyframes depends on the video's encoding settings (typically every 1-2 seconds)
- Output is in timeline order by default
