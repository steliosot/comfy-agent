---
name: workflow_ep46_flux_dev_txt2img_with_upscaler
description: >
  Workflow wrapper imported from `EP46 Flux Dev TXT2IMG with Upscaler.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "library", "upscaling"]
metadata.clawdbot.category: "media-generation"
metadata.clawdbot.input_type: "text"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 60
---

# workflow_ep46_flux_dev_txt2img_with_upscaler

Imported workflow skill generated from `EP46 Flux Dev TXT2IMG with Upscaler.json`.

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

- `clip`: `t5-v1_1-xxl-encoder-Q8_0.gguf` -> `models/clip`
- `diffusion_model`: `flux1-dev-Q8_0.gguf` -> `models/diffusion_models`
- `upscale_model`: `4x_NMKD-Siax_200k.pth` -> `models/upscale_models`
- `vae`: `ae.safetensors` -> `models/vae`

## Custom Node Requirements

- `ComfyUI-TiledDiffusion`
- `comfyui-easy-use`
- `comfyui-gguf`
- `controlaltai-nodes`

## Links

- https://discord.com/invite/gggpkVgBf3
- https://huggingface.co/Akumetsu971/SD_Anime_Futuristic_Armor/resolve/main/4x_NMKD-Siax_200k.pth?download=true
- https://huggingface.co/black-forest-labs/FLUX.1-schnell
- https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/ae.safetensors?download=true
- https://huggingface.co/city96/FLUX.1-dev-gguf/resolve/main/flux1-dev-Q8_0.gguf?download=true
- https://huggingface.co/city96/FLUX.1-dev-gguf/tree/main
- https://huggingface.co/city96/t5-v1_1-xxl-encoder-gguf/resolve/main/t5-v1_1-xxl-encoder-Q8_0.gguf?download=true
- https://huggingface.co/city96/t5-v1_1-xxl-encoder-gguf/tree/main
- https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors?download=true
- https://www.youtube.com/@pixaroma

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `upscaling`
- Input modalities: `text_prompt`
- Output modalities: `image/png`
- Model families: `flux, sd3, wan`
- Node count: `32`
- Complexity score: `7`
- Resource profile: `high`
- Estimated runtime: `slow (often 2-6 min depending on model/server load)`
- Max latent resolution hint: `1024`x`1024`
- Max sampler steps hint: `30`

## Detected Models

- `clip`: `t5-v1_1-xxl-encoder-Q8_0.gguf` -> `models/clip`
- `diffusion_model`: `flux1-dev-Q8_0.gguf` -> `models/diffusion_models`
- `upscale_model`: `4x_NMKD-Siax_200k.pth` -> `models/upscale_models`
- `vae`: `ae.safetensors` -> `models/vae`

## Detected Custom Nodes

- `ComfyUI-TiledDiffusion`
- `comfyui-easy-use`
- `comfyui-gguf`
- `controlaltai-nodes`

## Runtime Warnings

- Large model(s) detected; ensure enough VRAM and disk space.
- Medium-high resolution detected; expect moderate extra runtime.
- Multiple custom nodes required; verify node installation/version compatibility.
<!-- AUTO-METADATA-END -->

