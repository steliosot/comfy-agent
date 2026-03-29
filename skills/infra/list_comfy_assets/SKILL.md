---
name: list_comfy_assets
description: >
  List available ComfyUI assets (checkpoints, vae, clip, lora, unet) and local input/output image files.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "skill", "lora", "asset-discovery"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "none"
metadata.clawdbot.output_type: "application/json"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 80
---

# list_comfy_assets

List available ComfyUI assets (checkpoints, vae, clip, lora, unet) and local input/output image files.

## Usage

```bash
python3 skills/infra/list_comfy_assets/scripts/run.py --args '{}' --pretty
```

Pass JSON kwargs for `run(...)` via `--args`:

```bash
python3 skills/infra/list_comfy_assets/scripts/run.py --args '{"param":"value"}' --pretty
```

## Inputs / Outputs

- Inputs follow `skills/infra/list_comfy_assets/skill.yaml`.
- Output is JSON printed to stdout from `run(...)`.

## Composition

This skill is designed to compose with other single-purpose skills.
Use `run_id` and artifact references when chaining.
