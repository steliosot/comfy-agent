---
name: curated_qwenvl_video_to_text
description: >
  Curated ComfyUI workflow imported from `QwenVL Video to Text.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "curated", "video_t2v_i2v_avatar"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "video/mp4"
metadata.clawdbot.output_type: "application/json"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 70
---

# curated_qwenvl_video_to_text

Curated workflow skill generated from `QwenVL Video to Text.json`.

## Capability Family

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
  - `output_images` (includes image/video entries reported by Comfy history)

## Model Requirements

- None detected from loader nodes.

## Custom Node Requirements

- `comfyui-qwenvl`
- `comfyui-videohelpersuite`

## Links Extracted From Workflow Notes

- https://discord.com/invite/gggpkVgBf3
- https://github.com/1038lab/ComfyUI-QwenVL
- https://www.youtube.com/@pixaroma

## Source

- Original: `comfy-data/workflows/QwenVL Video to Text.json`

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `video_t2v_i2v_avatar`
- Input modalities: `video`
- Output modalities: `application/json`
- Model families: `qwen, wan`
- Node count: `5`
- Complexity score: `5`
- Resource profile: `medium`
- Estimated runtime: `moderate (about 30-120s depending on server)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `None`

## Detected Models

- None detected.

## Detected Custom Nodes

- `comfyui-qwenvl`
- `comfyui-videohelpersuite`

## Runtime Warnings

- Uses custom nodes; missing nodes can cause validation/runtime failures.
- Video workflow: usually slower and VRAM-intensive than still-image workflows.
<!-- AUTO-METADATA-END -->

