---
name: curated_ep52_flux_1_kontext_dev_inpaint_2
description: >
  Curated ComfyUI workflow imported from `EP52 Flux 1 Kontext Dev - Inpaint-2.json`.
homepage: https://github.com/steliosot/comfy-agent
metadata.clawdbot.os: ["darwin", "linux"]
metadata.clawdbot.requires.bins: ["python3"]
metadata.clawdbot.requires.env: ["COMFY_URL", "COMFY_AUTH_HEADER"]
metadata.clawdbot.files: ["workflow.json", "skill.py", "skill.yaml", "scripts/*"]
metadata.clawdbot.tags: ["comfyui", "workflow", "curated", "img2img_inpaint_outpaint"]
metadata.clawdbot.category: "media-editing"
metadata.clawdbot.input_type: "image/png"
metadata.clawdbot.output_type: "image/png"
metadata.clawdbot.output_can_feed_into: []
metadata.clawdbot.accepts_input_from: []
metadata.clawdbot.priority: 70
---

# curated_ep52_flux_1_kontext_dev_inpaint_2

Curated workflow skill generated from `EP52 Flux 1 Kontext Dev - Inpaint-2.json`.

## Capability Family

- `img2img_inpaint_outpaint`

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

- `diffusion_model`: `flux1-dev-kontext_fp8_scaled.safetensors` -> `models/diffusion_models`
- `vae`: `ae.safetensors` -> `models/vae`

## Custom Node Requirements

- `comfyui-easy-use`
- `comfyui-inpaint-cropandstitch`
- `rgthree-comfy`

## Links Extracted From Workflow Notes

- https://bfl.ai/models/flux-kontext
- https://discord.com/invite/gggpkVgBf3
- https://docs.bfl.ai/guides/prompting_guide_kontext_i2i
- https://docs.comfy.org/tutorials/flux/flux-1-kontext-dev
- https://docs.comfy.org/tutorials/flux/flux-1-kontext-dev#flux-kontext-prompt-techniques
- https://huggingface.co/Akumetsu971/SD_Anime_Futuristic_Armor/resolve/main/4x_NMKD-Siax_200k.pth?download=true
- https://huggingface.co/Comfy-Org/Lumina_Image_2.0_Repackaged/resolve/main/split_files/vae/ae.safetensors?download=true
- https://huggingface.co/Comfy-Org/flux1-kontext-dev_ComfyUI/resolve/main/split_files/diffusion_models/flux1-dev-kontext_fp8_scaled.safetensors
- https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors?download=true
- https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp16.safetensors
- https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp8_e4m3fn_scaled.safetensors
- https://www.youtube.com/@pixaroma

## Source

- Original: `comfy-data/workflows/EP52 Flux 1 Kontext Dev - Inpaint-2.json`
