---
name: curated_fluxmania_txt2img_with_cn_depth_and_upscaler_portrait_instagram_1080x1350px_4_5
description: >
  Curated ComfyUI workflow imported from `Fluxmania txt2img with CN Depth and Upscaler - Portrait Instagram 1080x1350px 4-5.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "curated", "upscaling"]
metadata.clawdbot.category: "media-editing"
metadata.clawdbot.input_type: "image/png"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 70
---

# curated_fluxmania_txt2img_with_cn_depth_and_upscaler_portrait_instagram_1080x1350px_4_5

Curated workflow skill generated from `Fluxmania txt2img with CN Depth and Upscaler - Portrait Instagram 1080x1350px 4-5.json`.

## Capability Family

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
  - `output_images` (includes image/video entries reported by Comfy history)

## Model Requirements

- `upscale_model`: `4x_NMKD-Siax_200k.pth` -> `models/upscale_models`
- `clip`: `t5-v1_1-xxl-encoder-Q8_0.gguf` -> `models/clip`
- `vae`: `ae.safetensors` -> `models/vae`
- `controlnet`: `flux-cn-pro-2.safetensors` -> `models/controlnet`
- `diffusion_model`: `fluxmania_Legacy.safetensors` -> `models/diffusion_models`

## Custom Node Requirements

- `ComfyUI-TiledDiffusion`
- `comfyui-easy-use`
- `comfyui-gguf`
- `comfyui_controlnet_aux`

## Links Extracted From Workflow Notes

- https://civitai.com/
- https://civitai.com/api/download/models/1769925?type=Model&format=SafeTensor&size=full&fp=fp8
- https://civitai.com/models/778691?modelVersionId=1769925
- https://discord.com/invite/gggpkVgBf3
- https://huggingface.co/Akumetsu971/SD_Anime_Futuristic_Armor/resolve/main/4x_NMKD-Siax_200k.pth?download=true
- https://huggingface.co/Shakker-Labs/FLUX.1-dev-ControlNet-Union-Pro-2.0/resolve/main/diffusion_pytorch_model.safetensors?download=true
- https://huggingface.co/black-forest-labs/FLUX.1-schnell
- https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/ae.safetensors?download=true
- https://huggingface.co/city96/t5-v1_1-xxl-encoder-gguf/resolve/main/t5-v1_1-xxl-encoder-Q8_0.gguf?download=true
- https://huggingface.co/city96/t5-v1_1-xxl-encoder-gguf/tree/main
- https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors?download=true
- https://www.youtube.com/@pixaroma

## Source

- Original: `comfy-data/workflows/Fluxmania txt2img with CN Depth and Upscaler - Portrait Instagram 1080x1350px 4-5.json`
