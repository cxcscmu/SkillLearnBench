---
name: video-processing
description: Tools and techniques for extracting keyframes and processing video files using FFmpeg.
---

# Video Processing with FFmpeg

FFmpeg is a powerful tool for video manipulation. For this task, we focus on extracting keyframes.

## Extraction of Keyframes

To extract keyframes from a video file, use the following command:

```bash
ffmpeg -i input_video.mp4 -vf "select='eq(pict_type,I)'" -vsync vfr output_prefix_%03d.png
```

### Parameters:
- `-i`: Input file path.
- `-vf "select='eq(pict_type,I)'"`: Filter to select only I-frames (keyframes).
- `-vsync vfr`: Variable frame rate to ensure output frames are not duplicated.
- `output_prefix_%03d.png`: Output pattern for extracted images.

## Performance Tips
- Use `-q:v 2` to maintain high quality if needed.
- Ensure the output directory exists before running the command.
