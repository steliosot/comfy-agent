---
name: workflow_02_z_image_turbo_txt2img_bf16_1920x1080px_fullhd
description: >
  Workflow wrapper imported from `02-Z Image Turbo txt2img bf16 1920x1080px FullHD.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "library", "txt2img"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "text"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 60
---

# workflow_02_z_image_turbo_txt2img_bf16_1920x1080px_fullhd

Imported workflow skill generated from `02-Z Image Turbo txt2img bf16 1920x1080px FullHD.json`.

## Family

- `txt2img`

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

- `clip`: `qwen_3_4b.safetensors` -> `models/clip`
- `vae`: `ae.safetensors` -> `models/vae`
- `diffusion_model`: `z_image_turbo_bf16.safetensors` -> `models/diffusion_models`

## Custom Node Requirements

- None detected.

## Links

- https://discord.com/invite/gggpkVgBf3
- https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/diffusion_models/z_image_turbo_bf16.safetensors
- https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/text_encoders/qwen_3_4b.safetensors
- https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/vae/ae.safetensors
- https://www.youtube.com/@pixaroma

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `txt2img`
- Input modalities: `text_prompt`
- Output modalities: `image/png`
- Model families: `qwen, sd3, z_image_turbo`
- Node count: `13`
- Complexity score: `3`
- Resource profile: `medium`
- Estimated runtime: `moderate (about 30-120s depending on server)`
- Max latent resolution hint: `1920`x`1088`
- Max sampler steps hint: `5`

## Detected Models

- `clip`: `qwen_3_4b.safetensors` -> `models/clip`
- `vae`: `ae.safetensors` -> `models/vae`
- `diffusion_model`: `z_image_turbo_bf16.safetensors` -> `models/diffusion_models`

## Detected Custom Nodes

- None detected.

## Runtime Warnings

- High output resolution detected; generation time/memory use can increase significantly.
<!-- AUTO-METADATA-END -->

