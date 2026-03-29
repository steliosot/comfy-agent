---
name: workflow_flux_krea_txt2img_with_lora_and_upscaler
description: >
  Workflow wrapper imported from `Flux Krea txt2img with Lora and Upscaler.json`.
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

# workflow_flux_krea_txt2img_with_lora_and_upscaler

Imported workflow skill generated from `Flux Krea txt2img with Lora and Upscaler.json`.

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

- `vae`: `ae.safetensors` -> `models/vae`
- `upscale_model`: `4x_NMKD-Siax_200k.pth` -> `models/upscale_models`
- `diffusion_model`: `flux1-krea-dev-Q8_0.gguf` -> `models/diffusion_models`
- `clip`: `t5-v1_1-xxl-encoder-Q8_0.gguf` -> `models/clip`

## Custom Node Requirements

- `ComfyUI-TiledDiffusion`
- `comfyui-easy-use`
- `comfyui-gguf`
- `controlaltai-nodes`
- `rgthree-comfy`

## Links

- https://discord.com/invite/gggpkVgBf3
- https://huggingface.co/Akumetsu971/SD_Anime_Futuristic_Armor/resolve/main/4x_NMKD-Siax_200k.pth?download=true
- https://huggingface.co/Comfy-Org/Lumina_Image_2.0_Repackaged/resolve/main/split_files/vae/ae.safetensors?download=true
- https://huggingface.co/Pixaroma/flux-kontext-loras/resolve/main/p1x4r0ma_woman.safetensors?download=true
- https://huggingface.co/QuantStack/FLUX.1-Krea-dev-GGUF/resolve/main/flux1-krea-dev-Q8_0.gguf?download=true
- https://huggingface.co/QuantStack/FLUX.1-Krea-dev-GGUF/tree/main
- https://huggingface.co/city96/t5-v1_1-xxl-encoder-gguf/resolve/main/t5-v1_1-xxl-encoder-Q8_0.gguf?download=true
- https://huggingface.co/city96/t5-v1_1-xxl-encoder-gguf/tree/main
- https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors?download=true
- https://www.youtube.com/@pixaroma

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `upscaling`
- Input modalities: `text_prompt`
- Output modalities: `image/png`
- Model families: `flux, sd3`
- Node count: `29`
- Complexity score: `7`
- Resource profile: `high`
- Estimated runtime: `slow (often 2-6 min depending on model/server load)`
- Max latent resolution hint: `1024`x`1024`
- Max sampler steps hint: `20`

## Detected Models

- `vae`: `ae.safetensors` -> `models/vae`
- `upscale_model`: `4x_NMKD-Siax_200k.pth` -> `models/upscale_models`
- `diffusion_model`: `flux1-krea-dev-Q8_0.gguf` -> `models/diffusion_models`
- `clip`: `t5-v1_1-xxl-encoder-Q8_0.gguf` -> `models/clip`

## Detected Custom Nodes

- `ComfyUI-TiledDiffusion`
- `comfyui-easy-use`
- `comfyui-gguf`
- `controlaltai-nodes`
- `rgthree-comfy`

## Runtime Warnings

- Large model(s) detected; ensure enough VRAM and disk space.
- Medium-high resolution detected; expect moderate extra runtime.
- Multiple custom nodes required; verify node installation/version compatibility.
<!-- AUTO-METADATA-END -->

