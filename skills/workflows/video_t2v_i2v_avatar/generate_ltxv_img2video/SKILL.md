---
name: generate_ltxv_img2video
description: >
  Generate an LTXV image-to-video clip from a pre-uploaded Comfy input image.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "skill", "upload", "transport", "video-generation"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "image-file"
metadata.clawdbot.output_type: "application/json"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 80
---

# generate_ltxv_img2video

Generate an LTXV image-to-video clip from a pre-uploaded Comfy input image.

## Usage

```bash
python3 skills/workflows/generate_ltxv_img2video/scripts/run.py --args '{}' --pretty
```

Pass JSON kwargs for `run(...)` via `--args`:

```bash
python3 skills/workflows/generate_ltxv_img2video/scripts/run.py --args '{"param":"value"}' --pretty
```

## Inputs / Outputs

- Inputs follow `skills/workflows/generate_ltxv_img2video/skill.yaml`.
- Output is JSON printed to stdout from `run(...)`.

## Composition

This skill is designed to compose with other single-purpose skills.
Use `run_id` and artifact references when chaining.

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `video_t2v_i2v_avatar`
- Input modalities: `text_prompt`
- Output modalities: `application/json`
- Model families: `other`
- Node count: `None`
- Complexity score: `None`
- Resource profile: `unknown`
- Estimated runtime: `depends on runtime parameters and server resources`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `None`

## Detected Models

- None detected.

## Detected Custom Nodes

- None detected.

## Runtime Warnings

- Hand-authored skill (no embedded workflow.json); metadata is inferred and may be approximate.
<!-- AUTO-METADATA-END -->
