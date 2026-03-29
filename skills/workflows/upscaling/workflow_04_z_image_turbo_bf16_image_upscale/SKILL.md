---
name: workflow_04_z_image_turbo_bf16_image_upscale
description: >
  Workflow wrapper imported from `04-Z Image Turbo bf16 Image Upscale.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "library", "upscaling"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "image/png"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 60
---

# workflow_04_z_image_turbo_bf16_image_upscale

Imported workflow skill generated from `04-Z Image Turbo bf16 Image Upscale.json`.

## Family

- `upscaling`

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

- `diffusion_model`: `z_image_turbo_bf16.safetensors` -> `models/diffusion_models`
- `clip`: `qwen_3_4b.safetensors` -> `models/clip`
- `vae`: `ae.safetensors` -> `models/vae`
- `upscale_model`: `4xNomos2_hq_dat2.safetensors` -> `models/upscale_models`

## Custom Node Requirements

- `rgthree-comfy`

## Links

- https://discord.com/invite/gggpkVgBf3
- https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/diffusion_models/z_image_turbo_bf16.safetensors
- https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/text_encoders/qwen_3_4b.safetensors
- https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/vae/ae.safetensors
- https://huggingface.co/Phips/4xNomos2_hq_dat2
- https://huggingface.co/Phips/4xNomos2_hq_dat2/resolve/main/4xNomos2_hq_dat2.safetensors?download=true
- https://www.youtube.com/@pixaroma

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `upscaling`
- Input modalities: `image, text_prompt`
- Output modalities: `image/png`
- Model families: `flux, qwen, z_image_turbo`
- Node count: `19`
- Complexity score: `1`
- Resource profile: `low`
- Estimated runtime: `fast (usually under 30s on modern GPU)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `5`

## Detected Models

- `diffusion_model`: `z_image_turbo_bf16.safetensors` -> `models/diffusion_models`
- `clip`: `qwen_3_4b.safetensors` -> `models/clip`
- `vae`: `ae.safetensors` -> `models/vae`
- `upscale_model`: `4xNomos2_hq_dat2.safetensors` -> `models/upscale_models`

## Detected Custom Nodes

- `rgthree-comfy`

## Runtime Warnings

- Uses custom nodes; missing nodes can cause validation/runtime failures.
<!-- AUTO-METADATA-END -->

