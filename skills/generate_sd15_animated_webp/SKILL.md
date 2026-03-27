---
name: generate_sd15_animated_webp
description: >
  Generate a simple animated WEBP from an SD1.5 image batch.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "skill", "image-generation"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "text"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 80
---

# generate_sd15_animated_webp

Generate a simple animated WEBP from an SD1.5 image batch.

## Usage

```bash
python3 skills/generate_sd15_animated_webp/scripts/run.py --args '{}' --pretty
```

Pass JSON kwargs for `run(...)` via `--args`:

```bash
python3 skills/generate_sd15_animated_webp/scripts/run.py --args '{"param":"value"}' --pretty
```

## Inputs / Outputs

- Inputs follow `skills/generate_sd15_animated_webp/skill.yaml`.
- Output is JSON printed to stdout from `run(...)`.

## Composition

This skill is designed to compose with other single-purpose skills.
Use `run_id` and artifact references when chaining.
