---
name: curated_05_z_image_turbo_txt2img_bf16_lora_style
description: >
  Curated ComfyUI workflow imported from `05-Z Image Turbo txt2img bf16 + Lora style.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "curated", "editing_restyle"]
metadata.clawdbot.category: "media-editing"
metadata.clawdbot.input_type: "text"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 70
---

# curated_05_z_image_turbo_txt2img_bf16_lora_style

Curated workflow skill generated from `05-Z Image Turbo txt2img bf16 + Lora style.json`.

## Capability Family

- `editing_restyle`

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

- `clip`: `qwen_3_4b.safetensors` -> `models/clip`
- `vae`: `ae.safetensors` -> `models/vae`
- `diffusion_model`: `z_image_turbo_bf16.safetensors` -> `models/diffusion_models`
- `lora`: `pixaf4nt4sy fantasy style game item.safetensors` -> `models/loras`

## Custom Node Requirements

- None detected.

## Links Extracted From Workflow Notes

- https://discord.com/invite/gggpkVgBf3
- https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/diffusion_models/z_image_turbo_bf16.safetensors
- https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/text_encoders/qwen_3_4b.safetensors
- https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/vae/ae.safetensors
- https://huggingface.co/Pixaroma/experimental_loras/resolve/main/pixaf4nt4sy%20fantasy%20style%20game%20item.safetensors?download=true
- https://www.youtube.com/@pixaroma

## Source

- Original: `comfy-data/workflows/05-Z Image Turbo txt2img bf16 + Lora style.json`

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `editing_restyle`
- Input modalities: `text_prompt`
- Output modalities: `image/png`
- Model families: `qwen, sd3, z_image_turbo`
- Node count: `14`
- Complexity score: `2`
- Resource profile: `low`
- Estimated runtime: `fast (usually under 30s on modern GPU)`
- Max latent resolution hint: `1024`x`1024`
- Max sampler steps hint: `5`

## Detected Models

- `clip`: `qwen_3_4b.safetensors` -> `models/clip`
- `vae`: `ae.safetensors` -> `models/vae`
- `diffusion_model`: `z_image_turbo_bf16.safetensors` -> `models/diffusion_models`
- `lora`: `pixaf4nt4sy fantasy style game item.safetensors` -> `models/loras`

## Detected Custom Nodes

- None detected.

## Runtime Warnings

- Medium-high resolution detected; expect moderate extra runtime.
<!-- AUTO-METADATA-END -->

