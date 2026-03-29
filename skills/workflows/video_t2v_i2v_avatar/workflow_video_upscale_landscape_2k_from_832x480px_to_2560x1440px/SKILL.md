---
name: workflow_video_upscale_landscape_2k_from_832x480px_to_2560x1440px
description: >
  Workflow wrapper imported from `Video Upscale Landscape 2K from 832x480px to 2560x1440px.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "library", "video_t2v_i2v_avatar"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "video/mp4"
metadata.clawdbot.output_type: "video/mp4"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 60
---

# workflow_video_upscale_landscape_2k_from_832x480px_to_2560x1440px

Imported workflow skill generated from `Video Upscale Landscape 2K from 832x480px to 2560x1440px.json`.

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

- `upscale_model`: `4x_NMKD-Siax_200k.pth` -> `models/upscale_models`

## Custom Node Requirements

- `comfyui-easy-use`
- `comfyui-videohelpersuite`

## Links

- https://discord.com/invite/gggpkVgBf3
- https://huggingface.co/Akumetsu971/SD_Anime_Futuristic_Armor/resolve/main/4x_NMKD-Siax_200k.pth?download=true
- https://www.youtube.com/@pixaroma

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `video_t2v_i2v_avatar`
- Input modalities: `video`
- Output modalities: `video/mp4`
- Model families: `wan`
- Node count: `13`
- Complexity score: `5`
- Resource profile: `medium`
- Estimated runtime: `moderate (about 30-120s depending on server)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `None`

## Detected Models

- `upscale_model`: `4x_NMKD-Siax_200k.pth` -> `models/upscale_models`

## Detected Custom Nodes

- `comfyui-easy-use`
- `comfyui-videohelpersuite`

## Runtime Warnings

- Uses custom nodes; missing nodes can cause validation/runtime failures.
- Video workflow: usually slower and VRAM-intensive than still-image workflows.
<!-- AUTO-METADATA-END -->

