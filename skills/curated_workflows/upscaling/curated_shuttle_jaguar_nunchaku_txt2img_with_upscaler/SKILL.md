---
name: curated_shuttle_jaguar_nunchaku_txt2img_with_upscaler
description: >
  Curated ComfyUI workflow imported from `Shuttle Jaguar (Nunchaku) txt2img with Upscaler.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "curated", "upscaling"]
metadata.clawdbot.category: "media-editing"
metadata.clawdbot.input_type: "text"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 70
---

# curated_shuttle_jaguar_nunchaku_txt2img_with_upscaler

Curated workflow skill generated from `Shuttle Jaguar (Nunchaku) txt2img with Upscaler.json`.

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
- `vae`: `ae.safetensors` -> `models/vae`

## Custom Node Requirements

- `ComfyUI-TiledDiffusion`
- `ComfyUI-nunchaku`
- `comfyui-easy-use`
- `controlaltai-nodes`

## Links Extracted From Workflow Notes

- https://discord.com/invite/gggpkVgBf3
- https://github.com/Tavris1/ComfyUI-Easy-Install/tree/Windows-Nunchaku
- https://huggingface.co/Akumetsu971/SD_Anime_Futuristic_Armor/resolve/main/4x_NMKD-Siax_200k.pth?download=true
- https://huggingface.co/Comfy-Org/Lumina_Image_2.0_Repackaged/resolve/main/split_files/vae/ae.safetensors?download=true
- https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors?download=true
- https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp8_e4m3fn_scaled.safetensors?download=true
- https://huggingface.co/comfyanonymous/flux_text_encoders/tree/main
- https://huggingface.co/mit-han-lab/nunchaku-shuttle-jaguar
- https://huggingface.co/mit-han-lab/nunchaku-shuttle-jaguar/resolve/main/svdq-fp4_r32-shuttle-jaguar.safetensors?download=true
- https://huggingface.co/mit-han-lab/nunchaku-shuttle-jaguar/resolve/main/svdq-int4_r32-shuttle-jaguar.safetensors?download=true
- https://huggingface.co/shuttleai/shuttle-jaguar
- https://www.youtube.com/@pixaroma
- https://www.youtube.com/watch?v=eATIu4lkOl0

## Source

- Original: `comfy-data/workflows/Shuttle Jaguar (Nunchaku) txt2img with Upscaler.json`
