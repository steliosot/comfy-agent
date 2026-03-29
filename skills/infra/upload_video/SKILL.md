---
name: upload_video
description: >
  Upload a local video file to ComfyUI input storage with deterministic naming.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "skill", "upload", "transport", "video"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "video-file"
metadata.clawdbot.output_type: "application/json"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 80
---

# upload_video

Upload a local video file to ComfyUI input storage with deterministic naming.

## Usage

```bash
python3 skills/infra/upload_video/scripts/run.py --args '{"video_path":"tmp/outputs/demo.mp4"}' --pretty
```
