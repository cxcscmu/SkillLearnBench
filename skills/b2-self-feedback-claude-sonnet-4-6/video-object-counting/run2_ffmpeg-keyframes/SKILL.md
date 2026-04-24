---
name: run2_ffmpeg-keyframes
description: Extract I-frame keyframes from video files using FFmpeg CLI, saving as zero-padded PNG sequences starting at 001.
---

# FFmpeg Keyframe Extraction

## Prerequisites
- FFmpeg installed: `sudo apt install ffmpeg`

## Extract Keyframes (I-frames) as PNG Sequence
```bash
ffmpeg -i <input_video> -vf "select='eq(pict_type,I)'" -vsync vfr <output_dir>/keyframes_%03d.png
```

### Example
```bash
ffmpeg -i /root/super-mario.mp4 -vf "select='eq(pict_type,I)'" -vsync vfr /root/keyframes_%03d.png
```

## Output
- Files named: `keyframes_001.png`, `keyframes_002.png`, ..., up to total keyframe count
- Files are in RGB color (PNG format, 3-channel)
- Frame index starts at 001
- Timeline order is preserved (sorted by video timestamp)

## Key Flags
- `-vf "select='eq(pict_type,I)'"` — selects only I-frames (keyframes)
- `-vsync vfr` — avoids duplicate frame output

## Notes
- The number of keyframes depends on the video's encoding (GOP size)
- PNG output is lossless and RGB by default
- To list extracted files in order: `ls /root/keyframes_*.png | sort`
