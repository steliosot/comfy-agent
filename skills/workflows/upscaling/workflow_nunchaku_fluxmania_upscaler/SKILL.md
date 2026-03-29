---
name: workflow_nunchaku_fluxmania_upscaler
description: >
  Workflow wrapper imported from `Nunchaku Fluxmania Upscaler.json`.
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

# workflow_nunchaku_fluxmania_upscaler

Imported workflow skill generated from `Nunchaku Fluxmania Upscaler.json`.

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
- `rgthree-comfy`

## Links

- https://discord.com/invite/gggpkVgBf3
- https://github.com/Tavris1/ComfyUI-Easy-Install
- https://huggingface.co/Comfy-Org/Lumina_Image_2.0_Repackaged/resolve/main/split_files/vae/ae.safetensors?download=true
- https://huggingface.co/Phips/4xNomos2_hq_dat2
- https://huggingface.co/Phips/4xNomos2_hq_dat2/resolve/main/4xNomos2_hq_dat2.safetensors?download=true
- https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors?download=true
- https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp8_e4m3fn_scaled.safetensors?download=true
- https://huggingface.co/comfyanonymous/flux_text_encoders/tree/main
- https://huggingface.co/spooknik/Fluxmania-SVDQ
- https://huggingface.co/spooknik/Fluxmania-SVDQ/resolve/main/svdq-fp4_r32-fluxmania-legacy.safetensors?download=true
- https://huggingface.co/spooknik/Fluxmania-SVDQ/resolve/main/svdq-int4_r32-fluxmania-legacy.safetensors?download=true
- https://www.youtube.com/@pixaroma

<!-- AUTO-METADATA-START -->
## Routing Metadata

- Family: `upscaling`
- Input modalities: `image, text_prompt`
- Output modalities: `image/png`
- Model families: `flux`
- Node count: `26`
- Complexity score: `2`
- Resource profile: `low`
- Estimated runtime: `fast (usually under 30s on modern GPU)`
- Max latent resolution hint: `None`x`None`
- Max sampler steps hint: `20`

## Detected Models

- `vae`: `ae.safetensors` -> `models/vae`
- `upscale_model`: `4xNomos2_hq_dat2.safetensors` -> `models/upscale_models`

## Detected Custom Nodes

- `ComfyUI-TiledDiffusion`
- `ComfyUI-nunchaku`
- `comfyui-easy-use`
- `comfyui-nunchaku`
- `rgthree-comfy`

## Runtime Warnings

- Multiple custom nodes required; verify node installation/version compatibility.
<!-- AUTO-METADATA-END -->

