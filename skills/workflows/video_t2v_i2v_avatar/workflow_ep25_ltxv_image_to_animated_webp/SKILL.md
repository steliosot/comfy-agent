---
name: workflow_ep25_ltxv_image_to_animated_webp
description: >
  Workflow wrapper imported from `Ep25 LTXV Image to Animated WebP.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "library", "video_t2v_i2v_avatar"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "image/png"
metadata.clawdbot.output_type: "application/json"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 60
---

# workflow_ep25_ltxv_image_to_animated_webp

Imported workflow skill generated from `Ep25 LTXV Image to Animated WebP.json`.

## Family

- `video_t2v_i2v_avatar`

## Inputs

- Optional runtime overrides supported by `run(...)`:
  - `prompt`
  - `negative_prompt`
  - `width`, `height`
  - `seed`, `steps`, `cfg`
  - `sampler_name`, `scheduler`, `denoise`
  - `server`, `headers`, `api_prefix`

## Outputs

- Returns JSON with:
  - `status`
  - `prompt_id`
  - `output_images`

## Model Requirements

- `clip`: `t5xxl_fp16.safetensors` -> `models/clip`
- `checkpoint`: `ltx-video-2b-v0.9.safetensors` -> `models/checkpoints`

## Custom Node Requirements

- None detected.

## Links

- https://www.youtube.com/@pixaroma

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `video_t2v_i2v_avatar`
- Input modalities: `image, text_prompt`
- Output modalities: `application/json`
- Model families: `ltx`
- Node count: `14`
- Complexity score: `6`
- Resource profile: `high`
- Estimated runtime: `slow (often 2-6 min depending on model/server load)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `None`

## Detected Models

- `clip`: `t5xxl_fp16.safetensors` -> `models/clip`
- `checkpoint`: `ltx-video-2b-v0.9.safetensors` -> `models/checkpoints`

## Detected Custom Nodes

- None detected.

## Runtime Warnings

- Large model(s) detected; ensure enough VRAM and disk space.
- Video workflow: usually slower and VRAM-intensive than still-image workflows.
<!-- AUTO-METADATA-END -->

