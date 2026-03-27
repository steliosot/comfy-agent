---
name: generate_flux_multi_input_img2img
description: >
  Generate one image from 2 or 3 already-uploaded Comfy input images using a FLUX multi-reference img2img pipeline.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "skill", "upload", "transport", "image-generation"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "image-file"
metadata.clawdbot.output_type: "application/json"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 80
---

# generate_flux_multi_input_img2img

Generate one image from 2 or 3 already-uploaded Comfy input images using a FLUX multi-reference img2img pipeline.

## Usage

```bash
python3 skills/generate_flux_multi_input_img2img/scripts/run.py --args '{}' --pretty
```

Pass JSON kwargs for `run(...)` via `--args`:

```bash
python3 skills/generate_flux_multi_input_img2img/scripts/run.py --args '{"param":"value"}' --pretty
```

## Inputs / Outputs

- Inputs follow `skills/generate_flux_multi_input_img2img/skill.yaml`.
- Output is JSON printed to stdout from `run(...)`.

## Composition

This skill is designed to compose with other single-purpose skills.
Use `run_id` and artifact references when chaining.
