---
name: workflow_z_image_turbo_txt2img_bf16_cn_canny
description: >
  Workflow wrapper imported from `Z Image Turbo txt2img bf16 CN Canny.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "library", "txt2img"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "image/png"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 60
---

# workflow_z_image_turbo_txt2img_bf16_cn_canny

Imported workflow skill generated from `Z Image Turbo txt2img bf16 CN Canny.json`.

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

- `comfyui_controlnet_aux`
- `rgthree-comfy`

## Links

- https://discord.com/invite/gggpkVgBf3
- https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/diffusion_models/z_image_turbo_bf16.safetensors
- https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/text_encoders/qwen_3_4b.safetensors
- https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/vae/ae.safetensors
- https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union
- https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union/resolve/main/Z-Image-Turbo-Fun-Controlnet-Union.safetensors?download=true
- https://www.youtube.com/@pixaroma

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `txt2img`
- Input modalities: `image, text_prompt`
- Output modalities: `image/png`
- Model families: `qwen, sd3, z_image_turbo`
- Node count: `17`
- Complexity score: `3`
- Resource profile: `medium`
- Estimated runtime: `moderate (about 30-120s depending on server)`
- Max latent resolution hint: `1024`x`1024`
- Max sampler steps hint: `5`

## Detected Models

- `clip`: `qwen_3_4b.safetensors` -> `models/clip`
- `vae`: `ae.safetensors` -> `models/vae`
- `diffusion_model`: `z_image_turbo_bf16.safetensors` -> `models/diffusion_models`

## Detected Custom Nodes

- `comfyui_controlnet_aux`
- `rgthree-comfy`

## Runtime Warnings

- Medium-high resolution detected; expect moderate extra runtime.
- Uses custom nodes; missing nodes can cause validation/runtime failures.
<!-- AUTO-METADATA-END -->

