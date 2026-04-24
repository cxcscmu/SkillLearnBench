---
name: run2_ffmpeg-extract
description: Extract key frames (I-frames) from a video file into a sequence of images using FFmpeg.
---
# FFmpeg Keyframe Extraction

Extract key frames (I-frames) from video files using FFmpeg CLI. This is particularly useful for video analysis tasks where you only need representative frames rather than every single frame.

## Prerequisites
- FFmpeg installed and available in PATH
- Input video file (MP4, MKV, AVI, MOV, etc.)

## Methods

### Method 1: Skip Non-Keyframes (Faster)
This method is highly recommended for performance as it skips decoding non-keyframes entirely.

```bash
ffmpeg -skip_frame nokey -i <input_video> -vsync vfr <output_pattern>
```

**Options Explained:**
- `-skip_frame nokey`: Tells the decoder to skip non-keyframes.
- `-i <input_video>`: The source video file.
- `-vsync vfr`: Variable frame rate synchronization, prevents duplicate frames in the output. Note: in newer ffmpeg versions, `-fps_mode vfr` is preferred.
- `<output_pattern>`: The filename pattern for the output, such as `keyframes_%03d.png` which produces `keyframes_001.png`, `keyframes_002.png`, etc.

### Example

```bash
ffmpeg -skip_frame nokey -i video.mp4 -fps_mode vfr keyframes_%03d.png
```
