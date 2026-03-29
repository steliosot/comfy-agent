---
name: download_video
description: >
  Download generated video outputs from ComfyUI history to local storage.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "skill", "download", "transport", "video"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "application/json"
metadata.clawdbot.output_type: "video-file"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 80
---

# download_video

Download generated video outputs from ComfyUI history to local storage.

## Usage

```bash
python3 skills/infra/download_video/scripts/run.py --args '{"prompt_id":"<id>","run_id":"demo"}' --pretty
```
