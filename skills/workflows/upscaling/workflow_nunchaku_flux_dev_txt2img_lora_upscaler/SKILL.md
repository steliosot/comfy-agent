---
name: workflow_nunchaku_flux_dev_txt2img_lora_upscaler
description: >
  Workflow wrapper imported from `Nunchaku Flux Dev txt2img + Lora + Upscaler.json`.
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

# workflow_nunchaku_flux_dev_txt2img_lora_upscaler

Imported workflow skill generated from `Nunchaku Flux Dev txt2img + Lora + Upscaler.json`.

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
- `upscale_model`: `4xNomos2_hq_dat2.safetensors` -> `models/upscale_models`

## Custom Node Requirements

- `ComfyUI-TiledDiffusion`
- `ComfyUI-nunchaku`
- `comfyui-easy-use`
- `comfyui-nunchaku`

## Links

- https://discord.com/invite/gggpkVgBf3
- https://github.com/Tavris1/ComfyUI-Easy-Install
- https://huggingface.co/Comfy-Org/Lumina_Image_2.0_Repackaged/resolve/main/split_files/vae/ae.safetensors?download=true
- https://huggingface.co/Phips/4xNomos2_hq_dat2
- https://huggingface.co/Phips/4xNomos2_hq_dat2/resolve/main/4xNomos2_hq_dat2.safetensors?download=true
- https://huggingface.co/aleksa-codes/flux-ghibsky-illustration
- https://huggingface.co/aleksa-codes/flux-ghibsky-illustration/resolve/main/lora_v2.safetensors?download=true
- https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors?download=true
- https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp8_e4m3fn_scaled.safetensors?download=true
- https://huggingface.co/comfyanonymous/flux_text_encoders/tree/main
- https://huggingface.co/mit-han-lab/nunchaku-flux.1-dev/resolve/main/svdq-fp4_r32-flux.1-dev.safetensors?download=true
- https://huggingface.co/mit-han-lab/nunchaku-flux.1-dev/resolve/main/svdq-int4_r32-flux.1-dev.safetensors?download=true
- https://huggingface.co/mit-han-lab/nunchaku-flux.1-dev/tree/main
- https://www.youtube.com/@pixaroma

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `upscaling`
- Input modalities: `text_prompt`
- Output modalities: `image/png`
- Model families: `flux, sd3`
- Node count: `28`
- Complexity score: `4`
- Resource profile: `medium`
- Estimated runtime: `moderate (about 30-120s depending on server)`
- Max latent resolution hint: `1024`x`1024`
- Max sampler steps hint: `30`

## Detected Models

- `vae`: `ae.safetensors` -> `models/vae`
- `upscale_model`: `4xNomos2_hq_dat2.safetensors` -> `models/upscale_models`

## Detected Custom Nodes

- `ComfyUI-TiledDiffusion`
- `ComfyUI-nunchaku`
- `comfyui-easy-use`
- `comfyui-nunchaku`

## Runtime Warnings

- Medium-high resolution detected; expect moderate extra runtime.
- Multiple custom nodes required; verify node installation/version compatibility.
<!-- AUTO-METADATA-END -->

