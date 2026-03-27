---
name: download_image
description: >
  Download ComfyUI image outputs to local files using deterministic names.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "skill", "download", "transport"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "application/json"
metadata.clawdbot.output_type: "image-file"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 80
---

# download_image

Download ComfyUI image outputs to local files using deterministic names.

## Usage

```bash
python3 skills/download_image/scripts/run.py --args '{}' --pretty
```

Pass JSON kwargs for `run(...)` via `--args`:

```bash
python3 skills/download_image/scripts/run.py --args '{"param":"value"}' --pretty
```

## Inputs / Outputs

- Inputs follow `skills/download_image/skill.yaml`.
- Output is JSON printed to stdout from `run(...)`.

## Composition

This skill is designed to compose with other single-purpose skills.
Use `run_id` and artifact references when chaining.
