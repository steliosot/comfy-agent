---
name: generate_video_clip
description: >
  Generate a WAN 2.1 video clip using EmptyHunyuanLatentVideo and VHS_VideoCombine (video/h264-mp4).
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "skill", "video-generation"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "text+image-ref"
metadata.clawdbot.output_type: "video/mp4"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 80
---

# generate_video_clip

Generate a WAN 2.1 video clip using EmptyHunyuanLatentVideo and VHS_VideoCombine (video/h264-mp4).

## Usage

```bash
python3 skills/generate_video_clip/scripts/run.py --args '{}' --pretty
```

Pass JSON kwargs for `run(...)` via `--args`:

```bash
python3 skills/generate_video_clip/scripts/run.py --args '{"param":"value"}' --pretty
```

## Inputs / Outputs

- Inputs follow `skills/generate_video_clip/skill.yaml`.
- Output is JSON printed to stdout from `run(...)`.

## Composition

This skill is designed to compose with other single-purpose skills.
Use `run_id` and artifact references when chaining.
