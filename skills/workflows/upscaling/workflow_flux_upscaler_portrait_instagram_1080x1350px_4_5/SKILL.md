---
name: workflow_flux_upscaler_portrait_instagram_1080x1350px_4_5
description: >
  Workflow wrapper imported from `Flux Upscaler - Portrait Instagram 1080x1350px 4-5.json`.
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

# workflow_flux_upscaler_portrait_instagram_1080x1350px_4_5

Imported workflow skill generated from `Flux Upscaler - Portrait Instagram 1080x1350px 4-5.json`.

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
- `diffusion_model`: `fluxmania_Legacy.safetensors` -> `models/diffusion_models`
- `upscale_model`: `4x_NMKD-Siax_200k.pth` -> `models/upscale_models`
- `vae`: `ae.safetensors` -> `models/vae`

## Custom Node Requirements

- `ComfyUI-TiledDiffusion`
- `comfyui-easy-use`
- `comfyui-gguf`
- `rgthree-comfy`

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
- Input modalities: `image, text_prompt`
- Output modalities: `image/png`
- Model families: `flux`
- Node count: `27`
- Complexity score: `4`
- Resource profile: `medium`
- Estimated runtime: `moderate (about 30-120s depending on server)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `20`

## Detected Models

- `clip`: `t5-v1_1-xxl-encoder-Q8_0.gguf` -> `models/clip`
- `diffusion_model`: `fluxmania_Legacy.safetensors` -> `models/diffusion_models`
- `upscale_model`: `4x_NMKD-Siax_200k.pth` -> `models/upscale_models`
- `vae`: `ae.safetensors` -> `models/vae`

## Detected Custom Nodes

- `ComfyUI-TiledDiffusion`
- `comfyui-easy-use`
- `comfyui-gguf`
- `rgthree-comfy`

## Runtime Warnings

- Large model(s) detected; ensure enough VRAM and disk space.
- Multiple custom nodes required; verify node installation/version compatibility.
<!-- AUTO-METADATA-END -->

